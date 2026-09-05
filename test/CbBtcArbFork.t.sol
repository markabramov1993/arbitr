// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface VmCbBtc {
    function createSelectFork(string calldata urlOrAlias) external returns (uint256 forkId);
    function prank(address msgSender) external;
}

interface IERC20CbBtc {
    function balanceOf(address) external view returns (uint256);
    function transfer(address,uint256) external returns (bool);
    function approve(address,uint256) external returns (bool);
}

interface IUniRouterCbBtc {
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

interface IAeroRouterCbBtc {
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

contract CbBtcArbForkTest {
    VmCbBtc constant VM = VmCbBtc(address(uint160(uint256(keccak256("hevm cheat code")))));

    address constant USDC  = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913;
    address constant CBBTC = 0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf;

    address constant UNI_ROUTER  = 0x2626664c2603336E57B271c5C0b26F421741e481;
    // Slipstream V3 router paired with the newest Base CLFactory.
    address constant AERO_ROUTER = 0x698Cb2b6dd822994581fEa6eA4Fc755d1363A92F;

    address constant FUNDING_HOLDER = 0xb4CB800910B228ED3d0834cF79D697127BBB00e5;

    event log_named_uint(string key, uint256 val);
    event log_named_int(string key, int256 val);

    function setUp() public {
        // Prefer Base's public RPC here; the previous Alchemy-public run hit 429s.
        VM.createSelectFork("https://mainnet.base.org");
    }

    // The live spot shortlist currently selects Uni 1 bp -> Aero tick spacing 1.
    // Sweep small sizes first because a few-bps edge disappears quickly with impact.
    function testCbBtc25() public { _roundTrip(25e6, 1); }
    function testCbBtc50() public { _roundTrip(50e6, 1); }
    function testCbBtc100() public { _roundTrip(100e6, 1); }
    function testCbBtc250() public { _roundTrip(250e6, 1); }
    function testCbBtc500() public { _roundTrip(500e6, 1); }
    function testCbBtc1000() public { _roundTrip(1_000e6, 1); }

    // Control route retained to expose how much worse the previous spacing-50 leg is.
    function testCbBtc100Spacing50Control() public { _roundTrip(100e6, 50); }

    function _roundTrip(uint256 amountIn, int24 aeroSpacing) internal {
        VM.prank(FUNDING_HOLDER);
        require(IERC20CbBtc(USDC).transfer(address(this), amountIn), "fund");

        require(IERC20CbBtc(USDC).approve(UNI_ROUTER, amountIn), "approve uni");
        uint256 cbBtcOut = IUniRouterCbBtc(UNI_ROUTER).exactInputSingle(
            IUniRouterCbBtc.ExactInputSingleParams({
                tokenIn: USDC,
                tokenOut: CBBTC,
                fee: 100,
                recipient: address(this),
                amountIn: amountIn,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            })
        );

        require(IERC20CbBtc(CBBTC).approve(AERO_ROUTER, cbBtcOut), "approve aero");
        uint256 finalUsdc = IAeroRouterCbBtc(AERO_ROUTER).exactInputSingle(
            IAeroRouterCbBtc.ExactInputSingleParams({
                tokenIn: CBBTC,
                tokenOut: USDC,
                tickSpacing: aeroSpacing,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: cbBtcOut,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            })
        );

        emit log_named_uint("aero_tick_spacing", uint256(uint24(aeroSpacing)));
        emit log_named_uint("amountIn_USDC_6dec", amountIn);
        emit log_named_uint("cbBTC_out_8dec", cbBtcOut);
        emit log_named_uint("final_USDC_6dec", finalUsdc);
        emit log_named_int("grossPnl_USDC_6dec", int256(finalUsdc) - int256(amountIn));
    }
}
