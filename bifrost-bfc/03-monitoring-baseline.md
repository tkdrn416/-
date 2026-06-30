# Bifrost (BFC) 모니터링 베이스라인 + 루프 플레이북

> 작성/스냅샷 기준: **2026-06-29** · 목적: 반복 루프가 "변동/주목할 변화"를 감지하기 위한 **기준값(baseline)** + **매 루프 재실행 쿼리/디프 대상** 정의
> 대상: **한국 파이랩테크놀로지 Bifrost Network, BFC** (Polkadot BNC 아님)
> 사용법: 매 루프마다 아래 각 차원의 "재실행"을 돌려 "기준값"과 diff → 차이 발생 시에만 보고. 변화 시 이 문서의 기준값을 갱신.

## ⚠️ 혼동 방지 (루프마다 필수 필터)
- 우리 대상: `bifrostnetwork.com`, `thebifrost.io`, `medium.com/bifrost`, `medium.com/bifrost-blog-kor`, GitHub `bifrost-platform`, X `@Bifrost_Network`, BFC ERC-20 `0x0c7D5ae0...Cab9c`, 메인넷 chainId **3068**.
- ❌ 제외(=Polkadot BNC): `bifrost.io`, `bifrost.io/blog`, `app.bifrost.io`, GitHub `bifrost-io`/`bifrost-finance`, vDOT/vKSM/SLP/parachain/Kusama 관련.
- ⚠️ **CoinMarketCap "CMC AI latest updates" 페이지는 BNC와 BFC를 섞음** (예: "100만 DOT 트레저리 상환" = BNC). 날짜 참고용으로만 쓰고 DOT/Polkadot 항목은 버릴 것.

---

# 차원 1 — 상위 어카운트(홀더) 변동 ★네이티브 메인넷(3068) 우선★

> 메인넷 전환 후 **실제 보유·유통은 네이티브 체인(3068)이 핵심.** ETH ERC-20은 브릿지/원장용으로 보조.

## 1-A. 네이티브 메인넷 리치리스트 (주력)
**재실행:** `GET https://explorer-backend.mainnet.thebifrost.io/api/v2/addresses` (잔액 내림차순)

**기준값 (2026-06-30):** 네이티브 주소 ~6,028만 · TOP25 라벨 포함

| # | 주소 | 잔액(BFC) | 라벨/식별 |
|---|---|---:|---|
| 1 | `0x50F187Ef4447dA6e5Ff1D740439e91175BAC955E` | 332,484,206 | **업비트 콜드허브** |
| 2 | `0xDCd52f5f5aF5022edEfD59fD5353f4DA3f2C8935` | 137,482,292 | **빗썸 콜드허브** |
| 3 | `0x4bAE7ba39E4e71660307dcE780f1Ec9b7B7666Ee` | 87,424,912 | 미식별 콜드(유출0 축적) |
| 4 | `0xAe172D8c5E428D4b7C70f9E593b207F9daC9BF3e` | 40,342,392 | **Unified BFC 컨트랙트** |
| 5 | `0x5EeFFDbCDf6d269AE249e445b95BfFaDC0673cc7` | 16,494,730 | 미식별 |
| 6 | `0x081a4ee55739F0DA8abB8af40D07687527a268c3` | 15,377,787 | **업비트 핫** |
| 7 | `0xb68a0A0121be78f25A7d147394D90C35F2e34C5d` | 14,017,724 | 미식별 |
| 8 | `0xf6ac30649a26130E2D1c6875E935a1FA67Cee76c` | 14,001,000 | 미식별 |
| 9 | `0x5dEc180f0D414B4f3606e759c408A6B3561b1b2e` | 11,810,189 | 미식별 |
| 10 | `0xd7C451b4A52DAFd95be3302d05eE70d097139A87` | 11,000,500 | 미식별 |
| … | (11~25위 ~6.6M~10M) | | 다수 미식별 |
| 19 | `0x6d6f646C70792f74727372790000000000000000` | 7,538,155 | **Treasury 국고**(modlpy/trsry) |
| 21 | `0xffFaAC4Ea0972C21c2834a0410A0582e4AbfF741` | 6,845,339 | 검증자 stash |
| 22 | `0x330d76197a25721357e05368179EbA8d0be9Be0e` | 6,777,852 | 검증자 stash |
| 25 | `0x355b784757473741133911042bcD215B3d8EE289` | 6,666,148 | 검증자 stash |

