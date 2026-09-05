// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/MorphoSelfFundedLiquidatorV2.sol";

contract MockTokenLiquidatorV2 {
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

contract MockUniRouterLiquidatorV2 is IUniV3RouterV2 {
    function exactInputSingle(ExactInputSingleParams calldata p) external payable returns (uint256 amountOut) {
        require(MockTokenLiquidatorV2(p.tokenIn).transferFrom(msg.sender, address(this), p.amountIn), "pull collateral");
        // Deterministic positive spread for unit testing only.
        amountOut = p.amountOutMinimum + 5;
        MockTokenLiquidatorV2(p.tokenOut).mint(p.recipient, amountOut);
    }
}

interface IMorphoCallbackTargetV2 {
    function onMorphoLiquidate(uint256 repaidAssets, bytes calldata data) external;
}

contract MockMorphoLiquidatorV2 is IMorphoLiquidatorV2 {
    bool public doubleCallback;
    bool public skipCallback;
    uint256 public constant SEIZED = 100;

    function setDoubleCallback(bool value) external {
        doubleCallback = value;
    }

    function setSkipCallback(bool value) external {
        skipCallback = value;
    }

    function liquidate(
        MorphoMarketParamsV2 memory marketParams,
        address,
        uint256,
        uint256 repaidShares,
        bytes calldata data
    ) external returns (uint256 seizedAssetsOut, uint256 repaidAssetsOut) {
        MockTokenLiquidatorV2 collateral = MockTokenLiquidatorV2(marketParams.collateralToken);
        MockTokenLiquidatorV2 loan = MockTokenLiquidatorV2(marketParams.loanToken);

        require(collateral.transfer(msg.sender, SEIZED), "send collateral");

        if (!skipCallback) {
            IMorphoCallbackTargetV2(msg.sender).onMorphoLiquidate(repaidShares, data);
            if (doubleCallback) {
                // A hostile/buggy repeated callback must be rejected before a second swap.
                IMorphoCallbackTargetV2(msg.sender).onMorphoLiquidate(repaidShares, data);
            }
        }

        require(loan.transferFrom(msg.sender, address(this), repaidShares), "pull repayment");
        return (SEIZED, repaidShares);
    }
}

contract MorphoSelfFundedLiquidatorV2SafetyTest {
    MockTokenLiquidatorV2 internal loan;
    MockTokenLiquidatorV2 internal collateral;
    MockMorphoLiquidatorV2 internal morpho;
    MockUniRouterLiquidatorV2 internal router;
    MorphoSelfFundedLiquidatorV2 internal liquidator;

    function setUp() public {
        loan = new MockTokenLiquidatorV2();
        collateral = new MockTokenLiquidatorV2();
        morpho = new MockMorphoLiquidatorV2();
        router = new MockUniRouterLiquidatorV2();
        liquidator = new MorphoSelfFundedLiquidatorV2(address(morpho), address(router), address(router));
        collateral.mint(address(morpho), 1_000);
    }

    function testSingleCallbackSucceedsAndPaysOnlyProfit() external {
        uint256 beforeOwner = loan.balanceOf(address(this));
        uint256 profit = liquidator.execute(_market(), address(0xB0B), 50, 1, 500, 0, 1, bytes32(uint256(1)));
        uint256 afterOwner = loan.balanceOf(address(this));

        require(profit == 6, "unexpected profit");
        require(afterOwner - beforeOwner == profit, "owner did not receive profit");
        require(loan.balanceOf(address(morpho)) == 50, "Morpho repayment mismatch");
    }

    function testRepeatedMorphoCallbackIsRejected() external {
        morpho.setDoubleCallback(true);
        (bool ok, bytes memory ret) = address(liquidator).call(
            abi.encodeCall(
                MorphoSelfFundedLiquidatorV2.execute,
                (_market(), address(0xB0B), 50, uint8(1), int24(500), 0, 1, bytes32(uint256(2)))
            )
        );
        require(!ok, "double callback unexpectedly succeeded");
        require(_selector(ret) == MorphoSelfFundedLiquidatorV2.CallbackAlreadyHandled.selector, "wrong revert selector");
    }

    function testMissingMorphoCallbackIsRejected() external {
        morpho.setSkipCallback(true);
        (bool ok, bytes memory ret) = address(liquidator).call(
            abi.encodeCall(
                MorphoSelfFundedLiquidatorV2.execute,
                (_market(), address(0xB0B), 50, uint8(1), int24(500), 0, 1, bytes32(uint256(3)))
            )
        );
        require(!ok, "missing callback unexpectedly succeeded");
        require(_selector(ret) == MorphoSelfFundedLiquidatorV2.MissingCallback.selector, "wrong revert selector");
    }

    function _market() internal view returns (MorphoMarketParamsV2 memory p) {
        p = MorphoMarketParamsV2({
            loanToken: address(loan),
            collateralToken: address(collateral),
            oracle: address(0x1234),
            irm: address(0x5678),
            lltv: 0.86e18
        });
    }

    function _selector(bytes memory ret) internal pure returns (bytes4 sel) {
        if (ret.length < 4) return bytes4(0);
        assembly {
            sel := mload(add(ret, 32))
        }
    }
}
