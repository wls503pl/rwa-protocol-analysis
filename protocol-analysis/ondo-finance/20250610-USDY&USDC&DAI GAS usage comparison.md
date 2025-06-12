# USDY Gas Consumption Analysis
**Initial version Date:** June 10, 2025
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

- Transfer from EOA to EOA

| # | Transaction Hash |   Type   | Gas Used |    Gas Price     |     Base Gas     |       ETH Cost       | Notes |
|---|------------------|----------|----------|------------------|------------------|----------------------|-------|
| 1 | 0x1d3ed7...66c4  | Transfer |  85,614  | 0.664942605 Gwei | 0.564942605 Gwei | 0.00005692839618447  | From 0x8C78a181...8Cc9dD74A To 0xb33820a3...e6743e615 For 262.065597254403563793($286.70) USDY |
| 2 | 0xa5fd7d...3173  | Transfer |  85,590  | 1.333275047 Gwei | 0.833275047 Gwei | 0.00011411501127273  | From 0x8f51B0F7...98a366bC9 To 0xa1f37db3...4432a977D For 3,010($3,292.94) USDY |
| 3 | 0x73db3a...3757  | Transfer |  90,402  | 1.11242621  Gwei | 1.01242621  Gwei | 0.00010056555423642  | From 0xcc7137d4...0E25A243B To 0x8F608e91...11155eb4A For 1.0047164479211521($1.10) USDY |
| 4 | 0xe82089...6558  | Transfer |  73,290  | 5.844575667 Gwei | 4.783395667 Gwei | 0.00042834895063443  | From 0x6C578079...5BaDbA8de To 0x596F8884...902e548cA For 4,577.166($5,007.42) USDY |
| 5 | 0x1cd7c2...af39  | Transfer |  90,390  | 0.867560582 Gwei | 0.367560582 Gwei | 0.00007841880100698  | From 0x29b795d5...A7747A4ec To 0x596F8884...902e548cA For 4,598.02($5,030.23) USDY |
| 6 | 0x2873fd...ab86  | Transfer |  85,590  | 0.377573614 Gwei | 0.327573614 Gwei | 0.00003231652562226  | From 0xB7f57799...26d8a9Bbb To 0x2AD7d18E...42cDd3dCB For 2,000($2,188.00) USDY |
| 7 | 0xaca73e...93ea  | Transfer |  73,302  | 0.664352207 Gwei | 0.590598432 Gwei | 0.000048698345477514 | From 0x4089CfBB...0BF9A438f To 0x1d819921...22D1aceaE For 43.020131($47.06) USDY |
| 8 | 0x6716d6...7d3c  | Transfer |  73,290  | 1.166868617 Gwei | 0.853449272 Gwei | 0.00008551980093993  | From 0x4089CfBB...0BF9A438f To 0x1d819921...22D1aceaE For 9.386826($10.27) USDY |
| 9 | 0xe69bab...d7df  | Transfer |  90,378  | 1.803354048 Gwei | 0.803354046 Gwei | 0.000162983532150144 | From 0x2de18235...20465CAAb To ENS Name element101.eth For 2($2.19) USDY |
| 10 | 0x76090c...8112 | Transfer |  85,578  | 3 Gwei           | 0.383447965 Gwei | 0.000256734          | From 0xa11eBBB8...80E6002A1 To 0x4660FDA9...c1398c12E For 5($5.47) USDY |
| 11 | 0xd267e4...49a9 | Transfer |  85,614  | 2.695556912 Gwei | 1.273986469 Gwei | 0.000230777409463968 | From 0x7B9dB594...e52FC000c To 0x35F5932d...6d1903f03 For 834.410990717099010254($912.85) USDY |
| 12 | 0xa94b6c...868e | Transfer |  85,614  | 0.828000006 Gwei | 0.328000006 Gwei | 0.000070888392513684 | From 0x296343Ca...8e3aCb2ae To 0x3855B152...724FefE80 For 3,448.625338999263835685($3,772.80) USDY |

- Internal operations of the Exchange

