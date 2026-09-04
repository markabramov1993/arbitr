// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

struct MorphoMarketParamsV2 {
    address loanToken;
    address collateralToken;
    address oracle;
    address irm;
    uint256 lltv;
}

interface IERC20LiquidatorV2 {
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
}

interface IMorphoLiquidatorV2 {
    function liquidate(
        MorphoMarketParamsV2 memory marketParams,
        address borrower,
        uint256 seizedAssets,
        uint256 repaidShares,
        bytes calldata data
    ) external returns (uint256 seizedAssetsOut, uint256 repaidAssetsOut);
}

interface IUniV3RouterV2 {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut);
}

interface IAeroSlipstreamRouterV2 {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        int24 tickSpacing;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut);
}

/// @notice Morpho Blue liquidation executor that uses the protocol callback to sell seized
/// collateral before Morpho pulls repayment. No debt-token trading capital is required.
/// Supports direct Uniswap V3 and Aerodrome Slipstream exits on Base.
contract MorphoSelfFundedLiquidatorV2 {
    uint8 public constant VENUE_UNISWAP_V3 = 1;
    uint8 public constant VENUE_AERODROME_SLIPSTREAM = 2;

    error NotOwner();
    error NotMorpho();
    error Busy();
    error NoActiveLiquidation();
    error InvalidAddress();
    error InvalidMarket();
    error InvalidVenue();
    error InvalidPoolParameter();
    error ZeroShares();
    error NoCollateralSeized();
    error SwapOutputTooLow(uint256 amountOut, uint256 requiredOut);
    error ProfitTooLow(uint256 profit, uint256 minProfit);
    error TokenCallFailed(address token, bytes4 selector);

    event LiquidationExecuted(
        bytes32 indexed marketIdHint,
        address indexed borrower,
        uint8 venue,
        int24 poolParameter,
        uint256 repaidShares,
        uint256 repaidAssets,
        uint256 seizedAssets,
        uint256 profit
    );

    address public immutable owner;
    IMorphoLiquidatorV2 public immutable morpho;
    IUniV3RouterV2 public immutable uniRouter;
    IAeroSlipstreamRouterV2 public immutable aeroRouter;

    bool private active;
    address private activeLoanToken;
    address private activeCollateralToken;
    uint256 private collateralBalanceBefore;
    uint256 private loanBalanceBefore;
    uint8 private activeVenue;
    int24 private activePoolParameter;
    uint256 private activeMinSwapOut;
    uint256 private activeMinProfit;
    uint256 private callbackRepaidAssets;
    uint256 private callbackSeizedAssets;

    constructor(address morpho_, address uniRouter_, address aeroRouter_) {
        if (morpho_ == address(0) || uniRouter_ == address(0) || aeroRouter_ == address(0)) revert InvalidAddress();
        owner = msg.sender;
        morpho = IMorphoLiquidatorV2(morpho_);
        uniRouter = IUniV3RouterV2(uniRouter_);
        aeroRouter = IAeroSlipstreamRouterV2(aeroRouter_);
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    /// @param venue 1=Uniswap V3, 2=Aerodrome Slipstream.
    /// @param poolParameter Uniswap fee (positive int24) or Aerodrome tickSpacing.
    function execute(
        MorphoMarketParamsV2 calldata marketParams,
        address borrower,
        uint256 repaidShares,
        uint8 venue,
        int24 poolParameter,
        uint256 minSwapOut,
        uint256 minProfit,
        bytes32 marketIdHint
    ) external onlyOwner returns (uint256 profit) {
        if (active) revert Busy();
        if (borrower == address(0)) revert InvalidAddress();
        if (marketParams.loanToken == address(0) || marketParams.collateralToken == address(0)) revert InvalidMarket();
        if (marketParams.loanToken == marketParams.collateralToken) revert InvalidMarket();
        if (repaidShares == 0) revert ZeroShares();
        if (venue != VENUE_UNISWAP_V3 && venue != VENUE_AERODROME_SLIPSTREAM) revert InvalidVenue();
        if (poolParameter <= 0) revert InvalidPoolParameter();

        active = true;
        activeLoanToken = marketParams.loanToken;
        activeCollateralToken = marketParams.collateralToken;
        collateralBalanceBefore = IERC20LiquidatorV2(marketParams.collateralToken).balanceOf(address(this));
        loanBalanceBefore = IERC20LiquidatorV2(marketParams.loanToken).balanceOf(address(this));
        activeVenue = venue;
        activePoolParameter = poolParameter;
        activeMinSwapOut = minSwapOut;
        activeMinProfit = minProfit;
        callbackRepaidAssets = 0;
        callbackSeizedAssets = 0;

        (uint256 seizedAssetsOut, uint256 repaidAssetsOut) =
            morpho.liquidate(marketParams, borrower, 0, repaidShares, hex"01");

        // Cross-check the callback bookkeeping against Morpho's own return values.
        if (seizedAssetsOut != callbackSeizedAssets || repaidAssetsOut != callbackRepaidAssets) revert InvalidMarket();

        uint256 endingLoanBalance = IERC20LiquidatorV2(marketParams.loanToken).balanceOf(address(this));
        profit = endingLoanBalance - loanBalanceBefore;
        if (profit < minProfit) revert ProfitTooLow(profit, minProfit);

        uint256 repaidAssets = callbackRepaidAssets;
        uint256 seizedAssets = callbackSeizedAssets;
        uint8 usedVenue = activeVenue;
        int24 usedPoolParameter = activePoolParameter;

        _clearContext();

        emit LiquidationExecuted(
            marketIdHint,
            borrower,
            usedVenue,
            usedPoolParameter,
            repaidShares,
            repaidAssets,
            seizedAssets,
            profit
        );

        if (profit != 0) _safeTransfer(marketParams.loanToken, owner, profit);
    }

    /// @notice Called by Morpho after collateral is transferred here and before repayment is pulled.
    function onMorphoLiquidate(uint256 repaidAssets, bytes calldata) external {
        if (msg.sender != address(morpho)) revert NotMorpho();
        if (!active) revert NoActiveLiquidation();

        uint256 currentCollateral = IERC20LiquidatorV2(activeCollateralToken).balanceOf(address(this));
        uint256 seized = currentCollateral - collateralBalanceBefore;
        if (seized == 0) revert NoCollateralSeized();

        uint256 requiredOut = repaidAssets + activeMinProfit;
        if (activeMinSwapOut > requiredOut) requiredOut = activeMinSwapOut;

        uint256 amountOut;
        if (activeVenue == VENUE_UNISWAP_V3) {
            uint24 fee = uint24(uint256(int256(activePoolParameter)));
            _forceApprove(activeCollateralToken, address(uniRouter), seized);
            amountOut = uniRouter.exactInputSingle(
                IUniV3RouterV2.ExactInputSingleParams({
                    tokenIn: activeCollateralToken,
                    tokenOut: activeLoanToken,
                    fee: fee,
                    recipient: address(this),
                    amountIn: seized,
                    amountOutMinimum: requiredOut,
                    sqrtPriceLimitX96: 0
                })
            );
        } else if (activeVenue == VENUE_AERODROME_SLIPSTREAM) {
            _forceApprove(activeCollateralToken, address(aeroRouter), seized);
            amountOut = aeroRouter.exactInputSingle(
                IAeroSlipstreamRouterV2.ExactInputSingleParams({
                    tokenIn: activeCollateralToken,
                    tokenOut: activeLoanToken,
                    tickSpacing: activePoolParameter,
                    recipient: address(this),
                    deadline: block.timestamp,
                    amountIn: seized,
                    amountOutMinimum: requiredOut,
                    sqrtPriceLimitX96: 0
                })
            );
        } else {
            revert InvalidVenue();
        }

        if (amountOut < requiredOut) revert SwapOutputTooLow(amountOut, requiredOut);
        _forceApprove(activeLoanToken, address(morpho), repaidAssets);
        callbackRepaidAssets = repaidAssets;
        callbackSeizedAssets = seized;
    }

    function rescue(address token, uint256 amount) external onlyOwner {
        if (active) revert Busy();
        _safeTransfer(token, owner, amount);
    }

    function _clearContext() internal {
        active = false;
        activeLoanToken = address(0);
        activeCollateralToken = address(0);
        collateralBalanceBefore = 0;
        loanBalanceBefore = 0;
        activeVenue = 0;
        activePoolParameter = 0;
        activeMinSwapOut = 0;
        activeMinProfit = 0;
        callbackRepaidAssets = 0;
        callbackSeizedAssets = 0;
    }

    function _forceApprove(address token, address spender, uint256 amount) internal {
        if (_callOptionalBool(token, abi.encodeWithSelector(IERC20LiquidatorV2.approve.selector, spender, amount))) return;
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20LiquidatorV2.approve.selector, spender, 0))) {
            revert TokenCallFailed(token, IERC20LiquidatorV2.approve.selector);
        }
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20LiquidatorV2.approve.selector, spender, amount))) {
            revert TokenCallFailed(token, IERC20LiquidatorV2.approve.selector);
        }
    }

    function _safeTransfer(address token, address to, uint256 amount) internal {
        if (!_callOptionalBool(token, abi.encodeWithSelector(IERC20LiquidatorV2.transfer.selector, to, amount))) {
            revert TokenCallFailed(token, IERC20LiquidatorV2.transfer.selector);
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
