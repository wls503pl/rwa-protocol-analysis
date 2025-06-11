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

- Transfer method

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0x7a98fe...58f3  | Transfer |  45,148  | 1.878127825 Gwei | 0.0000847937150431   | From 0xd6a648...0EA8 To 0x798e3B...CB43 For 922.717514 ($922.51) USDC |
| 2 | 0x3a164f...d07e  | Transfer |  45,160  | 2.043151299 Gwei | 0.00009226871266284  | From Roobet: Hot Wallet To 0xefd74f...354e For 133.795458($133.77) USDC |
| 3 | 0x89a8d5...6dae  | Transfer |  62,260  | 3.811005502 Gwei | 0.00023727320255452  | Withdraw 109.756642($109.73) USDC to 0xdea8E4...fCbD from Binance |
| 4 | 0x592891...99ad  | Transfer |  40,348  | 1.656571629 Gwei | 0.000066839352086892 | Transfer 56($55.99) USDC to 0x74AA53...6828 |
| 5 | 0x636377...839a  | Transfer |  45,148  | 1.968417186 Gwei | 0.000088870099113528 | From Wirex 3 To 0x1126b3...4956 For 1,100($1,099.73) USDC |
| 6 | 0x933aa1...91cf  | Transfer |  40,360  | 1.687391023 Gwei | 0.00006810310168828  | From Uniswap: Fees 2 To Coinbase Prime For 20.971817($20.97) USDC |

- TransferFrom method

| # | Transaction Hash |      Type     | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|---------------|----------|------------------|----------------------|-------|
| 1 | 0xf27644...7b00  | Transfer From |  46,625  | 2.610285153 Gwei | 0.000121704545258625 | From 0x5637E8...6F52 To 0xA26148...b521 For 22.341896($22.34) USDC |
| 2 | 0x8ff738...c73d  | Transfer From |  46,613  | 4.067381 Gwei    | 0.000189592830553    | From 0x0412bF...E2a2 To Kraken 10 For 9,998.4($9,996.28) USDC |
| 3 | 0x717153...5f12  | Transfer From |  53,413  | 3.459925335 Gwei | 0.000184804991918355 | From 0x714F3f...8448 To 0xF0211d...317A For 3,714.01($3,713.22) USDC |
| 4 | 0xa88a22...04f6  | Transfer From |  46,601  | 9.411064348 Gwei | 0.000438565009681148 | From 0xc3025b...3253 To Kraken 10 For 3,706.4($3,705.61) USDC |
| 5 | 0x160c86...d7ea  | Transfer From |  46,625  | 7.308770034 Gwei | 0.00034077140283525  | From 0x8CA60A...c5e8 To Circle For 5,000,000($4,998,940.00) USDC |
| 6 | 0x95690a...277c  | Transfer From |  48,637  | 7.411069749 Gwei | 0.000360452199382113 | From 0x8f0eE0...86AE To 0x1751f2...68FF For 30,000,000 ($29,993,880.00) USDC |

- Approve/Mint method

| # | Transaction Hash |  Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|---------|----------|------------------|----------------------|-------|
| 1 | 0x81a372...e9b1  | Approve |  55,906  | 4.425491446 Gwei | 0.000247411524780076 | Approve Unlimited USDC for Trade on OKX: DEX Token Approval 1 by 0xE396eE...E36a |
| 2 | 0x870667...6840  | Approve |  55,558  | 3.638314286 Gwei | 0.000202137465101588 | Approve 20 USDC for Trade on Aave: Pool V3 by gusstavocrf.eth |
| 3 | 0x6e49c9...45ed  | Approve |  55,558  | 3.883926147 Gwei | 0.000215783168875026 | Approve 2 USDC for Trade on 0x6104fe...0cB6 by iacceptmoney.eth |
| 4 | 0x10215a...e559  | Approve |  55,558  | 3.673557168 Gwei | 0.000204095489139744 | Approve 2,200 USDC for Trade on Pendle: RouterV4 by 0x510165...44E7 |
| 5 | 0x99dfd8...c0e2  | Approve |  55,570  | 8.397311653 Gwei | 0.00046663860855721  | Approve 722.804167 USDC for Trade on 0xaaaaaa...3D4d by 0xdEBeC3...c196 |
| 6 | 0xb6b4aa...4f4a  |  Mint   |  55,636  | 7.226154642 Gwei | 0.000402034339662312 | From Null: 0x000...000 To Circle For 381,150.13 ($381,070.09) USDC |

### DAI Transfer Data
**Source:** https://etherscan.io/address/0x6B175474E89094C44Da98b954EedeAC495271d0F

- Transfer method

