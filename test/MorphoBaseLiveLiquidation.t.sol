// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

struct MarketParams {
    address loanToken;
    address collateralToken;
    address oracle;
    address irm;
    uint256 lltv;
}

interface IMorphoBlue {
    function position(bytes32 id, address user) external view returns (uint256 supplyShares, uint128 borrowShares, uint128 collateral);
    function liquidate(MarketParams memory marketParams, address borrower, uint256 seizedAssets, uint256 repaidShares, bytes calldata data) external returns (uint256, uint256);
}

interface IWETH {
    function deposit() external payable;
    function approve(address spender, uint256 amount) external returns (bool);
    function balanceOf(address user) external view returns (uint256);
}

interface IERC20 {
    function balanceOf(address user) external view returns (uint256);
}

interface IOracle {
    function price() external view returns (uint256);
}

interface Vm {
    function createSelectFork(string calldata urlOrAlias) external returns (uint256 forkId);
    function deal(address account, uint256 newBalance) external;
}

contract MorphoBaseLiveLiquidationTest {
    Vm constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    address constant MORPHO = 0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb;
    address constant WETH = 0x4200000000000000000000000000000000000006;
    address constant WSTETH = 0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452;
    address constant ORACLE = 0xaE10cbdAa587646246c8253E4532A002EE4fa7A4;
    address constant IRM = 0x46415998764C29aB2a25CbeA6254146D50D22687;
    address constant BORROWER = 0x10c53e75fE7A7E6bF58a9e68B6a30Fcc7D4e6e2c;
    bytes32 constant MARKET_ID = 0x6aa81f51dfc955df598e18006deae56ce907ac02b0b5358705f1a28fcea23cc0;
    uint256 constant LLTV = 965000000000000000;

    event log_named_uint(string key, uint256 val);
    event log_named_address(string key, address val);

    receive() external payable {}

    function testLiveFullLiquidationOnLatestBaseFork() external {
        vm.createSelectFork("https://base-mainnet.g.alchemy.com/public");

        (uint256 supplyShares, uint128 borrowShares, uint128 collateralBeforePosition) =
            IMorphoBlue(MORPHO).position(MARKET_ID, BORROWER);
        supplyShares;

        emit log_named_uint("borrowSharesBefore", uint256(borrowShares));
        emit log_named_uint("borrowerCollateralBefore", uint256(collateralBeforePosition));
        require(borrowShares > 0, "borrower no longer has debt");
        require(collateralBeforePosition > 0, "borrower no longer has collateral");

        MarketParams memory p = MarketParams({
            loanToken: WETH,
            collateralToken: WSTETH,
            oracle: ORACLE,
            irm: IRM,
            lltv: LLTV
        });

        // Fund only inside the local fork. This never touches mainnet/Base state.
        vm.deal(address(this), 100 ether);
        IWETH(WETH).deposit{value: 50 ether}();
        require(IWETH(WETH).approve(MORPHO, type(uint256).max), "approve failed");

        uint256 wethBefore = IERC20(WETH).balanceOf(address(this));
        uint256 wstBefore = IERC20(WSTETH).balanceOf(address(this));
        uint256 oraclePrice = IOracle(ORACLE).price();

        (uint256 seizedAssets, uint256 repaidAssets) =
            IMorphoBlue(MORPHO).liquidate(p, BORROWER, 0, uint256(borrowShares), "");

        uint256 wethAfter = IERC20(WETH).balanceOf(address(this));
        uint256 wstAfter = IERC20(WSTETH).balanceOf(address(this));
        uint256 spentWeth = wethBefore - wethAfter;
        uint256 receivedWst = wstAfter - wstBefore;
        uint256 oracleValueWeth = receivedWst * oraclePrice / 1e36;
        uint256 grossBonusWeth = oracleValueWeth > spentWeth ? oracleValueWeth - spentWeth : 0;

        emit log_named_uint("oraclePrice", oraclePrice);
        emit log_named_uint("seizedAssets_wstETH", seizedAssets);
        emit log_named_uint("receivedWstETH", receivedWst);
        emit log_named_uint("repaidAssets_WETH", repaidAssets);
        emit log_named_uint("spentWETH", spentWeth);
        emit log_named_uint("oracleValueOfSeized_WETH", oracleValueWeth);
        emit log_named_uint("grossBonus_WETH", grossBonusWeth);

        require(seizedAssets == receivedWst, "seized/received mismatch");
        require(repaidAssets == spentWeth, "repaid/spent mismatch");
        require(grossBonusWeth > 0, "no gross liquidation bonus");

        (, uint128 borrowSharesAfter, uint128 collateralAfter) = IMorphoBlue(MORPHO).position(MARKET_ID, BORROWER);
        emit log_named_uint("borrowSharesAfter", uint256(borrowSharesAfter));
        emit log_named_uint("borrowerCollateralAfter", uint256(collateralAfter));
        require(borrowSharesAfter == 0, "full liquidation did not clear debt");
    }
}
