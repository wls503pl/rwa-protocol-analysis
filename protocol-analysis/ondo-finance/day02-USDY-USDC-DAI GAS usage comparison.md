# Day 2: USDY Gas Consumption Analysis
**Date:** June 10, 2025  
**Focus:** USDY vs USDC vs DAI Transfer Gas

## 🎯 Research Objectives
- [ ] Quantifying USDY’s gas premium relative to standard stablecoins
- [ ] Identify specific sources of extra gas consumption for USDY
- [ ] Design targeted gas optimization solutions
- [ ] Estimate cost savings potential after optimization

## 📊 Token Contract Information

### Target Analysis: USDY (Ondo Finance)
**Address:** `0x96F6eF951840721AdBF46Ac996b59E0235CB985C`  
**Type:** Compliance-focused stablecoin  

### Baseline 1: USDC (Circle)
**Address:** `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`  
**Type:** Standard centralized stablecoin  

### Baseline 2: DAI (MakerDAO)
**Address:** `0x6B175474E89094C44Da98b954EedeAC495271d0F`  
**Type:** Decentralized stablecoin with additional logic  

## 📋 Data Collection Sample

### USDY Transfer Data
**Source:** https://etherscan.io/address/0x96F6eF951840721AdBF46Ac996b59E0235CB985C

- Transfer from EOA to EOA / Deposit to the Exchange

| # | Transaction Hash |   Type   | Block Num  | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|------------|----------|------------------|----------------------|-------|
| 1 | 0x1d3ed7...66c4  | Transfer |	 22655411  |  85,614  | 0.664942605 Gwei | 0.00005692839618447  | Transfer 262.065597254403563793 ($285.65) USDY to 0xb33820...e615 |
| 2 | 0xa5fd7d...3173  | Transfer |  22503811  |  85,590  | 1.333275047 Gwei | 0.00011411501127273  | From 0x8f51B0...6bC9 To 0xa1f37d...977D For 3,010($3,292.94) USDY |
| 3 | 0xe82089...6558  | Transfer |  22451919  |  73,290  | 5.844575667 Gwei | 0.00042834895063443  | Transfer 4,577.166($5,016.57) USDY to 0x596F88...48cA |
| 4 | 0x1cd7c2...af39  | Transfer |  22404566  |  90,390  | 0.867560582 Gwei | 0.00007841880100698  | From 0x29b795...A4ec To 0x596F88...48cA For 4,598.02($5,039.43) USDY |
| 5 | 0x7296fc...3617  | Transfer |  22399147  |  90,390  | 0.868842928 Gwei | 0.00007853471226192  | From 0x7d00EE...0B2a To ByBit Dep: 0x38D3a4...F3453F For 115.33202($126.40) USDY |
| 6 | 0x24e992...dc5b  | Transfer |  21383082  |  85,590  | 17.3577195 Gwei  | 0.001485647212005    | Transfer 423,747.82168($464,003.86) USDY to ByBit Dep: 0x9Df91f...e369 |

- Internal operations of the exchange / Withdraw from the Exchange

| # | Transaction Hash |   Type   | Block Num  | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|------------|----------|------------------|----------------------|-------|
| 1 | 0x1696c2...8faa  | Transfer |	 22465571  |  68,526  | 3.795716967 Gwei | 0.000260105300880642 | From ByBit Dep: 0x2572F6...b347 To Bybit: Hot Wallet For 36,237.218445318561862834($39,715.99) USDY |
| 2 | 0xedff47...2fdf  | Transfer |  22465337  |  68,526  | 2.945424146 Gwei | 0.000201838135028796 | From ByBit Dep: 0x2572F6...b347 To Bybit: Hot Wallet For 36,243.711946127277($39,723.11) USDY |
| 3 | 0xb06a1e...4e26  | Transfer |  22454413  |  68,514  | 6.643443827 Gwei | 0.000455168910363078 | From ByBit Dep: 0x2572F6...61b347 To Bybit: Hot Wallet For 35,972.5367($39,425.90) USDY |
| 4 | 0x2e8999...dd66  | Transfer |  21848888  |  68,514  | 2.719991104 Gwei | 0.000186357470499456 | From ByBit Dep: 0x985B31...F74C2c To Bybit: Hot Wallet For 487.138921939669226816($533.90) USDY |
| 5 | 0xea9427...8441  | Transfer |  21732033  |  90,402  | 5.522121889 Gwei | 0.000499210863009378 | From Bybit: Hot Wallet To Ondo Finance: USDY Token For 918.806936($1,007.01) USDY |
| 6 | 0x6a5648...0262  | Transfer |  21443977  |  73,302  | 30.531958832 Gwei| 0.002238053646303264 | Withdraw 500,000($547,500.00) USDY to Smart Account by Safe0x47D9D9...2E1E from Bybit |

