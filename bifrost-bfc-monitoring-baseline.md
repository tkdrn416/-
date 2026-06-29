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

(11~30위는 2천만 BFC 이하 — 전체 표는 `bifrost-bfc-research-followup.md` 참조 불필요, 잔액 변동만 추적)

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

# 차원 8 (추가) — 한국 거래소(업비트/빗썸) BFC 보유량

**★ 핵심:** 업비트/빗썸의 알려진 이더리움 핫·콜드월렛은 **BFC ERC-20을 0 보유**(직접 확인). 거래소 BFC는 **네이티브 Bifrost 메인넷(3068)**에 있음 → ETH만 보면 안 잡힘.

**현재 가능한 것:**
- ETH ERC-20 거래소 라벨 주소 모니터링(만일의 이동 대비, 현재 0):
  - Bithumb Hot `0x17e5545b11b468072283cee1f066a059fb0dbf24`, Bithumb `0x88d34944cf554e9cccf4a24292d891f620e9c94f`
  - Upbit `0x390de26d772d2e2005c6d1d24afc902bae37a4bb`, `0xba826fec90cefdf6706858e5fbafcb27a290fbe0`, `0x5e032243d507c743b061ef021e2ec7fcc6d3ab89`
  - 재실행: `https://api.ethplorer.io/getAddressInfo/{ADDR}?apiKey=freekey` → tokens[]에서 BFC balance
- (참고) ETH 상위홀더 중 거래소 라벨은 KuCoin `0x2677c4c8757da1857cc7cc4071e0e0dd32ccb975`(BFC ~4.5M), Gate `0x0d0707963952f2fba59dd06f2b425ace40b492fe`(BFC 0)

**미해결 (후속 과제):**
1. **네이티브 Bifrost 체인의 업비트/빗썸 입금/핫월렛 주소 확정** — 익스플로러가 Next.js SPA라 표준 Blockscout API(`/api/v2/...`, `/api?module=...`)가 HTML 반환. **별도 API 백엔드 호스트 탐색 필요**(예: blockscout 백엔드 서브도메인) 또는 익스플로러 UI에서 리치리스트/라벨 수동 확보.
2. 빗썸 증빙센터(`bithumb.com/customer_support/proof`)는 클라이언트 렌더(503/빈본문) → 백엔드 JSON 엔드포인트 탐색 필요. 업비트 투명성보고서는 코인별 수치 없음.

**확정 후 디프:** 네이티브 거래소 주소 잔액 일별 델타 = 순유입(+, 매도압력)/순유출(−) 프록시.

---

# 부록 — 루프 실행 체크리스트 (요약)

매 루프:
1. **차원1·4** ethplorer getTopTokenHolders + getTokenInfo + getTokenHistory → 홀더/카운터/대형전송 diff
2. **차원2** RPC eth_call(0x...0400) → 검증자 24/9/15, 스테이킹 406M diff
3. **차원3** bscscan + blockscout counters → Socket txn 17,532/10,132 diff
4. **차원5** github API → 커밋 SHA/릴리스/신규레포 diff
5. **차원6** medium-kr + telegram + 검색 → 워터마크 2026-06-02 이후 신규
6. **차원7** 파트너별 URL → 표의 "감시 신호" (특히 HashPort TVL, BitTrade BFC 상장)
7. **차원8** ethplorer 거래소주소(현 0) + [후속] 네이티브 거래소주소 확정

변화 발견 시에만 보고 + 본 문서 기준값 갱신. 항상 BNC/Polkadot 항목 필터링.
