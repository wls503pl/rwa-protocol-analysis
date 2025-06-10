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

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0x1d3ed7...66c4  | Transfer |  85,614  | 0.664942605 Gwei | 0.00005692839618447  | Transfer 262.065597254403563793 ($285.65) USDY to 0xb33820...e615 |
| 2 | 0xb20a67...e107  | Transfer |  68,502  | 3.467435602 Gwei | 0.000237526273608204 | Transfer 1,642.17253($1,789.97) USDY to Bybit: Hot Wallet |
| 3 | 0x3b040b...3062  | Transfer |  85,602  | 1.554237712 Gwei | 0.000133045856622624 | Transfer 1,642.17253($1,789.97) USDY to ByBit Dep: 0xbD6775...181F |
| 4 | 0xcd9d92...50e5  | Transfer |  90,402  | 3.945220542 Gwei | 0.000356655827437884 | Withdraw 1,642.17253($1,789.97) USDY to qpxquz.eth from Bybit |
| 5 | 0xc2186f...3753  | Approve  |  53,639  | 1.606879685 Gwei | 0.000086191419423715 | Approve 98,702.229527415501662866 USDY for Trade on Ondo Finance: USDY Manager by mitschabaude.eth |

### USDC Transfer Data
**Source:** https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0xd791d1...7e04  | Transfer |  40,360  | 6.519307107 Gwei | 0.00026311923483852  | Transfer 100.023305($100.00) USDC to 0x7b0694...7007 |
| 2 | 0xda6a97...fb3a  | Transfer |  45,172  | 7.279038192 Gwei | 0.000328808713209024 | From Kraken 75 To 0xb8F717...B3ae For 5,342.542741($5,341.45)USDC |
| 3 | 0x33e823...ede0  | Transfer |  62,260  | 8.279038191 Gwei | 0.00051545291777166  | Withdraw 29.339847($29.33)USDC to 0x49BC01...69B7 from Binance |
| 4 | 0x2eafcc...5690  | Transfer From |  51,413  | 3.945220542 Gwei | 0.000443068841084815 | From 0xaeb5E4...Ea74 To Kraken 10 For 900,000($899,816.40) USDC |
| 5 | 0x43e184...12d5  | Approve  |  55,582  | 8.100705031 Gwei | 0.000450253387033042 | Approve 156,217.402068 USDC for Trade on Circle: Token Messenger by 0xE8c9C8...10Cc |

### DAI Transfer Data
**Source:** https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0x4abce5...87cf  | Transfer |  29,918  | 7.393790288 Gwei | 0.000221207417836384 | Transfer 201.13($201.03) DAI to 0xcb149D...4323 |
| 2 | 0x2cd0cf...15f5  | Transfer |  29,930  | 9 Gwei | 0.00026937 | From Binance Dep: 0x85b147...4392 To Binance 14 For 5,000($4,997.62) DAI |
| 3 | 0x3d119b...8a48  | Transfer |  51,830  | 10.188659699 Gwei | 0.00052807823219917 | From HTX 52 To ByBit Dep: 0x39AcF8...Db72 For 38,744.1657664($38,725.68) DAI |
| 4 | 0xd5c146...4c48  | Transfer From |  32,642  | 7.335632139 Gwei | 0.000239449704281238 | From 0x7b0B60...40ac To Kraken 12 For 10,000($9,995.23) DAI |
| 5 | 0x610933...afd4  | Approve  |  29,094  | 8.199504008 Gwei | 0.000238556369608752 | Approve 43,811.286880815689910187 DAI for Trade on DSProxy #213,086 by 0xa84a4E...a99C |

