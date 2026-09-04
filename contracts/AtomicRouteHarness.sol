// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20Lite {
    function balanceOf(address) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IUniswapV2PairLite {
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function swap(uint256 amount0Out, uint256 amount1Out, address to, bytes calldata data) external;
}

interface IV3Router02Lite {
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

interface IV3ClassicRouterLite {
    struct ExactInputSingleParams {
        address tokenIn;
        address tokenOut;
        uint24 fee;
        address recipient;
        uint256 deadline;
        uint256 amountIn;
        uint256 amountOutMinimum;
        uint160 sqrtPriceLimitX96;
    }
    function exactInputSingle(ExactInputSingleParams calldata params) external payable returns (uint256 amountOut);
}

interface ICurvePoolLite {
    function exchange(int128 i, int128 j, uint256 dx, uint256 minDy) external returns (uint256);
}

interface IBalancerV3RouterLite {
    function swapSingleTokenExactIn(
        address pool,
        IERC20Lite tokenIn,
        IERC20Lite tokenOut,
        uint256 exactAmountIn,
        uint256 minAmountOut,
        uint256 deadline,
        bool wethIsEth,
        bytes calldata userData
    ) external payable returns (uint256 amountOut);
}

/// @notice Local/fork research harness for executing a mixed DEX route atomically.
/// @dev It is intentionally NOT a Flash Loan receiver and is not intended for public-chain deployment.
/// Program format is repeated TLV records:
/// [kind:1][target:20][tokenIn:20][tokenOut:20][payloadLen:2][payload:N]
/// kinds: 1=V2 direct pair, 2=V3 exactInputSingle, 3=Curve exchange, 4=Balancer V3 exact-in.
contract AtomicRouteHarness {
    error BadProgram();
    error BadToken();
    error TransferFailed();
    error ApproveFailed();
    error Unprofitable(uint256 finalAmount, uint256 minFinalAmount);

    function execute(address inputToken, uint256 amountIn, uint256 minFinalAmount, bytes calldata program)
        external
        returns (uint256 finalAmount)
    {
        _safeTransferFrom(inputToken, msg.sender, address(this), amountIn);
        uint256 off;
        while (off < program.length) {
            if (program.length - off < 63) revert BadProgram();
            uint8 kind = uint8(program[off]);
            address target = _addressAt(program, off + 1);
            address tokenIn = _addressAt(program, off + 21);
            address tokenOut = _addressAt(program, off + 41);
            uint16 payloadLen = _u16(program, off + 61);
            uint256 payload = off + 63;
            if (payload + payloadLen > program.length) revert BadProgram();
            uint256 amount = IERC20Lite(tokenIn).balanceOf(address(this));
            if (amount == 0) revert BadToken();

            if (kind == 1) {
                if (payloadLen != 2) revert BadProgram();
                _swapV2(target, tokenIn, tokenOut, amount, _u16(program, payload));
            } else if (kind == 2) {
                if (payloadLen != 24) revert BadProgram();
                uint8 style = uint8(program[payload]);
                uint24 fee = _u24(program, payload + 1);
                uint160 limit = _u160(program, payload + 4);
                _approveMax(tokenIn, target, amount);
                if (style == 0) {
                    IV3Router02Lite(target).exactInputSingle(
                        IV3Router02Lite.ExactInputSingleParams(tokenIn, tokenOut, fee, address(this), amount, 0, limit)
                    );
                } else if (style == 1) {
                    IV3ClassicRouterLite(target).exactInputSingle(
                        IV3ClassicRouterLite.ExactInputSingleParams(tokenIn, tokenOut, fee, address(this), block.timestamp, amount, 0, limit)
                    );
                } else {
                    revert BadProgram();
                }
            } else if (kind == 3) {
                if (payloadLen != 32) revert BadProgram();
                uint128 i = _u128(program, payload);
                uint128 j = _u128(program, payload + 16);
                _approveMax(tokenIn, target, amount);
                (bool ok,) = target.call(abi.encodeWithSelector(ICurvePoolLite.exchange.selector, int128(i), int128(j), amount, 0));
                if (!ok) revert BadProgram();
            } else if (kind == 4) {
                if (payloadLen != 20) revert BadProgram();
                address pool = _addressAt(program, payload);
                _approveMax(tokenIn, target, amount);
                IBalancerV3RouterLite(target).swapSingleTokenExactIn(
                    pool, IERC20Lite(tokenIn), IERC20Lite(tokenOut), amount, 0, block.timestamp, false, ""
                );
            } else {
                revert BadProgram();
            }
            off = payload + payloadLen;
        }
        if (off != program.length) revert BadProgram();
        finalAmount = IERC20Lite(inputToken).balanceOf(address(this));
        if (finalAmount < minFinalAmount) revert Unprofitable(finalAmount, minFinalAmount);
        _safeTransfer(inputToken, msg.sender, finalAmount);
    }

    function _swapV2(address pair, address tokenIn, address tokenOut, uint256 amountIn, uint16 feeBps) internal {
        if (feeBps >= 10_000) revert BadProgram();
        IUniswapV2PairLite p = IUniswapV2PairLite(pair);
        address t0 = p.token0();
        address t1 = p.token1();
        if (!((tokenIn == t0 && tokenOut == t1) || (tokenIn == t1 && tokenOut == t0))) revert BadToken();
        (uint112 r0, uint112 r1,) = p.getReserves();
        uint256 reserveIn = tokenIn == t0 ? uint256(r0) : uint256(r1);
        uint256 reserveOut = tokenIn == t0 ? uint256(r1) : uint256(r0);
        uint256 amountInWithFee = amountIn * (10_000 - feeBps);
        uint256 amountOut = (amountInWithFee * reserveOut) / (reserveIn * 10_000 + amountInWithFee);
        _safeTransfer(tokenIn, pair, amountIn);
        p.swap(tokenOut == t0 ? amountOut : 0, tokenOut == t1 ? amountOut : 0, address(this), "");
    }

    function _approveMax(address token, address spender, uint256 needed) internal {
        _callOptionalBool(token, abi.encodeWithSelector(IERC20Lite.approve.selector, spender, 0), ApproveFailed.selector);
        _callOptionalBool(token, abi.encodeWithSelector(IERC20Lite.approve.selector, spender, needed), ApproveFailed.selector);
    }

    function _safeTransfer(address token, address to, uint256 amount) internal {
        _callOptionalBool(token, abi.encodeWithSignature("transfer(address,uint256)", to, amount), TransferFailed.selector);
    }

    function _safeTransferFrom(address token, address from, address to, uint256 amount) internal {
        _callOptionalBool(token, abi.encodeWithSignature("transferFrom(address,address,uint256)", from, to, amount), TransferFailed.selector);
    }

    function _callOptionalBool(address token, bytes memory data, bytes4 err) internal {
        (bool ok, bytes memory ret) = token.call(data);
        if (!ok || (ret.length != 0 && !abi.decode(ret, (bool)))) {
            assembly { mstore(0, err) revert(0, 4) }
        }
    }

    function _addressAt(bytes calldata b, uint256 off) internal pure returns (address a) {
        if (off + 20 > b.length) revert BadProgram();
        assembly { a := shr(96, calldataload(add(b.offset, off))) }
    }
    function _u16(bytes calldata b, uint256 off) internal pure returns (uint16 v) {
        if (off + 2 > b.length) revert BadProgram();
        assembly { v := shr(240, calldataload(add(b.offset, off))) }
    }
    function _u24(bytes calldata b, uint256 off) internal pure returns (uint24 v) {
        if (off + 3 > b.length) revert BadProgram();
        assembly { v := shr(232, calldataload(add(b.offset, off))) }
    }
    function _u128(bytes calldata b, uint256 off) internal pure returns (uint128 v) {
        if (off + 16 > b.length) revert BadProgram();
        assembly { v := shr(128, calldataload(add(b.offset, off))) }
    }
    function _u160(bytes calldata b, uint256 off) internal pure returns (uint160 v) {
        if (off + 20 > b.length) revert BadProgram();
        assembly { v := shr(96, calldataload(add(b.offset, off))) }
    }
}