| # | Transaction Hash |   Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|----------|----------|------------------|----------------------|-------|
| 1 | 0x4c9269...e44d  | Transfer |  34,754  | 14.501803166 Gwei| 0.000503995667231164 | Transfer 22,961.57897182633($22,953.34) DAI to 0x2c48F1...b70a |
| 2 | 0x0e722a...4062  | Transfer |  51,830  | 3.959463165 Gwei | 0.00020521897584195  | Withdraw 161.68707($161.63) DAI to 0x68D5A5...C752 from Gate.io |
| 3 | 0x0fb458...8c30  | Transfer |  34,718  | 3.722950778 Gwei | 0.000129253405110604 | Withdraw 198.04($197.97) DAI to 0xF0e49e...e017 from Binance |
| 4 | 0x43f05c...7331  | Transfer |  29,918  | 3.809771974 Gwei | 0.000113980757918132 | From ByBit Dep: 0x1E984A...d76e To Bybit: Hot Wallet For 500($499.82) Dai Stableco... (DAI) |
| 5 | 0xaeff8d...d0d4  | Transfer |  29,930  | 0.413393328 Gwei | 0.00001237286230704  | From KuCoin Dep: 0x9672dd...E0a5 To KuCoin 20 For 115,281.67($115,237.40) DAI |
| 6 | 0x54559f...d142  | Transfer |  51,818  | 1.425420544 Gwei | 0.000073862441748992 | From ENS Name *アレクサンダー.eth To ByBit Dep: 0x5041DF...85bc For 2,494($2,493.04) DAI |

- TransferFrom method

| # | Transaction Hash |      Type     | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|---------------|----------|------------------|----------------------|-------|
| 1 | 0x15c4ff...cb1d  | Transfer From |  32,642  | 3.84018105 Gwei  | 0.0001253511898341   | From 0x0aC504...1586 To Kraken 12 For 500,000($499,653.00) DAI |
| 2 | 0x0c8b38...e834  | Transfer From |  37,442  | 3.424471872 Gwei | 0.000128219075831424 | From 0x62DAd9...B8B2 To Kraken 12 For 24,283.15($24,266.30) DAI |
| 3 | 0xa5b662...e936  | Transfer From |  32,630  | 1.643224199 Gwei | 0.00005361840561337  | From 0x36aFA2...80D5 To KuCoin 20 For 2,830($2,828.04) DAI |
| 4 | 0x018102...bdc5  | Transfer From |  32,642  | 3.30202141 Gwei  | 0.00010778458286522  | From 0x3954dD...21e1 To 0x1616b0...44A1 For 201.617($201.55) DAI |
| 5 | 0xd5fe7c...0b8d  | Transfer From |  37,442  | 12 Gwei Gwei     | 0.000449304          | From 0x027594...370D To CEX.IO For 34.895000509464666($34.88) DAI |
| 6 | 0xf7ff98...b7f0  | Transfer From |  32,630  | 16.065280113 Gwei| 0.00052421009008719  | From 0x3b1146...A45e To 0xa0bf73...C0b4 For 1,100.64($1,100.25) DAI |

- Approve method

| # | Transaction Hash |  Type   | Gas Used | Gas Price (gwei) |        ETH Cost      | Notes |
|---|------------------|---------|----------|------------------|----------------------|-------|
| 1 | 0x0c5258...1462  | Approve |  46,158  | 8.499846829 Gwei | 0.000392335929932982 | Approve 2,500 DAI for Trade on 0x38C541...9E0a by 0xdA4DD2...EFf7 |
| 2 | 0x61a93d...d8e7  | Approve |  46,458  | 8.896205749 Gwei | 0.000413299926687042 | Approve Unlimited DAI for Trade on Aggregation Router V6 by 0xCB981A...C9Cd |
| 3 | 0xef330e...5b91  | Approve |  26,558  | 5.245546837 Gwei | 0.000139311232897046 | Approve Unlimited DAI for Trade on Aave: Pool V3 by bfdn.eth |
| 4 | 0xc00912...1404  | Approve |  46,158  | 3.158353512 Gwei | 0.000145783281406896 | Approve 17.35955 DAI for Trade on Rango V2: Rango Diamond by 0x002D74...73A8 |
| 5 | 0x298a52...7790  | Approve |  24,174  | 3.478003679 Gwei | 0.000084077260936146 | Revoke DAI for Trade on Uniswap V3: Positions NFT by yuva.eth |
| 6 | 0x403d5d...fd85  | Approve |  46,170  | 0.925819704 Gwei | 0.00004274509573368  | Approve 513,000 DAI for Trade on Aggregation Router V6 by 0xb3251d...A727 |

