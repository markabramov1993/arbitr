// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20FlashLite {
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

interface IAaveV3PoolLite {
    function flashLoanSimple(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

interface IAtomicRouteHarnessLite {
    function execute(address inputToken, uint256 amountIn, uint256 minFinalAmount, bytes calldata program)
        external
        returns (uint256 finalAmount);
}

/// @notice Controlled Aave V3 flash-loan wrapper for Profit Engine fork/live validation.
/// @dev Designed to pair with AtomicRouteHarness. Deployment/signing remains a separate operator decision.
contract FlashArbExecutor {
    error NotOwner();
    error BadCallback();
    error AlreadyRunning();
    error ApproveFailed();
    error TransferFailed();
    error Unprofitable(uint256 profit, uint256 minProfit);

    IAaveV3PoolLite public immutable pool;
    IAtomicRouteHarnessLite public immutable harness;
    address public owner;
    bool private running;

    event OwnershipTransferred(address indexed oldOwner, address indexed newOwner);
    event FlashArbExecuted(
        address indexed asset,
        uint256 amount,
        uint256 premium,
        uint256 profit,
        address indexed recipient
    );

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor(address pool_, address harness_, address owner_) {
        if (pool_ == address(0) || harness_ == address(0) || owner_ == address(0)) revert BadCallback();
        pool = IAaveV3PoolLite(pool_);
        harness = IAtomicRouteHarnessLite(harness_);
        owner = owner_;
        emit OwnershipTransferred(address(0), owner_);
    }

    /// @notice Borrow `amount`, execute the encoded DEX route, repay Aave, and forward realized profit.
    /// @param minProfit Minimum post-premium profit denominated in `asset` raw units.
    function run(address asset, uint256 amount, uint256 minProfit, bytes calldata program, address profitRecipient)
        external
        onlyOwner
        returns (uint256 profit)
    {
        if (running) revert AlreadyRunning();
        if (asset == address(0) || amount == 0 || profitRecipient == address(0)) revert BadCallback();

        uint256 beforeBalance = IERC20FlashLite(asset).balanceOf(address(this));
        running = true;
        pool.flashLoanSimple(address(this), asset, amount, abi.encode(minProfit, program), 0);
        running = false;

        uint256 afterBalance = IERC20FlashLite(asset).balanceOf(address(this));
        profit = afterBalance > beforeBalance ? afterBalance - beforeBalance : 0;
        if (profit < minProfit) revert Unprofitable(profit, minProfit);

        if (profit != 0) _safeTransfer(asset, profitRecipient, profit);
    }

    /// @notice Aave V3 flashLoanSimple callback.
    function executeOperation(address asset, uint256 amount, uint256 premium, address initiator, bytes calldata params)
        external
        returns (bool)
    {
        if (msg.sender != address(pool) || initiator != address(this) || !running) revert BadCallback();
        (uint256 minProfit, bytes memory program) = abi.decode(params, (uint256, bytes));

        uint256 amountOwed = amount + premium;
        _safeApprove(asset, address(harness), amount);
        harness.execute(asset, amount, amountOwed + minProfit, program);

        uint256 balance = IERC20FlashLite(asset).balanceOf(address(this));
        uint256 callbackProfit = balance > amountOwed ? balance - amountOwed : 0;
        if (callbackProfit < minProfit) revert Unprofitable(callbackProfit, minProfit);

        // Aave pulls amount + premium after this callback returns.
        _safeApprove(asset, address(pool), amountOwed);
        emit FlashArbExecuted(asset, amount, premium, callbackProfit, owner);
        return true;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        if (newOwner == address(0)) revert BadCallback();
        address oldOwner = owner;
        owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }

    /// @notice Recover tokens accidentally sent to the executor while it is idle.
    function rescue(address token, address to, uint256 amount) external onlyOwner {
        if (running || to == address(0)) revert BadCallback();
        _safeTransfer(token, to, amount);
    }

    function _safeApprove(address token, address spender, uint256 amount) internal {
        (bool ok0, bytes memory ret0) = token.call(abi.encodeWithSelector(IERC20FlashLite.approve.selector, spender, 0));
        if (!ok0 || (ret0.length != 0 && !abi.decode(ret0, (bool)))) revert ApproveFailed();
        (bool ok1, bytes memory ret1) = token.call(abi.encodeWithSelector(IERC20FlashLite.approve.selector, spender, amount));
        if (!ok1 || (ret1.length != 0 && !abi.decode(ret1, (bool)))) revert ApproveFailed();
    }

    function _safeTransfer(address token, address to, uint256 amount) internal {
        (bool ok, bytes memory ret) = token.call(abi.encodeWithSelector(IERC20FlashLite.transfer.selector, to, amount));
        if (!ok || (ret.length != 0 && !abi.decode(ret, (bool)))) revert TransferFailed();
    }
}