- Approve method

| # | Transaction Hash |   Type   | Block Num  | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|------------|----------|------------------|----------------------|-------|
| 1 | 0xc2186f...3753  | Approve  |	 22651059  |  53,639  | 1.606879685 Gwei | 0.000086191419423715 | Approve 98,702.229527415501662866 USDY for Trade on Ondo Finance: USDY Manager by mitschabaude.eth |
| 2 | 0xf0520c...c46a  | Approve  |  22591375  |  54,253  | 2.207874995 Gwei | 0.000119011085855485 | Approve Unlimited USDY for Trade on 0xa62757...307D by 0xABb4F7...Ef3C |
| 3 | 0xb8cd0d...68e0  | Approve  |  22243813  |  53,627  | 1.021595802 Gwei | 0.000054785118073854 | Approve 69,999.999995 USDY for Trade on 0xa62757...307D by 0x1218Dc...600C |
| 4 | 0x5cbb9d...5c44  | Approve  |  22103357  |  33,619  | 0.4536775 Gwei   | 0.0000152521838725   | Revoke USDY for Trade on 0x201F6A...aE4b by 0x96ee57...BB19 |
| 5 | 0xdd0b9f...c8e0  | Approve  |  21708254  |  53,603  | 2.656918264 Gwei | 0.000142418789705192 | Approve 991 USDY for Trade on Aggregation Router V6 by 0xc4d3a5...66cC |
| 6 | 0x1722dd...986a  | Approve  |  21273201  |  36,491  | 16.111190157 Gwei| 0.000587913440019087 | Approve 5 USDY for Trade on 0xa62757...307D by 0x680fC6...06FF |

### USDC Transfer Data
**Source:** https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0xd791d1...7e04  | Transfer |  40,360  | 6.519307107 Gwei | 0.00026311923483852  | Transfer 100.023305($100.00) USDC to 0x7b0694...7007 |
| 2 | 0xda6a97...fb3a  | Transfer |  45,172  | 7.279038192 Gwei | 0.000328808713209024 | From Kraken 75 To 0xb8F717...B3ae For 5,342.542741($5,341.45)USDC |
| 3 | 0x33e823...ede0  | Transfer |  62,260  | 8.279038191 Gwei | 0.00051545291777166  | Withdraw 29.339847($29.33)USDC to 0x49BC01...69B7 from Binance |
| 4 | 0x2eafcc...5690  | Transfer From |  51,413  | 3.945220542 Gwei | 0.000443068841084815 | From 0xaeb5E4...Ea74 To Kraken 10 For 900,000($899,816.40) USDC |
| 5 | 0xea9427...8441  | Approve  |  55,582  | 8.100705031 Gwei | 0.000450253387033042 | Approve 156,217.402068 USDC for Trade on Circle: Token Messenger by 0xE8c9C8...10Cc |

### DAI Transfer Data
**Source:** https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0x4abce5...87cf  | Transfer |  29,918  | 7.393790288 Gwei | 0.000221207417836384 | Transfer 201.13($201.03) DAI to 0xcb149D...4323 |
| 2 | 0x2cd0cf...15f5  | Transfer |  29,930  | 9 Gwei | 0.00026937 | From Binance Dep: 0x85b147...4392 To Binance 14 For 5,000($4,997.62) DAI |
| 3 | 0x3d119b...8a48  | Transfer |  51,830  | 10.188659699 Gwei | 0.00052807823219917 | From HTX 52 To ByBit Dep: 0x39AcF8...Db72 For 38,744.1657664($38,725.68) DAI |
| 4 | 0xd5c146...4c48  | Transfer From |  32,642  | 7.335632139 Gwei | 0.000239449704281238 | From 0x7b0B60...40ac To Kraken 12 For 10,000($9,995.23) DAI |
| 5 | 0x610933...afd4  | Approve  |  29,094  | 8.199504008 Gwei | 0.000238556369608752 | Approve 43,811.286880815689910187 DAI for Trade on DSProxy #213,086 by 0xa84a4E...a99C |

