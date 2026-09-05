// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/FlashArbExecutor.sol";

interface IFlashArbCallback {
    function executeOperation(address asset, uint256 amount, uint256 premium, address initiator, bytes calldata params)
        external
        returns (bool);
}

contract MockFlashToken {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _move(msg.sender, to, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 allowed = allowance[from][msg.sender];
        require(allowed >= amount, "allowance");
        if (allowed != type(uint256).max) allowance[from][msg.sender] = allowed - amount;
        _move(from, to, amount);
        return true;
    }

    function _move(address from, address to, uint256 amount) internal {
        require(balanceOf[from] >= amount, "balance");
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
    }
}

contract MockAtomicHarness is IAtomicRouteHarnessLite {
    uint256 public configuredFinalAmount;

    function setFinalAmount(uint256 amount) external {
        configuredFinalAmount = amount;
    }

    function execute(address inputToken, uint256 amountIn, uint256 minFinalAmount, bytes calldata)
        external
        returns (uint256 finalAmount)
    {
        MockFlashToken token = MockFlashToken(inputToken);
        require(token.transferFrom(msg.sender, address(this), amountIn), "pull");
        finalAmount = configuredFinalAmount;
        require(finalAmount >= minFinalAmount, "route below floor");
        token.mint(msg.sender, finalAmount);
    }
}

contract MockAavePool is IAaveV3PoolLite {
    uint256 public premium;

    constructor(uint256 premium_) {
        premium = premium_;
    }

    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16
    ) external {
        MockFlashToken token = MockFlashToken(asset);
        require(token.transfer(receiverAddress, amount), "loan transfer");
        require(
            IFlashArbCallback(receiverAddress).executeOperation(asset, amount, premium, msg.sender, params),
            "callback false"
        );
        require(token.transferFrom(receiverAddress, address(this), amount + premium), "repayment");
    }
}

contract FlashArbExecutorSafetyTest {
    MockFlashToken internal token;
    MockAtomicHarness internal harness;
    MockAavePool internal pool;
    FlashArbExecutor internal executor;

    uint256 internal constant AMOUNT = 1_000_000;
    uint256 internal constant PREMIUM = 900;

    function setUp() public {
        token = new MockFlashToken();
        harness = new MockAtomicHarness();
        pool = new MockAavePool(PREMIUM);
        executor = new FlashArbExecutor(address(pool), address(harness), address(this));
        token.mint(address(pool), 10 * AMOUNT);
    }

    function testFlashArbRepaysPoolAndPaysOnlyProfit() external {
        uint256 minProfit = 25_000;
        harness.setFinalAmount(AMOUNT + PREMIUM + minProfit);

        uint256 poolBefore = token.balanceOf(address(pool));
        uint256 ownerBefore = token.balanceOf(address(this));

        uint256 profit = executor.run(address(token), AMOUNT, minProfit, hex"0102", address(this));

        require(profit == minProfit, "profit mismatch");
        require(token.balanceOf(address(this)) - ownerBefore == minProfit, "recipient mismatch");
        require(token.balanceOf(address(pool)) - poolBefore == PREMIUM, "premium not repaid");
        require(token.balanceOf(address(executor)) == 0, "executor dust");
    }

    function testRouteBelowRequiredFloorReverts() external {
        uint256 minProfit = 25_000;
        harness.setFinalAmount(AMOUNT + PREMIUM + minProfit - 1);

        (bool ok,) = address(executor).call(
            abi.encodeCall(FlashArbExecutor.run, (address(token), AMOUNT, minProfit, bytes(""), address(this)))
        );
        require(!ok, "unprofitable route unexpectedly succeeded");
    }

    function testUnauthorizedCallbackReverts() external {
        (bool ok, bytes memory ret) = address(executor).call(
            abi.encodeCall(
                FlashArbExecutor.executeOperation,
                (address(token), AMOUNT, PREMIUM, address(executor), bytes(""))
            )
        );
        require(!ok, "unauthorized callback unexpectedly succeeded");
        require(_selector(ret) == FlashArbExecutor.BadCallback.selector, "wrong revert selector");
    }

    function testOnlyOwnerCanRun() external {
        FlashArbCaller outsider = new FlashArbCaller();
        (bool ok, bytes memory ret) = outsider.tryRun(executor, address(token), AMOUNT);
        require(!ok, "non-owner run unexpectedly succeeded");
        require(_selector(ret) == FlashArbExecutor.NotOwner.selector, "wrong owner revert");
    }

    function _selector(bytes memory ret) internal pure returns (bytes4 sel) {
        if (ret.length < 4) return bytes4(0);
        assembly {
            sel := mload(add(ret, 32))
        }
    }
}

contract FlashArbCaller {
    function tryRun(FlashArbExecutor executor, address asset, uint256 amount)
        external
        returns (bool ok, bytes memory ret)
    {
        (ok, ret) = address(executor).call(
            abi.encodeCall(FlashArbExecutor.run, (asset, amount, 1, bytes(""), address(this)))
        );
    }
}
