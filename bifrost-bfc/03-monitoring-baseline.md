# Bifrost (BFC) 모니터링 베이스라인 + 루프 플레이북

> 작성/스냅샷 기준: **2026-06-29** · 목적: 반복 루프가 "변동/주목할 변화"를 감지하기 위한 **기준값(baseline)** + **매 루프 재실행 쿼리/디프 대상** 정의
> 대상: **한국 파이랩테크놀로지 Bifrost Network, BFC** (Polkadot BNC 아님)
> 사용법: 매 루프마다 아래 각 차원의 "재실행"을 돌려 "기준값"과 diff → 차이 발생 시에만 보고. 변화 시 이 문서의 기준값을 갱신.

## ⚠️ 혼동 방지 (루프마다 필수 필터)
- 우리 대상: `bifrostnetwork.com`, `thebifrost.io`, `medium.com/bifrost`, `medium.com/bifrost-blog-kor`, GitHub `bifrost-platform`, X `@Bifrost_Network`, BFC ERC-20 `0x0c7D5ae0...Cab9c`, 메인넷 chainId **3068**.
- ❌ 제외(=Polkadot BNC): `bifrost.io`, `bifrost.io/blog`, `app.bifrost.io`, GitHub `bifrost-io`/`bifrost-finance`, vDOT/vKSM/SLP/parachain/Kusama 관련.
- ⚠️ **CoinMarketCap "CMC AI latest updates" 페이지는 BNC와 BFC를 섞음** (예: "100만 DOT 트레저리 상환" = BNC). 날짜 참고용으로만 쓰고 DOT/Polkadot 항목은 버릴 것.

---

# 차원 1 — 상위 어카운트(홀더) 변동 [ETH ERC-20]

**재실행:** `https://api.ethplorer.io/getTopTokenHolders/0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c?apiKey=freekey&limit=30`
**전체 홀더수 재실행:** `https://api.ethplorer.io/getTokenInfo/0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c?apiKey=freekey` → `holdersCount`

**기준값 (2026-06-29):** 전체 홀더 **3,619명** · totalSupply 40억 · 상위3 집중 **73.88%**

| # | 주소 | 잔액(BFC) | % | 유형 |
|---|---|---:|---:|---|
| 1 | `0x...dead` | 1,631,415,927 | 40.79 | **소각** |
| 2 | `0x2f95c102cc26875406bc689fb01ae382b82aa535` | 863,522,304 | 21.59 | **ETH Vault(브릿지)** |
| 3 | `0x4d5aa29862bc8186e19ee5b699494aa40fc83206` | 459,987,204 | 11.50 | 컨트랙트(베스팅/트레저리 추정) |
| 4 | `0x08d1b81813cff08e8525145ce132a097abc031ca` | 297,936,989 | 7.45 | EOA |
| 5 | `0xfa24b321bd8bb0e1c318795cf37bf95b4fa9247c` | 248,498,596 | 6.21 | EOA |
| 6 | `0x752725e9d69f784625256822ba11419a0615b788` | 131,124,840 | 3.28 | EOA |
| 7 | `0xb23f8b9b046a8223d261890fc9df05c2e951ad62` | 110,000,000 | 2.75 | EOA |
| 8 | `0x66a02618b638ffc07f993317cab8e635e1437ec7` | 70,000,000 | 1.75 | EOA |
| 9 | `0xcbe7d8f55aafa79821f504a992aa5c0f495f8714` | 68,537,888 | 1.71 | EOA |
| 10 | `0xa2a1a561719cef0225f951a6d2bdde80ef4a1b76` | 60,000,000 | 1.50 | EOA |

(11~30위는 2천만 BFC 이하 — 잔액 변동만 추적)

**디프 대상:** ① 각 주소 `rawBalance`/`share` 증감, ② top30 신규 진입자, ③ 이탈자, ④ 순위 변동. **1순위 알림:** #2 Vault·#1 소각·#3 컨트랙트 잔액 변화(토크노믹스/브릿지 이벤트), `holdersCount` 큰 변동.

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

