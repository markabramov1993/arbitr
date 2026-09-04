// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Morpho Blue market parameters. Field order must match Morpho exactly.
struct MarketParams {
    address loanToken;
    address collateralToken;
    address oracle;
    address irm;
    uint256 lltv;
}

interface IERC20Minimal {
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

interface IMorphoBlue {
    function liquidate(
        MarketParams memory marketParams,
        address borrower,
        uint256 seizedAssets,
        uint256 repaidShares,
        bytes calldata data
    ) external returns (uint256 seizedAssetsOut, uint256 repaidAssetsOut);
}

interface IV3SwapRouter02 {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }

    function exactInputSingle(ExactInputSingleParams calldata params)
        external
        payable
        returns (uint256 amountOut);
}

/// @title MorphoSelfFundedLiquidator
/// @notice Liquidates an unhealthy Morpho Blue position without pre-funding the debt token.
/// @dev Morpho transfers seized collateral to this contract, then calls onMorphoLiquidate(),
///      and only after the callback pulls the repayment token. The callback sells the seized
///      collateral for the loan token and approves the exact repayment amount.
///
///      This first version deliberately supports one direct Uniswap V3 hop. The opportunity
///      engine must quote and validate the route on a current fork before execute() is sent.
contract MorphoSelfFundedLiquidator {
    error NotOwner();
    error NotMorpho();
    error ReentrantExecution();
    error NoActiveLiquidation();
    error InvalidAddress();
    error InvalidMarket();
    error ZeroShares();
    error NoCollateralSeized();
    error SwapOutputTooLow(uint256 amountOut, uint256 requiredOut);
    error ProfitTooLow(uint256 profit, uint256 minProfit);
    error TokenCallFailed(address token, bytes4 selector);

    event LiquidationExecuted(
        bytes32 indexed marketIdHint,
        address indexed borrower,
        address indexed loanToken,
        address collateralToken,
        uint256 repaidShares,
        uint256 repaidAssets,
        uint256 seizedAssets,
        uint256 profit
    );

    address public immutable owner;
    IMorphoBlue public immutable morpho;
    IV3SwapRouter02 public immutable router;

    bool private active;
    address private activeLoanToken;
    address private activeCollateralToken;
    uint256 private collateralBalanceBefore;
    uint256 private loanBalanceBefore;
    uint24 private activePoolFee;
    uint256 private activeMinSwapOut;
    uint256 private activeMinProfit;
    uint256 private callbackRepaidAssets;
    uint256 private callbackSeizedAssets;

    constructor(address morpho_, address router_) {
        if (morpho_ == address(0) || router_ == address(0)) revert InvalidAddress();
        owner = msg.sender;
        morpho = IMorphoBlue(morpho_);
        router = IV3SwapRouter02(router_);
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    /// @notice Execute one pre-validated liquidation.
    /// @param marketParams Exact current Morpho market parameters.
    /// @param borrower Unhealthy borrower.
    /// @param repaidShares Borrow shares to repay. Normally the scanner supplies the full current amount.
    /// @param poolFee Direct Uniswap V3 collateral/loan pool fee tier.
    /// @param minSwapOut Scanner-provided minimum output for the collateral sale.
    /// @param minProfit Minimum profit denominated in loan-token native units.
    /// @param marketIdHint Optional market id included only in the emitted event for observability.
    function execute(
        MarketParams calldata marketParams,
        address borrower,
        uint256 repaidShares,
        uint24 poolFee,
        uint256 minSwapOut,
        uint256 minProfit,
        bytes32 marketIdHint
    ) external onlyOwner returns (uint256 profit) {
        if (active) revert ReentrantExecution();
        if (borrower == address(0)) revert InvalidAddress();
        if (marketParams.loanToken == address(0) || marketParams.collateralToken == address(0)) {
            revert InvalidMarket();
        }
        if (marketParams.loanToken == marketParams.collateralToken) revert InvalidMarket();
        if (repaidShares == 0) revert ZeroShares();

        active = true;
        activeLoanToken = marketParams.loanToken;
        activeCollateralToken = marketParams.collateralToken;
        collateralBalanceBefore = IERC20Minimal(marketParams.collateralToken).balanceOf(address(this));
        loanBalanceBefore = IERC20Minimal(marketParams.loanToken).balanceOf(address(this));
        activePoolFee = poolFee;
        activeMinSwapOut = minSwapOut;
        activeMinProfit = minProfit;
        callbackRepaidAssets = 0;
        callbackSeizedAssets = 0;

        // Non-empty data makes Morpho invoke onMorphoLiquidate() after transferring collateral
        // and before pulling the loan-token repayment.
        morpho.liquidate(marketParams, borrower, 0, repaidShares, hex"01");

        uint256 endingLoanBalance = IERC20Minimal(marketParams.loanToken).balanceOf(address(this));
        profit = endingLoanBalance - loanBalanceBefore;
        if (profit < minProfit) revert ProfitTooLow(profit, minProfit);

        uint256 repaidAssets = callbackRepaidAssets;
        uint256 seizedAssets = callbackSeizedAssets;

        _clearContext();

        if (profit != 0) _safeTransfer(marketParams.loanToken, owner, profit);

        emit LiquidationExecuted(
            marketIdHint,
            borrower,
            marketParams.loanToken,
            marketParams.collateralToken,
            repaidShares,
            repaidAssets,
            seizedAssets,
            profit
        );
    }

    /// @notice Morpho liquidation callback. Must only be reached during execute().
    function onMorphoLiquidate(uint256 repaidAssets, bytes calldata) external {
        if (msg.sender != address(morpho)) revert NotMorpho();
        if (!active) revert NoActiveLiquidation();

        uint256 currentCollateral = IERC20Minimal(activeCollateralToken).balanceOf(address(this));
        uint256 seized = currentCollateral - collateralBalanceBefore;
        if (seized == 0) revert NoCollateralSeized();

        uint256 requiredOut = repaidAssets + activeMinProfit;
        if (activeMinSwapOut > requiredOut) requiredOut = activeMinSwapOut;

        _forceApprove(activeCollateralToken, address(router), seized);

        uint256 amountOut = router.exactInputSingle(
            IV3SwapRouter02.ExactInputSingleParams({
                tokenIn: activeCollateralToken,
                tokenOut: activeLoanToken,
                fee: activePoolFee,
                recipient: address(this),
                amountIn: seized,
                amountOutMinimum: requiredOut,
                sqrtPriceLimitX96: 0
            })
        );

        if (amountOut < requiredOut) revert SwapOutputTooLow(amountOut, requiredOut);

        // Morpho pulls the repayment after this callback returns.
        _forceApprove(activeLoanToken, address(morpho), repaidAssets);

        callbackRepaidAssets = repaidAssets;
        callbackSeizedAssets = seized;
    }

    /// @notice Recover an accidentally sent token when no liquidation is executing.
    function rescue(address token, uint256 amount) external onlyOwner {
        if (active) revert ReentrantExecution();
        _safeTransfer(token, owner, amount);
    }

    function _clearContext() internal {
        active = false;
        activeLoanToken = address(0);
        activeCollateralToken = address(0);
        collateralBalanceBefore = 0;
        loanBalanceBefore = 0;
        activePoolFee = 0;
        activeMinSwapOut = 0;
        activeMinProfit = 0;
        callbackRepaidAssets = 0;
        callbackSeizedAssets = 0;
    }

    function _forceApprove(address token, address spender, uint256 amount) internal {
        if (_callOptionalBool(token, abi.encodeWithSelector(IERC20Minimal.approve.selector, spender, amount))) return;
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20Minimal.approve.selector, spender, 0))) {
            revert TokenCallFailed(token, IERC20Minimal.approve.selector);
        }
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20Minimal.approve.selector, spender, amount))) {
            revert TokenCallFailed(token, IERC20Minimal.approve.selector);
        }
    }

    function _safeTransfer(address token, address to, uint256 amount) internal {
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20Minimal.transfer.selector, to, amount))) {
            revert TokenCallFailed(token, IERC20Minimal.transfer.selector);
        }
    }

    function _callOptionalBool(address token, bytes memory data) internal returns (bool) {
        (bool ok, bytes memory ret) = token.call(data);
        if (!ok) return false;
        if (ret.length == 0) return true;
        if (ret.length < 32) return false;
        return abi.decode(ret, (bool));
    }
}