**디프 대상:** 거래소 콜드허브(#1 업비트·#2 빗썸) 잔액 급변(=순유입/출), top25 신규 진입·이탈, **Treasury(#19) 변동**(국고 집행), 미식별 대형(#3 87M·#5 16M) 이동.

> 📊 **상위 홀더 흐름 분석 → [data/native-holders-analysis.md](./data/native-holders-analysis.md)**: #3(87M)=미검증 수신전용 리저브성 컨트랙트, 중간티어(#5·8·10·11·12)=휴면 배분/OTC 지갑, 추가로 네이티브 **DEX 라우터** `0x7Ace89E2…`(Uniswap V2형, 85,612 tx) 식별. 거래소 2곳이 네이티브 상위 470M 집중.

## 1-B. ETH ERC-20 홀더 (보조 — 브릿지/원장)
**재실행:** `https://api.ethplorer.io/getTopTokenHolders/0x0c7D5ae0…Cab9c?apiKey=freekey&limit=30` · holdersCount는 getTokenInfo
- 기준값(2026-06-29): 홀더 **3,619명**. 상위: `0x…dead` 소각 40.8%, ETH Vault `0x2f95c102…` 21.6%, 컨트랙트 `0x4d5aa298…` 11.5%
- **디프:** Vault·소각 주소 잔액 변화(토크노믹스/브릿지), holdersCount 변동

---

# 차원 2 — 노드/검증자 변화 [네이티브 체인 3068]

**재실행:** `POST https://public-01.mainnet.bifrostnetwork.com/rpc` · `eth_call` to BfcStaking 프리컴파일 `0x0000000000000000000000000000000000000400`
```bash
# 검증자 분포 (Full=15 기대): selected_candidates(2)
curl -s -X POST https://public-01.mainnet.bifrostnetwork.com/rpc -H "Content-Type: application/json" \
 -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0x0000000000000000000000000000000000000400","data":"0xa5542eea0000000000000000000000000000000000000000000000000000000000000002"},"latest"]}'
# 후보수: candidate_count() = 0x4b1c4c29   | 라운드: round_info() = 0xf8aa8ddd
```

**기준값 (2026-06-29, 블록 36,200,231):**
| 항목 | 값 |
|---|---|
| 라운드 | 2524 |
| 후보 총수 | **24** |
| 선출 검증자 전체 / Basic / Full | **24 / 9 / 15** |
| 총 스테이킹(self+위임) | **≈ 406,078,451 BFC** (self ≈60.9M + 위임 ≈345.2M) |
| 스테이킹 비율 | ≈ 29.3% (유통 대비) |
| 위임자 카운트 | 27,387 |

**기명 검증자(공지, 주소 비공개):** BitTrade(일본거래소, 2024-11-29) · AI Fusion Capital(도쿄 상장사, 2025-06-30) · KICA 한국정보인증(2023-01-29) · DeSpread(2022-12-23). ⚠️ Bifrost는 Substrate라 **온체인 identity 필드가 없어 실명↔주소 1:1 매핑은 원천 불가** — 익스플로러/Blockscout 모두 name·tag null.

**검증자 24개 온체인 주소(controller):** 전체 목록은 [validators-snapshot.md](./data/validators-snapshot.md) 참조. 디프는 이 주소집합 기준.

**디프 대상:** 후보수(24)·Basic(9)·Full(15) 분포 변화, 총 스테이킹 ±, **검증자 주소집합 신규/이탈**(data/validators-snapshot.md와 대조), 신규 검증자 공지(medium.com/bifrost).

---

# 차원 3 — 브릿지 변화

**재실행:**
- BSC Socket: `WebFetch https://bscscan.com/address/0xb5Fa48E8B9b89760a9f9176388D1B64A8D4968dF` → "total of N transactions"
- ETH Socket: `curl https://eth.blockscout.com/api/v2/addresses/0x4A31FfeAc276CC5e508cAC0568d932d398C4DD84/counters` → `transactions_count`
- 지원 체인/자산: `bifrostnetwork.com/bridge` 드롭다운
- CCCP v2: `https://github.com/bifrost-platform/bifrost-relayer.rs/releases`

**기준값 (2026-06-29):**
| 지표 | 값 |
|---|---|
| BSC Socket 누적 txn | **17,532** (당일 활성) |
| ETH Socket 누적 txn | **10,132** (당일 활성, EIP-1967 프록시) |
| 지원 체인 | 9개 (Bifrost/BTC/ETH/Base/Arbitrum/Core/BSC/Polygon/Oasys) |
| 지원 자산 | BFC, BiFi, ETH, USDC, USDT, WBTC |
| CCCP v2 / Hook | relayer v3.0.0 메인넷 배포, **Hook 기능은 아직 testnet 전용** (메인넷 `CCCPRelayQueue` 포함 시 활성) |

**디프 대상:** Socket txn 카운트 델타(브릿지 사용량), 신규 체인/자산 등재, **CCCP v2 메인넷 전환 여부**(주목 이벤트).

## 브릿지 Vault 락업자산(TVL) 베이스라인 (2026-06-29) — 신규
브릿지 실제 락업액. 각 체인 Vault 주소(02 B-1)의 보유자산 = 브릿지 TVL 대리지표.

**ETH Vault `0x2F95C102Cc26875406BC689Fb01aE382B82AA535`** (ethplorer getAddressInfo):
| 자산 | 수량 | ≈USD |
|---|---:|---:|
| BFC | 863,522,304 | ~$10.2M |
| USDC | 607,025 | ~$607K |
| BIFI | 136,968,328 | ~$232K |
| WBTC | 0.13 | ~$7.5K |
| USDT | 4,302 | ~$4.3K |
| **JPYC** | **3,989** | ~$24 (소액이나 JPYC 브릿지 존재 확인) |
| ETH | 193.3 | — |

**BSC Vault `0x78ae4c0FD4f02CA79A2d8738d3369A4Bc5D4E323`** (BSC RPC `eth_call balanceOf`):
| 자산 | 수량 |
|---|---:|
| BTCB | **44.3** (~$4.7M) |
| BNB | 115.2 |

**Bifrost 네이티브 Vault `0xD85EB87caB9041ad00764b95796702b1104F42D7`:** 75.6 BFC (아웃바운드용, 잔액 낮음 정상)

- **재실행:** ETH=`api.ethplorer.io/getAddressInfo/0x2F95C102…?apiKey=freekey` · BSC=`bsc-dataseed.bnbchain.org` `eth_call`(BTCB balanceOf vault) · 네이티브=explorer-backend
- **디프 대상:** Vault별 자산 수량 델타(브릿지 순유입/출), 특히 BFC·USDC·BTCB·**JPYC** 증감.

## BTCFi 핵심지표 — BtcUSD 발행량 (신규, 핵심 성장지표)
BtcUSD = BTCFi의 BTC담보 스테이블코인. **발행량 = BTCFi 사업 규모의 직접 지표.**

| 항목 | 값 (2026-06-30, 라이브 검증) |
|---|---|
| **BtcUSD totalSupply** | **8,061,957 BtcUSD** |
| 컨트랙트 (Bifrost 3068) | `0x6906Ccda405926FC3f04240187dd4fAd5DF6d555` |
| 멀티체인 | BSC `0x4F2c996248ED9592e64B59f781A15dEB1e2b0D4c` · Base `0xe4b20925D9E9a62F1E492e15a81dC0de62804dd4` · Core `0xad0c524Ce19ceA03654Dc377da7Bac52C56eDd10` · Oasys `0x4Cda2D683E3AF90ea50855008BdB15D9454527B7` |
| BTCFi TVL (DefiLlama) | ≈$2.68M |

- **재실행:** `eth_call` totalSupply(`0x18160ddd`) to BtcUSD on `public-01.mainnet.bifrostnetwork.com/rpc` + `api.llama.fi/protocol/btcfi`
```bash
curl -s -X POST https://public-01.mainnet.bifrostnetwork.com/rpc -H "Content-Type: application/json" \
 -d '{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0x6906Ccda405926FC3f04240187dd4fAd5DF6d555","data":"0x18160ddd"},"latest"]}'
```
- **디프 대상:** BtcUSD 발행량 증감(BTCFi 성장/수축), BTCFi TVL 델타. **발행량 급증 = HashPort/N.suite 등 일본 렌딩 수요 유입 신호와 교차검증 가능.**

---

# 차원 4 — 트랜잭션 변화 ★네이티브 메인넷(3068) 우선★

> 실제 온체인 활동은 네이티브 체인이 압도적(누적 tx 7,747만 vs ETH ERC-20 5.6만). 네이티브를 주력으로.

## 4-A. 네이티브 메인넷 활동 (주력)
**재실행:** `GET https://explorer-backend.mainnet.thebifrost.io/api/v2/stats`

**기준값 (2026-06-30):**
| 지표 | 값 |
|---|---|
| **누적 트랜잭션** | **77,476,593** |
| **당일 트랜잭션** | **~17,051** (tx_today) |
| 누적 블록 | 36,330,250 (블록타임 ~3s) |
| 누적 주소 | 60,285,254 |
| coin_price | $0.011745 |

- **대형 전송 감시:** 거래소 콜드허브/Treasury 출입금은 `GET /api/v2/addresses/{addr}/transactions?filter=to|from` 으로 value 큰 건 추적 (특히 #1 업비트·#2 빗썸·#19 Treasury).
- **디프 대상:** **당일 tx 수 급변**(활동 스파이크/둔화), 누적 tx·주소 증가율, 대형 네이티브 전송.

## 4-B. ETH ERC-20 활동 (보조)
**재실행:** `api.ethplorer.io/getTokenInfo/0x0c7D5ae0…?apiKey=freekey`(카운터) + `getTokenHistory…&limit=100&type=transfer`(대형전송)
- 기준값(2026-06-29): transfersCount **111,008** · txsCount **56,044** · price $0.0118 · vol24h $2.41M(급증구간) · rank ~901
- **디프:** transfersCount/txsCount 델타, vol24h 2~3배↑, value≥1M BFC 전송(to/from = dead·Vault)
- 시세 보조: `api.coingecko.com/api/v3/coins/ethereum/contract/0x0c7D5ae0…Cab9c`

---

# 차원 5 — GitHub 변경 [bifrost-platform]

**재실행 (API 권장 — 웹페이지는 연도 오인):**
```bash
curl -s "https://api.github.com/repos/bifrost-platform/bifrost-node/commits/main" | jq -r '.sha[:10]+" "+.commit.author.date'
curl -s "https://api.github.com/repos/bifrost-platform/bifrost-relayer.rs/commits/main" | jq -r '.sha[:10]+" "+.commit.author.date'
curl -s "https://api.github.com/repos/bifrost-platform/asset-info-v2/commits/main" | jq -r '.sha[:10]+" "+.commit.author.date'
curl -s "https://api.github.com/repos/bifrost-platform/bifrost-node/releases?per_page=1" | jq -r '.[0].tag_name'
curl -s "https://api.github.com/repos/bifrost-platform/bifrost-relayer.rs/releases?per_page=1" | jq -r '.[0].tag_name'
curl -s "https://api.github.com/orgs/bifrost-platform" | jq .public_repos
curl -s "https://api.github.com/orgs/bifrost-platform/repos?sort=created&direction=desc&per_page=3" | jq -r '.[]|.name+" "+.created_at'
```

**기준값 (2026-06-29):**
| 레포 | 최신 릴리스 | 최신 커밋 SHA · 날짜 | Open PR | ★/fork |
|---|---|---|---|---|
| bifrost-node | **v2.2.0** (2026-06-24) | `e0f08aa36f` · 2026-06-25 | 2 | 39/16 |
| bifrost-relayer.rs | **v3.0.0** (2026-06-24) | `f9c44ffe6c` · 2026-06-26 | 2 | 12/6 |
| asset-info-v2 (미러) | v3.0.7 (2026-03-18) | `44f6c3b69d` · 2026-03-18 | — | — |
| bifrost-frontier (fork) | — | 2025-08-31 | — | — |
| bifrost-substrate (fork, 정지) | — | **2023-07-04** | — | — |

- 조직 총 공개 레포: **34** · 최신 신규 레포: **`common`** (2025-12-10)
- 주 기여자: `dnjscksdn98`(node/relayer), 과거 `jormal`(asset)

**디프 대상:** 각 레포 최신 커밋 SHA·릴리스 태그 변경, Open PR 수, **신규 레포**(common보다 새 생성일), 총 레포수(34) 변화, **asset-info-v2 자산 폴더 추가**(신규 토큰/체인 등재 신호), substrate fork 재가동(=주목).

---

# 차원 6 — 인터넷 뉴스

**뉴스 워터마크 (기준):** **2026-06-02** — "Bifrost BTCFi × HashPort Wallet 통합, JPYC 연 ~4% 렌딩" (JinaCoin) — https://jinacoin.ne.jp/jpyc-bifrost-hashport-20260602/
→ **이 날짜보다 새로운 BFC 직접 항목이 나오면 "신규"**.
- **리프레시 (2026-06-30 확인):** 6/3~6/30 기간 **신규 공식 발표/파트너십/상장 없음**. 단 시세 기사 1건 — **2026-06-04 BFC 빗썸서 +30% 급등(상승률 1위, 거래량 ~5배)**, 뚜렷한 호재 없는 단기 매수세 ([news1](https://www.news1.kr/finance/blockchain-fintech/6187719)). 공식 발표 아님 → 워터마크 유지.

**재실행 소스 (우선순위):**
1. `https://medium.com/bifrost-blog-kor` (한국 공식, 가장 활발)
2. `https://medium.com/bifrost` · `https://bifrost.medium.com` (영문 공식)
3. `https://t.me/s/Bifrost_Notice` (텔레그램 공지 — 본문/날짜 렌더됨)
4. `https://bifrostnetwork.com/`
5. 검색: `Bifrost BFC BTCFi 2026 비프로스트`, `바이프로스트 BTCFi`, `site:tokenpost.kr Bifrost`, `ハッシュポート Bifrost JPYC`, `site:neweconomy.jp Bifrost`, `site:jinacoin.ne.jp Bifrost`, `Bifrost BFC 업비트 빗썸 상장`
6. 월 진행형 스윕: `Bifrost BTCFi July 2026` (매 루프 월 갱신)

**디프 대상:** 워터마크(2026-06-02) 이후 날짜의 신규 헤드라인. ❌ `bifrost.io/blog`·DOT/Polkadot·CMC AI의 BNC 항목 제외.

---

# 차원 7 — 일본 파트너사 / BFC 협업 서비스 추적

**기준 현황 (2026-06-29) — 모든 파트너십이 발표/논의/검증 단계, 공개 TVL·도입수치 없음. 가장 최근 = HashPort(2026-06-01).**

| 파트너/서비스 | 현재 상태 | 최신일 | 재확인 URL | 감시 신호(diff) |
|---|---|---|---|---|
| **HashPort Wallet × JPYC 4% 렌딩** | 가동(연 4% 무만기). Summer 캠페인 예고만, **TVL 미공개** | 2026-06-01 | jinacoin.ne.jp, neweconomy.jp, wallet.hashport.com/news | **첫 TVL/유입 수치**, 캠페인 금리·결과 |
| **DJT N.suite Treasury Access Plan** | 출시(JPYC 렌딩 1단계). 파일럿 고객명 미공개 | 2026-05-20 | doublejump.tokyo/news, nadanews.com | 고객사명, USDC 확대, 도입건수 |
| **SBI Digital Finance** | "개발 논의" 단계, 2026 진전 미확인 | 2025-08-13 | bifrost.medium.com, BeInCrypto | 정식계약/PoC, 기관 고객 |
| **Animoca Brands Japan** | 기본합의(검증). 제품출시 미확인 | 2025-12-16 | animocabrands.co.jp, prtimes.jp | 상장사 트레저리 실배포, 고객명 |
| **MOIN × JOC × Bifrost** | MOU. 이후 진척 미확인 | 2026-02-05 | gu-group.com/news, themoin.com | 송금 코리도어 런칭, 거래량 |
| **AI Fusion Capital / BitTrade** | 검증자 운영. 2026 업데이트·**BFC 상장 미확인** | 2024-11-29 | bittrade.co.jp/information, aifcg.jp | **BFC BitTrade 상장**(대형 촉매), 검증자 추가 |
| **JPYC 발행량** | 누적 **30억엔 돌파**, 계좌 19,000 | 2026-05-30 | corporate.jpyc.co.jp/news | 다음 마일스톤(50억/100억엔), 계좌수 |
| **신규 일본 파트너** | 2026-06-01 이후 신규 없음 | — | medium.com/bifrost, jinacoin/coinpost 검색 | 2026-06-01 이후 신규 일본 기업/거래소 |

> **최우선 감시 2건:** (a) HashPort/N.suite JPYC 렌딩 **첫 TVL 수치**, (b) **BFC의 BitTrade 상장**. 둘 다 나오면 즉시 보고.

---

# 차원 8 (추가) — 한국 거래소(업비트/빗썸) BFC 보유량 ★확정★

**★ 핵심:** 거래소 BFC는 **이더리움 ERC-20이 아니라 네이티브 Bifrost 메인넷(3068)**에 있음. 사용자 제보(업비트 출금 이력) + 빗썸 앱 공시값과의 온체인 교차검증으로 **두 거래소 클러스터를 확정**함.

## 백엔드 API (확보 완료)
- 익스플로러 백엔드(Blockscout): **`https://explorer-backend.mainnet.thebifrost.io`** (프론트 SPA 우회용)
- 리치리스트 `GET /api/v2/addresses` · 잔액 `GET /api/v2/addresses/{addr}` · 카운터 `GET /api/v2/addresses/{addr}/counters` · 입출금 `GET /api/v2/addresses/{addr}/transactions?filter=to|from` · 통계 `GET /api/v2/stats`

## 🟢 업비트(Upbit) 클러스터 — [확인됨, 높은 신뢰도]
근거: 사용자가 "업비트에서 주로 출금"한 지갑(`0xaDF77D87…55e43`)에 입금한 주소 5개가 모두 아래 콜드허브(`0x50F187Ef`)에서 자금을 공급받음.

| 역할 | 주소 | 잔액(2026-06-29) |
|---|---|---:|
| **콜드/분배 허브** | `0x50F187Ef4447dA6e5Ff1D740439e91175BAC955E` | **332,484,206** |
| 핫(유저 직접출금 7회) | `0x081a4ee55739F0DA8abB8af40D07687527a268c3` | 15,377,787 |
| 핫(콜드서 111.6M 수령) | `0x0056a1438fDDb84a2f40A696Cb38D3B717CD3D0e` | 0 (순환) |
| 핫 | `0x6C9b71C49FA61e176F99ab6297dfc12De70a4E85` | 0 (순환) |
| 핫 | `0x97e9b4C0e8275aC8F549A72C73bD92598DFe1645` | 0 (순환) |
| | **업비트 합계** | **≈ 347.9M BFC** (최대 보유 거래소) |

## 🟢 빗썸(Bithumb) 클러스터 — [확인됨, 공시값과 일치]
근거: 빗썸 앱 "내부 유통량" **143,666,510 BFC** ≈ 아래 콜드+핫 온체인 합계 **143.8M** (거의 정확히 일치). 업비트 클러스터와 거래 겹침 없음.

| 역할 | 주소 | 잔액(2026-06-29) |
|---|---|---:|
| **콜드/허브** | `0xDCd52f5f5aF5022edEfD59fD5353f4DA3f2C8935` | **137,482,292** |
| 핫(콜드서 117.6M 수령, 2,920tx) | `0x39528D59132920Ab0a637129D90CF9fB3650084D` | 6,264,119 |
| | **빗썸 합계** | **≈ 143.7M BFC** (= 공시 143,666,510 ✓) |

> 빗썸 앱 공시(거래소정보 탭) 추가 지표: BFC 보유자 **45,296명**, 순입금(24H), 전일대비 유통량(%), 최상위회원 보유/거래 비중. 앱/웹(`bithumb.com` BFC 정보)에서 확인. (웹은 JS 렌더라 자동 수집 시 백엔드 JSON 탐색 필요)

## 미식별 대형 주소 (거래소 아님으로 추정 / 추적만)
- `0x4bAE7ba39E4e71660307dcE780f1Ec9b7B7666Ee` (87.4M) · `0x09FCED81…4470E` (4.4M) — 클러스터 미연결, 운영/마켓메이커 가능성
- `0xAe172D8c5E428D4b7C70f9E593b207F9daC9BF3e` (40.3M) = **Unified BFC 컨트랙트**(거래소 아님)

## 루프 비교 방법
```bash
API=https://explorer-backend.mainnet.thebifrost.io
# 업비트 보유 (콜드+핫 합)
for a in 0x50F187Ef4447dA6e5Ff1D740439e91175BAC955E 0x081a4ee55739F0DA8abB8af40D07687527a268c3 \
         0x0056a1438fDDb84a2f40A696Cb38D3B717CD3D0e 0x6C9b71C49FA61e176F99ab6297dfc12De70a4E85 \
         0x97e9b4C0e8275aC8F549A72C73bD92598DFe1645; do curl -s $API/api/v2/addresses/$a | jq .coin_balance; done
# 빗썸 보유 (콜드+핫 합)
for a in 0xDCd52f5f5aF5022edEfD59fD5353f4DA3f2C8935 0x39528D59132920Ab0a637129D90CF9fB3650084D; do
  curl -s $API/api/v2/addresses/$a | jq .coin_balance; done
```
- **디프 대상:** 각 클러스터 합계 잔액 일별 델타 = **거래소 순유입(+, 매도압력)/순유출(−)** 프록시. 빗썸은 앱 공시값(143.6M)과 온체인 합 대조로 자가검증.
- **신규 핫월렛 출현 감시:** 콜드허브(0x50F187/0xDCd52f5f)의 outgoing 신규 수신주소 → 새 거래소 핫월렛일 수 있음(클러스터 확장).
- **재검증 팁:** 거래소가 지갑을 바꾸면 클러스터가 깨질 수 있음 → 빗썸은 공시값과 온체인 합이 벌어지면, 업비트는 콜드허브 outgoing 패턴 변화로 감지.

## 거래소 공개 API & 빗썸 공시 자동수집 (검증 완료, 2026-06-29)
**빗썸 "내부 유통량" 공시(앱 `m.bithumb.com/react/trade/info/BFC-KRW`):**
- 정확값(내부유통량 143,666,510 · 보유자 45,296명 · 순입금24H)을 주는 엔드포인트 `gw.bithumb.com/exchange/v1/.../coin/info`는 **회원 로그인 필요(`member.fail.00012`) + Akamai 봇차단(`_abck`,`bm_sz`)** → **인증 없이 자동수집 불가**(사용자 계정 자동화는 지양). 헤드리스 브라우저도 프록시 정책상 차단됨.
- **대체(자동수집 가능):** 온체인 빗썸 클러스터 합(0xDCd52f5f + 0x39528D59) ≈ 내부유통량. 위 스크립트로 키 없이 수집 → 공시값의 신뢰 프록시.

**거래소 공개 시세/상태 API (인증 불필요, 자동수집 OK):**
| 용도 | 엔드포인트 | 베이스라인(2026-06-29) |
|---|---|---|
| 빗썸 시세/거래대금 | `https://api.bithumb.com/public/ticker/BFC_KRW` | 종가 17.74원, 24h거래대금 ≈₩2.08억 |
| 빗썸 입출금 상태 | `https://api.bithumb.com/public/assetsstatus/BFC_KRW` | deposit=1, withdrawal=1 (정상) |
| 업비트 시세 | `https://api.upbit.com/v1/ticker?markets=BTC-BFC` | **업비트는 BTC-BFC 마켓만** (KRW 마켓 없음) |
| 업비트 입출금 상태 | `api.upbit.com` (지갑상태) | — |

- **디프 대상:** 빗썸 `assetsstatus`의 deposit/withdrawal 값이 0이 되면 **입출금 중단**(중요 이벤트). 거래대금 급변, 업비트 BTC-BFC 가격/거래량 변동.

## 미식별 대형 콜드 (추적만)
- `0x4bAE7ba39E4e71660307dcE780f1Ec9b7B7666Ee` (87.4M): **유출 0, 소액 입금만 축적** = 장기 콜드/커스터디 추정(거래소 단정 불가). 대량 유출 발생 시 주목.

---

# 차원 9 — 글로벌 거래소 유동성 (한국 외)

**기준값 (2026-06-29, 공개 API):**
| 거래소 | 마켓 | 가격 | 24h 거래량 | 비고 |
|---|---|---|---|---|
| **HTX(Huobi)** | BFC/USDT | $0.01183 | ~**$2.2M** | 글로벌 주력 |
| Gate.io | BFC/USDT | $0.01201 | ~$3K(quote) | 미미 |
| Coinone(KR) | — | 미상장 | — | BFC 마켓 없음 |
| (참고 국내) 업비트 | **BTC-BFC만** | — | — | KRW 마켓 없음 |
| (참고 국내) 빗썸 | BFC/KRW | 17.74원 | ~₩2.08억 | KRW 주력 |

- **재실행:** HTX `api.huobi.pro/market/detail/merged?symbol=bfcusdt` · Gate `api.gateio.ws/api/v4/spot/tickers?currency_pair=BFC_USDT` · 업비트 `api.upbit.com/v1/ticker?markets=BTC-BFC` · 빗썸 `api.bithumb.com/public/ticker/BFC_KRW`
- **디프 대상:** 거래소간 가격 괴리(차익/김프), 거래량 급증, **신규 상장/상폐**(마켓 목록 변화).

---

# 차원 10 — 소셜 모멘텀

**기준값 (2026-06-30):**
| 채널 | 수치 | 신뢰도 |
|---|---|---|
| Telegram `Bifrost_Notice`(KR공지) | **860** | 확인 |
| Telegram `Bifrost_Global` | **7,129** (온라인 ~125) | 확인 |
| Medium `@bifrost` | **7,500** | 확인 |
| X `@Bifrost_Network` | **~82,000** (CoinCarp 81,877) | 추정(제3자집계) |
| Discord | ~20,200 | 추정/미확인 |

- **재실행:** `t.me/s/Bifrost_Notice`·`t.me/s/Bifrost_Global`(구독자수 grep) · Medium `bifrost.medium.com` · X는 차단되어 **CoinCarp 동일소스 유지 권장**(일관성)
- **디프 대상:** 구독자/팔로워 급증(관심도), 공지 빈도 변화.

> ※ 차원 9·10은 보조 신호. 핵심은 1~8.

---

# 부록 — 루프 실행 체크리스트 (요약)

매 루프:
1. **차원1·4** ★네이티브 우선★ explorer-backend `/addresses`(리치리스트)·`/stats`(당일tx 17,051) diff + 보조로 ethplorer(ETH ERC-20)
2. **차원2** RPC eth_call(0x...0400) → 검증자 24/9/15, 스테이킹 406M diff + 검증자 주소집합(data/validators-snapshot.md) diff
3. **차원3** Socket txn(17,532/10,132) + **Vault TVL**(ETH BFC 863.5M/BSC BTCB 44.3) + **BtcUSD 발행량 8.06M** diff
4. **차원5** github API → 커밋 SHA/릴리스/신규레포 diff
5. **차원6** medium-kr + telegram + 검색 → 워터마크 2026-06-02 이후 신규
6. **차원7** 파트너별 URL → 표의 "감시 신호" (특히 HashPort TVL, BitTrade BFC 상장)
7. **차원8** explorer-backend 클러스터 합(업비트 348M/빗썸 143.7M) diff + 빗썸 `assetsstatus`(입출금중단)
8. **차원9·10** 글로벌 시세(HTX/Gate) + 소셜(텔레그램/Medium) — 보조

변화 발견 시에만 보고 + 본 문서 기준값 갱신. 항상 BNC/Polkadot 항목 필터링.

---

# 부록 2 — 수집 확장 후보 (검토 결과, 우선순위순)

전체 리서치 검토 후 "더 수집하면 좋은" 항목. ⭐=권장.

> ✅ **이미 수집 완료(베이스라인 반영):** 거래소 순흐름(클러스터 확정), 입출금중단 감지(assetsstatus), 검증자 24주소(data/validators-snapshot.md, 단 실명매핑은 원천불가), 브릿지 Vault TVL, **BtcUSD 발행량(8.06M)**, 글로벌 거래소(차원9), 소셜(차원10).
> ⬜ **남은 후보:** 온체인 거버넌스 제안, 토큰 언락/베스팅 일정, 미식별 87M 콜드 정체.

| 후보 | 왜 가치있나 | 수집 방법 | 난이도 |
|---|---|---|---|
| ⭐ **거래소 순흐름(업비트/빗썸 클러스터 일별 델타)** | 매도/매수 압력 선행지표. 이미 클러스터 확정됨 | explorer-backend 잔액 합 일별 기록 | 쉬움 |
| ⭐ **입출금 중단 감지** | 상폐·해킹·점검 조기신호 | `assetsstatus` deposit/withdrawal=0 감시 | 쉬움 |
| ⭐ **검증자 이름↔주소 매핑** | "노드 변화"를 실명(BitTrade/AIF 등)으로 추적 | 익스플로러 validator 페이지 + 공지 대조 | 중 |
| ⭐ **브릿지 Vault 잔액(체인별)** | 브릿지 실제 TVL·자금흐름 정량화 | 각 체인 Vault 주소 잔액(02 B-1) 조회 | 중 |
| **BtcUSD 발행량/담보 추적** | BTCFi 핵심상품 성장 지표 | DefiLlama btcfi TVL + BtcUSD 컨트랙트(미확보) | 중 |
| **거버넌스/온체인 제안** | 토크노믹스·파라미터 변경 선행 | 메인넷 거버넌스 pallet/공지 | 중 |
| **토큰 언락/베스팅 일정** | 대량 언락 = 매도압력 이벤트 | 대형 컨트랙트(#3 0x4d5aa 등) 해제 패턴 | 어려움 |
| **소셜 모멘텀(X/텔레그램 수치)** | 관심도 변화 | @Bifrost_Network 팔로워, t.me 멤버수 | 쉬움 |
| **글로벌 거래소 유동성(HTX/Gate)** | 한국 외 흐름 | 각 거래소 공개 ticker | 쉬움 |
| **미식별 대형주소(0x4bAE7 87M 등) 정체** | 잠재 거래소/기관 물량 | 추가 클러스터 분석 + 테스트입금 | 어려움 |