검증자 파트너(공지): BitTrade, AI Fusion Capital. (이름↔주소 매핑은 익스플로러 수동 대조 필요)

**디프 대상:** 후보수(24)·Basic(9)·Full(15) 분포 변화, 총 스테이킹 ±, 검증자 주소집합 신규/이탈, 신규 검증자 공지(medium.com/bifrost).

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

---

# 차원 4 — 트랜잭션 변화 [ETH ERC-20]

**재실행:** `https://api.ethplorer.io/getTokenInfo/0x0c7D5ae0...Cab9c?apiKey=freekey` (카운터) + `https://api.ethplorer.io/getTokenHistory/0x0c7D5ae0...Cab9c?apiKey=freekey&limit=100&type=transfer` (대형전송 감시)

**기준값 (2026-06-29):**
| 지표 | 값 |
|---|---|
| transfersCount 누적 | **111,008** |
| txsCount 누적 | **56,044** |
| price | **$0.011789** (₩18.21) |
| volume24h | **$2.41M** (당시 7d 대비 +80%, 급증 구간) |
| market_cap_rank | ~901 |

**디프 대상:** transfersCount/txsCount 델타(활동 스파이크), volume24h 평소 대비 2~3배↑, **대형 전송**(value≥1,000,000 BFC) 특히 to/from이 dead·Vault·top30이면 알림. 직전 루프 최신 txHash 저장 후 그 이후만 신규 처리.
**보조(시세):** `https://api.coingecko.com/api/v3/coins/ethereum/contract/0x0c7D5ae0...Cab9c`

> 참고: 네이티브 체인(3068) 트랜잭션 활동은 ETH ERC-20과 별개로 훨씬 클 수 있음. 네이티브 tx 카운트는 차원 2의 RPC/블록번호 진행으로 간접 추적(블록 36,200,231 기준, 블록타임 ~3s).

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
→ **이 날짜보다 새로운 BFC 직접 항목이 나오면 "신규"**. (2026-06-29 현재 이후 신규 없음)

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

**기준값 (2026-06-29):**
| 채널 | 수치 | 비고 |
|---|---|---|
| Telegram `Bifrost_Notice` | **860 subscribers** | 공식 KR 공지 |
| X `@Bifrost_Network` | (수집중) | 페이지 존재(200) |
| Medium `medium.com/bifrost` | (수집중) | 공식 |

- **재실행:** `https://t.me/s/Bifrost_Notice`(구독자수 grep) · X는 nitter/검색 보조
- **디프 대상:** 구독자/팔로워 급증(관심도), 공지 빈도 변화.

> ※ 차원 9·10은 보조 신호. 핵심은 1~8.

---

# 부록 — 루프 실행 체크리스트 (요약)

매 루프:
1. **차원1·4** ethplorer getTopTokenHolders + getTokenInfo + getTokenHistory → 홀더/카운터/대형전송 diff
2. **차원2** RPC eth_call(0x...0400) → 검증자 24/9/15, 스테이킹 406M diff
3. **차원3** bscscan + blockscout counters → Socket txn 17,532/10,132 diff
4. **차원5** github API → 커밋 SHA/릴리스/신규레포 diff
5. **차원6** medium-kr + telegram + 검색 → 워터마크 2026-06-02 이후 신규
6. **차원7** 파트너별 URL → 표의 "감시 신호" (특히 HashPort TVL, BitTrade BFC 상장)
7. **차원8** explorer-backend API 리치리스트 diff(후보 #1 332M·#2 137M) + ethplorer ETH거래소주소(현 0). 확정 귀속은 테스트입금 필요

변화 발견 시에만 보고 + 본 문서 기준값 갱신. 항상 BNC/Polkadot 항목 필터링.

---

# 부록 2 — 수집 확장 후보 (검토 결과, 우선순위순)

전체 리서치 검토 후 "더 수집하면 좋은" 항목. ⭐=권장.

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
