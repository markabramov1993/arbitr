// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/AtomicRouteHarness.sol";
import "../contracts/FlashArbExecutor.sol";

interface IERC20FlashRoute {
    function balanceOf(address account) external view returns (uint256);
}

interface VmFlashLocal {
    function createSelectFork(string calldata urlOrAlias) external returns (uint256 forkId);
    function snapshotState() external returns (uint256 snapshotId);
    function revertToState(uint256 snapshotId) external returns (bool success);
}

/// @notice Current-state Base fork gate for real Aave V3 flash-loan DEX routes.
/// @dev No private key and no public-chain broadcast. A route counts only if it
///      survives the real Aave premium and real router swaps on the latest fork.
contract BaseAaveFlashArbLiveTest {
    VmFlashLocal constant vm = VmFlashLocal(address(uint160(uint256(keccak256("hevm cheat code")))));

    event log_named_uint(string key, uint256 val);
    event log_named_int(string key, int256 val);
    event log_named_address(string key, address val);
    address constant AAVE_POOL = 0xA238Dd80C259a72e81d7e4664a9801593F98d1c5;
    address constant USDC = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913;
    address constant WETH = 0x4200000000000000000000000000000000000006;
    address constant CBBTC = 0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf;
    address constant UNI_ROUTER = 0x2626664c2603336E57B271c5C0b26F421741e481;
    address constant AERO_ROUTER = 0x698Cb2b6dd822994581fEa6eA4Fc755d1363A92F;

    string constant RPC = "https://base-rpc.publicnode.com";

    struct Candidate {
        address asset;
        int24 aeroTick;
        uint24 uniFee;
    }

    function testCurrentAaveFlashRouteMatrix() external {
        uint256 forkId = vm.createSelectFork(RPC);
        AtomicRouteHarness harness = new AtomicRouteHarness();
        FlashArbExecutor executor = new FlashArbExecutor(AAVE_POOL, address(harness), address(this));

        Candidate[4] memory routes = [
            Candidate(WETH, 10, 100),
            Candidate(WETH, 10, 500),
            Candidate(CBBTC, 50, 100),
            Candidate(CBBTC, 1, 100)
        ];
        uint256[6] memory sizes = [
            uint256(100e6),
            uint256(500e6),
            uint256(1_000e6),
            uint256(2_500e6),
            uint256(5_000e6),
            uint256(10_000e6)
        ];

        uint256 positives;
        emit log_named_uint("FLASH_FORK_ID", forkId);
        emit log_named_uint("FLASH_FORK_BLOCK", block.number);
        emit log_named_uint("FLASH_ROUTE_COUNT", routes.length);
        emit log_named_uint("FLASH_SIZE_COUNT", sizes.length);

        for (uint256 i; i < routes.length; ++i) {
            for (uint256 j; j < sizes.length; ++j) {
                uint256 snap = vm.snapshotState();
                uint256 gasBefore = gasleft();
                try executor.run(USDC, sizes[j], 1, _program(routes[i]), address(this)) returns (uint256 profit) {
                    uint256 gasUsed = gasBefore - gasleft();
                    if (profit > 0) {
                        ++positives;
                        emit log_named_uint("FLASH_POSITIVE_ROUTE", 1);
                        emit log_named_uint("FLASH_ROUTE_INDEX", i);
                        emit log_named_address("FLASH_ASSET", routes[i].asset);
                        emit log_named_int("FLASH_AERO_TICK", int256(routes[i].aeroTick));
                        emit log_named_uint("FLASH_UNI_FEE", routes[i].uniFee);
                        emit log_named_uint("FLASH_AMOUNT_USDC_RAW", sizes[j]);
                        emit log_named_uint("FLASH_NET_AFTER_PREMIUM_USDC_RAW", profit);
                        emit log_named_uint("FLASH_GAS_UNITS", gasUsed);
                    }
                } catch {}
                require(vm.revertToState(snap), "snapshot revert failed");
            }
        }

        emit log_named_uint("FLASH_PROFITABLE_COUNT", positives);
        emit log_named_uint("FLASH_OWNER_USDC_AFTER", IERC20FlashRoute(USDC).balanceOf(address(this)));
    }

    function _program(Candidate memory c) internal pure returns (bytes memory) {
        bytes memory aeroPayload = abi.encodePacked(bytes3(uint24(c.aeroTick)));
        bytes memory aero = abi.encodePacked(
            uint8(5),
            AERO_ROUTER,
            USDC,
            c.asset,
            uint16(aeroPayload.length),
            aeroPayload
        );

        bytes memory uniPayload = abi.encodePacked(
            uint8(0),
            bytes3(c.uniFee),
            bytes20(uint160(0))
        );
        bytes memory uni = abi.encodePacked(
            uint8(2),
            UNI_ROUTER,
            c.asset,
            USDC,
            uint16(uniPayload.length),
            uniPayload
        );

        return bytes.concat(aero, uni);
    }
}