| # | Transaction Hash |   Type   | Gas Used |    Gas Price     |     Base Gas     |       ETH Cost       | Notes |
|---|------------------|----------|----------|------------------|------------------|----------------------|-------|
| 1 | 0x1c5b2d...927b  | Transfer |  68,502  | 3.872267938 Gwei | 1.872267938 Gwei | 0.000265258098288876 | From ByBit Dep: 0xAfA22a...D9076d To Bybit: Hot Wallet For 300,000($328,200.00) USDY |
| 2 | 0xec0158...c442  | Transfer |  68,526  | 2.854312219 Gwei | 0.854312219 Gwei | 0.000195594599119194 | From ByBit Dep: 0x0952A9...791b36 To Bybit: Hot Wallet For 49,054.079259873783827048($53,665.16) USDY |
| 3 | 0xf1cfa9...e5c9  | Transfer |  68,502  | 26.671674641 Gwei| 24.671674641 Gwei| 0.001827063056257782 | From ByBit Dep: 0x6dED5b...cA2f51 To Bybit: Hot Wallet For 500,200($546,718.60) USDY |
| 4 | 0x0bd10d...54d4  | Transfer |  68,514  | 3.094296612 Gwei | 1.094296612 Gwei | 0.000212002638074568 | From ByBit Dep: 0xAe2619...D3405C To Bybit: Hot Wallet For 1,100.471272771127224702($1,202.82) USDY |
| 5 | 0x8335a4...4288  | Transfer |  68,478  | 34.84437898 Gwei | 32.84437898 Gwei | 0.00238607338379244  | From ByBit Dep: 0x55681E...193B28 To Bybit: Hot Wallet For 10($10.93) USDY |
| 6 | 0xc6da06...2302  | Transfer |  85,602  | 33.348412638 Gwei| 31.348412638 Gwei| 0.002854690818638076 | From ByBit Dep: 0xB7D63d...291D8c To Bybit: Hot Wallet For 30,000($32,790.00) USDY |

- Deposit to the Exchange

| # | Transaction Hash |   Type   | Gas Used |    Gas Price     |     Base Gas     |       ETH Cost       | Notes |
|---|------------------|----------|----------|------------------|------------------|----------------------|-------|
| 1 | 0x3b040b...3062  | Transfer |  85,602  | 1.554237712 Gwei | 1.503312079 Gwei | 0.000133045856622624 | From ENS Name qpxquz.eth To ByBit Dep: 0xbD6775...68181F For 1,642.17253($1,794.89) USDY |
| 2 | 0xd59970...0bc3  | Transfer |  90,402  | 7.078027473 Gwei | 6.231579079 Gwei | 0.000639867839614146 | From ENS Name lphunter.eth To ByBit Dep: 0xAB2281...C5377F For 65,466.01($71,554.35) USDY |
| 3 | 0xe21a79...5052  | Transfer |  85,614  | 11.21 Gwei       | 11.162463927 Gwei| 0.00095973294        | From ENS Name jl1734.eth To 0x2aEdc26E...54879d5cD For 22.779032716302588543($24.90) USDY |
| 4 | 0x02b87b...cf7b  | Transfer |  85,614  | 17.958515242 Gwei| 17.864515242 Gwei| 0.001537500323928588 | From ENS Name 888.rektguy.eth To ByBit Dep: 0x26BA76...E09e77 For 35.158082027749753993($38.43) USDY |
| 5 | 0xc61c5c...5560  | Transfer |  85,614  | 3.81537874 Gwei  | 2.956644715 Gwei | 0.00032664983544636  | From ENS Name besttiger.eth To ByBit Dep: 0xe832A0...7F3fA3 For 1,000.749851584880924191($1,093.82) USDY |
| 6 | 0x834360...ce8f  | Transfer |  85,614  | 7.355193702 Gwei | 6.442520702 Gwei | 0.000629707553603028 | From ENS Name kenta7270.eth To ByBit Dep: 0x589330...d4010f For 30.15003589542307219($32.95) USDY |

- Withdraw from the Exchange

| # | Transaction Hash |   Type   | Gas Used |    Gas Price     |     Base Gas     |       ETH Cost       | Notes |
|---|------------------|----------|----------|------------------|------------------|----------------------|-------|
| 1 | 0x9f07b5...20b9  | Transfer |  90,414  | 4.856898115 Gwei | 2.856898115 Gwei | 0.00043913158616961  | Withdraw 8,657.61($9,462.77) USDY to 0x296b0843...dcf2484E4 from Bybit |
| 2 | 0xa4d99b...ef73  | Transfer |  90,414  | 6.191733651 Gwei | 4.191733651 Gwei | 0.000559819406321514 | Withdraw 8,589.36($9,388.17) USDY to 0x296b0843...dcf2484E4 from Bybit |
| 3 | 0xab7522...244f  | Transfer |  90,414  | 7.109629673 Gwei | 5.109629673 Gwei | 0.000642810057254622 | Withdraw 8,535.31($9,329.09) USDY to 0x296b0843...dcf2484E4 from Bybit |
| 4 | 0x6c8a05...cb84  | Transfer |  90,414  | 2.88723677 Gwei  | 0.88723677 Gwei  | 0.00026104662532278  | Withdraw 8,712.57($9,522.84) USDY to 0x296b0843...dcf2484E4 from Bybit |
| 5 | 0x475a8e...5938  | Transfer |  90,378  | 42.497469405 Gwei| 40.497469405 Gwei| 0.00384083628988509  | Withdraw 40.96($44.77) USDY to 0xa2cE4a7d...Bb9bc9660 from Bybit |
| 6 | 0x0f90a6...c2492 | Transfer |  90,390  | 18.501227416 Gwei| 16.501227416 Gwei| 0.00167232594613224  | Withdraw 6,853.21($7,490.55) USDY to 0x30CB2c51...A00e19Ab5 from Bybit |

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

