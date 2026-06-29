# Bifrost (BFC) 심층 후속 리서치 — 온체인·GitHub·일본 사업

> 작성일: 2026-06-29 · `01-overview.md`의 후속/심화 문서 (미확정 항목 해소 + 일본 심층 + 온체인 실측)
> 대상: **한국 파이랩테크놀로지 Bifrost Network, BFC** (Polkadot BNC 아님)
> 표기 규칙: **확인** = 1차/소스 검증 / **부정확인** = 사실이 아님이 확인됨 / **미확인** = 자료 없음

---

## A. 온체인 실측 데이터 (관찰일 2026-06-29)

### A-1. BFC ERC-20 (Ethereum) `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c`
출처: ethplorer API (라이브)
- 컨트랙트 totalSupply: **40억 BFC** (초기 발행 그대로, 소각분 포함)
- 홀더 수: **약 3,619명** · 전송 누계 111,008 / txs 56,044
- 배포자(owner): `0x509f6180bc2b195c2864ce7ee920d3ac08943f17` (현재 BFC 미보유)

**상위 홀더 (2026-06-29):**
| # | 주소 | 비중 | 성격 |
|---|---|---|---|
| 1 | `0x...dead` | **40.79%** (~16.3억) | **소각 주소** (2022-02 재단 40% 소각과 일치) |
| 2 | `0x2f95c102cc26875406bc689fb01ae382b82aa535` | 21.59% (~8.64억) | **컨트랙트 = Ethereum Vault** (config의 ETH Vault `0x2F95C1...AA535`와 동일!) |
| 3 | `0x4d5aa29862bc8186e19ee5b699494aa40fc83206` | 11.5% (~4.6억) | 컨트랙트(스테이킹/락 추정) |
| 4 | `0x08d1b81813cff08e8525145ce132a097abc031ca` | 7.45% | EOA |
| 5 | `0xfa24b321bd8bb0e1c318795cf37bf95b4fa9247c` | 6.21% | |

→ 상위 3개가 ~73.9% 점유. **#2 홀더가 브릿지 Vault 컨트랙트**라는 점이 핵심(브릿지로 락업된 물량). ⚠️ etherscan 라벨 페이지가 봇 차단(403)이라 Upbit/Bithumb 거래소 핫월렛은 라벨로 식별 불가.

### A-2. 브릿지 Socket 활동
- **Ethereum Socket** `0x4A31FfeAc2...4DD84`: 컨트랙트 확인, 생성 2023-01-18, 배포자 `0x576f0a8a...` (Vault와 동일 인프라군)
- **BSC Socket** `0xb5Fa48E8...968dF`: **활성**. TransparentUpgradeableProxy(업그레이더블), **총 트랜잭션 17,530건**, 최근 활동 ~10시간 전 → 실가동 중
- ⚠️ Socket이 보유한 토큰으로 표시되는 HEX/DW 등은 스팸 에어드랍 → 브릿지 TVL 직접 산정 불가

### A-3. TVL / 시세 (DefiLlama + CoinGecko, 라이브)
- **BTCFi 프로토콜 TVL: 약 $2.63M** (Bifrost Network $2.63M / Bitcoin $6.40M / Base $66.8K) — `api.llama.fi/protocol/btcfi`
- **Bifrost Network 체인 전체 TVL: 약 $11.86M** — `api.llama.fi/v2/chains`
- BiFi(렌딩) TVL: 약 $4,901 (피크 2021-08 $207.9M → 사실상 붕괴)
- **시세 (2026-06-29):** 가격 **$0.01195**, 시총 **$16.6M** (#896), 24h 거래량 ~$2.4M, 유통 13.9억, 총공급 23.7억, 최대공급 ∞, FDV $28.3M
- ⚠️ DefiLlama에 "Bifrost"(BNC, gecko_id bifrost-native-coin, TVL $3.19M)가 별도 존재 → 혼동 주의

---

## B. 컨트랙트 주소 풀셋 (GitHub 소스 직접 추출 — 확정)

> 권위 출처: `bifrost-relayer.rs/configs/config.mainnet.yaml` + `asset-info-v2/assets/*/info.json`

### B-1. 체인별 Socket / Authority / Vault (메인넷)
| 체인 | ChainID | Socket | Vault |
|---|---|---|---|
| **Bifrost** | 3068 | `0xd551F33Ca8eCb0Be83d8799D9C68a368BA36Dd52` | `0xD85EB87caB9041ad00764b95796702b1104F42D7` |
| **Ethereum** | 1 | `0x4A31FfeAc276CC5e508cAC0568d932d398C4DD84` | `0x2F95C102Cc26875406BC689Fb01aE382B82AA535` |
| **BSC** | 56 | `0xb5Fa48E8B9b89760a9f9176388D1B64A8D4968dF` | `0x78ae4c0FD4f02CA79A2d8738d3369A4Bc5D4E323` |
| **Polygon** | 137 | `0x050606CC2Bcd9504991Be2c309D6c6c832Bb5bd0` | `0x5fA7fe5F94f2D15585a3134C1C5d3019c8c1645d` |
| **Base** | 8453 | `0xAe172D8c5E428D4b7C70f9E593b207F9daC9BF3e` | `0x4F7aB59b5AC112970F5dD66D8a7ac505c8E5e08B` |
| **Arbitrum** | 42161 | `0xac1552e30857A814a225BAa81145bcB071B46DDd` | `0xf549E4B5B4Cb7fd4e83b8AA047C742C06D527429` |
| **Oasys** | 248 | `0x4C7a44F3FB37A53F33D3fe3cCdE97A444F105239` | `0x872b347cd764d46c127ffefbcaB605FFF3f3a48C` |

(릴레이어 감시 체인: 3068, 1, 56, 137, 8453, 42161, 248)

**오라클 가격 피드 (Ethereum, Chainlink):** BTC/USD `0xf4030086...e88c`, JPY/USD `0xBcE206ca...beb3`, USDC/USD `0x8fFfFfd4...18f6`, USDT/USD `0x3E7d1eAB...e32D`. → **JPY/USD 피드를 쓴다는 점이 일본 사업(엔화 자산)과 일치.**

### B-2. BFC 토큰 — 체인별 (asset-info-v2/bfc-0)
| 체인 | 주소 |
|---|---|
| Ethereum | `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c` (원본 ERC-20) |
| Oasys | `0x640952E7984f2ECedeAd8Fd97aA618Ab1210A21C` |
| Bifrost (Unified BFC) | `0xAe172D8c5E428D4b7C70f9E593b207F9daC9BF3e` |
| Bifrost (네이티브 가스) | `0xEeeeeEee...eeEEeE` (placeholder) |

→ **BSC(evm-56) 항목이 소스에 아예 없음 = 공식 BFC의 BSC 배포는 존재하지 않음 (확정).**

### B-3. BiFi 토큰 (asset-info-v2/bifi-0)
| 체인 | 주소 | 심볼 |
|---|---|---|
| Ethereum | `0x2791BfD60D232150Bff86b39B7146c0eaAA2BA81` | BiFi |
| **BSC** | `0x1378e33a09d8bd8e449CFD8A5aBCa0439286d645` | **BiFiB** (BSC상 유일한 공식 Bifrost 생태계 토큰) |
| Bifrost | `0x047938C3aD13c1eB821C8e310B2B6F889b6d0003` | Unified BiFi |

### B-4. 가짜 토큰 (블랙리스트 — 절대 BFC로 취급 금지)
- BSC `0xf4b5cd30bb12955ab54e106003e79223639009ec` — "HelloBEP20", 총발행 1만개, 홀더 5명 **(가짜 확정)**
- BSC `0x5Dec5345bA6c4CBcb6CF0ACA4954954174068dC9` — 총발행 1000조, 홀더 15명 **(가짜 확정)**
- Fantom `0x84c882a4...106117` — **Anyswap 브릿지 래퍼(AnyswapV3ERC20)**. 공식 발행 아닌 브릿지 산출물. (이전 문서에서 "Fantom 발행"으로 본 것 정정)

### B-5. 비트코인 통합 메커니즘 (코드 기반)
- BTC vault는 **정적 멀티시그 주소가 아님**. 릴레이어 그룹 공개키를 모아 만든 **임계치(threshold) 다중서명 + PSBT 기반 동적 vault** (taproot/musig). 사용자/라운드별 동적 생성.
- 입금 흐름: BTC 입금 → `registration_pool`로 vault↔사용자 Bifrost 주소 매핑 → `bitcoin_socket`이 릴레이어 투표 집계 → UTXO 릴레이. 출금은 `relay_executive`만 PSBT 서명.
- v2.1.0(2025-09)부터 **BLAZE 팔레트**(고급 UTXO 관리) 도입.
- ⚠️ config에 하드코딩된 BTC vault 주소 없음(운영자가 RPC만 설정) → 정적 BTC 주소로 추적 불가, 온체인 BTC 추적은 Registration Pool 이벤트 기반으로 해야 함.

---

## C. 토크노믹스 정합성 (4B 캡 미스터리 해소)

**시계열로 정리 (확인):**
1. 초기 발행 **40억(4B) BFC** (백서 캡)
2. **2022-02 재단이 40%인 16억 BFC 소각** → `0x...dead`에 락 (온체인 #1 홀더와 일치)
3. **2023-01-30 메인넷 전환** 시 고정 캡 폐지 → **DPoS 인플레이션 모델**로 전환, max supply ∞
4. **StableDAO (2025-07-18 출범):** DAO 수익 30%로 BFC 소각 (2025 Q3 ~50M BFC, ~$1.45M 소각) → 디플레이션 압력

**인플레이션율 — ⚠️ 코드 vs 문서 불일치:**
- **메인넷 체인스펙 코드(`chain_spec.rs`): 연 13% 고정** (min=ideal=max=13%)
- 공식 문서(docs): min 7% / ideal 10% / max 13% (동적)
- Dev 체인: 7/13/15%, Testnet: 100% 고정
- → 실제 메인넷은 코드값(13%)이 우선. 고정 스테이킹 APR은 없고 개인별 추정수익.
- 기대 스테이킹량: 5,000 / 10,000 / 50,000 BFC × SUPPLY_FACTOR

---

## D. 검증 결과 — 정정 사항 (중요)

### D-1. eBTC / BitVM = **파이랩 제품 아님 (부정확인)**
- `bifrost.blue`(eBTC, BitVM 1:1 BTC 백킹)는 **Pi Lab의 Bifrost Network와 무관한 별개/동명 프로젝트**. 도메인은 현재 DNS 미해석(비활성 가능성).
- Pi Lab 공식 채널(pilab.co, bifrostnetwork.com, btcfi.one)에 eBTC/BitVM 언급 **전무**.
- **Pi Lab의 실제 비트코인 라인 = BRP(Bitcoin Relaying Protocol) + BtcUSD(BTC 담보 스테이블, 3.5% APY) + BTCFi/BTCFi Boost.** BitVM 사용 안 함.

### D-2. JPYSC ↔ Bifrost = **직접 연결 없음 (부정확인, 재확인)**
- JPYSC = Shinsei Trust&Banking 발행 / SBI VC Trade 유통 / **Startale** 기술. 배포 예정 체인은 Strium L1, Soneium 등. **Bifrost/BFC 언급 전무.**
- 단, Bifrost는 **SBI Digital Finance와 별도 제휴**(2025-08) → 같은 SBI 그룹 우산이나 JPYSC와는 무관.

### D-3. 신제품 상태
- **Pockie 지갑 (확인):** 셀프커스터디 멀티체인 지갑, **8체인** (ETH/BNB/Arbitrum/Polygon/Avalanche/Base/Bifrost/Klaytn), Chrome 확장. 2023-12 출시.
- **Biplorer (확인):** 온체인 분석 도구, pilab.co에 등재 (상세 미공개)
- **MJPY/MKRW/MUSD (미확인/미출시 추정):** 2025-07 상표 출원 단계에 머묾. **실제 스테이블코인 라인은 BtcUSD.**

### D-4. 보안 사고
- **2022-07-10 BiFi 해킹: 약 $2.25M (1,852 ETH).** 스마트컨트랙트가 아닌 **BTC 주소 발급 서버 키 유출**이 원인.
- **2024–2026 Bifrost Network / 브릿지(CCCP) 신규 해킹은 확인되지 않음.**

---

## E. GitHub 활동 상세 (github.com/bifrost-platform)

**bifrost-node 릴리스:**
- **v2.2.0 (2026-06-24, 최신):** Polkadot SDK stable2512 업글 → **Ethereum Fusaka 하드포크 지원**, BLAZE 스토리지 마이그레이션 v3
- v2.1.0 (2025-09-11): **BLAZE 팔레트**(BTC UTXO 관리), **Pectra/EIP-7702 계정추상화**, trace RPC
- v2.0.0 (2024-11-07): **BRP 통합 + Bitcoin 지원 도입**

**bifrost-relayer.rs 릴리스:**
- **v3.0.0 (2025-06-24, 필수 업그레이드):** **CCCP v2 + Hook** 통합(테스트넷), Price Deviation Checker, core chain 지원 제거

**저장소 현황:** 약 20개. node(★39)·relayer(★12) 모두 2026-06 활발. **2025년 신규 저장소 사실상 없음**(최신 생성=2024-12 Bifrost-Node-AdminPanel). relayer.py는 deprecated/archived. ⚠️ 정확한 기여자 수/커밋 빈도는 세션 GitHub 권한 제한(tkdrn416/-만 허용)으로 미확인 — 소규모 코어팀 추정.

---

## F. 일본 사업 — 전체 타임라인 + 심층

### F-1. 일본 행보 타임라인 (확인)
| 시점 | 사건 |
|---|---|
| 2024-04-19 | **JCBA**(일본암호자산비즈니스협회) 가입 |
| 2024-09-26 | **Japan Open Chain(JOC)** 전략적 투자·제휴 |
| 2024-11-29 | **BitTrade**(구 Huobi Japan) 노드 검증자 합류 |
| 2025-01-29 | **Oasys·MCH·PLANZ** 생태계 BtcUSD 통합 발표 |
| 2025-03-04 | **FAJ**(일본핀테크협회) Web3 부문 가입 |
| 2025-06-30 | **AI Fusion Capital(AIF)** — 도쿄 상장사, 검증자+BTCFi 재무 |
| 2025-07-24 | **BTCFi Boost** 정식 출시 |
| 2025-07~08 | **Oasys Gaming DEX 자동 브릿지** 라이브 (최대 ~40% APY) |
| 2025-08-13 | **SBI Digital Finance** btcUSD 개발 논의 개시 |
| 2025-10-23 | **double jump.tokyo(DJT)** N.suite — BTC/JPYC 급여 프레임워크 |
| 2025-11-04 | **BCCC**(블록체인 협업 컨소시엄) 가입 |
| 2025-12-16 | **Animoca Brands Japan** — 상장사 BTC 재무 공동검증 |
| 2026-02-05 | **MOIN × JOC × Bifrost** 다통화 스테이블코인 송금 MOU |
| 2026-05-20 | DJT **N.suite Treasury Access Plan** (JPYC 렌딩 1단계) |
| 2026-06-01 | **HashPort Wallet** 통합, JPYC 연 4% 렌딩 |

### F-2. Double Jump Tokyo (DJT) / N.suite
- DJT = 일본 대표 Web3 인프라·블록체인게임사. **N.suite** = 법인용 멀티시그·승인워크플로우 지갑 OS.
- 2025-10-23 제휴: N.suite에 BTCFi/BtcUSD/BiFi 통합 → **BTC/JPYC 기업 급여·회계·재무 프레임워크**. "일본 최초 기업 단위 스테이블코인 운용".
- **★ 후속 (2026-05-20): "N.suite Treasury Access Plan"** — N.suite를 Treasury OS로 확장, 일본 법인이 N.suite 환경 유지한 채 **Bifrost BTCFi Boost로 JPYC 렌딩 접근**. DJT는 "렌딩 사업자가 아니며 서비스 주체는 Bifrost"라 명시. (파일럿 고객명/수익률 미공개)

### F-3. HashPort Wallet
- 2026-06-01: Bifrost **"BTCFi Partners"** 솔루션이 HashPort Wallet 통합 → **JPYC 연 4.0% 고정수익, 락업·만기 없음.** 제공 주체 = 싱가포르 Bifrost 법인.
- "Summer Campaign"(3개월, 보너스 금리) — JPYC 신규 유저 타깃.
- HashPort Wallet = **EXPO 2025(오사카 만박) 공식 디지털 지갑** 출신, 누적 **100만+ 다운로드**(일본 1위 논커스터디), **JPYC 사용자 84%가 사용**, "JPYC 공식 추천 지갑".
- ⚠️ **TVL·유치 규모·캠페인 실적 수치는 미공개** (추적 필요)
- ⚠️ 단위 주의: 다운로드는 115만(≈1.15M)이지 1억1,500만 아님.
- ❌ 폐쇄된 hashport bridge(2026-05-31)와는 무관.

### F-4. SBI
- 2025-08-13: **SBI Digital Finance**(SBI홀딩스 자회사, HashHub Lending 운영)와 btcUSD 활용처·FSA 규제부합 BTC 관리 프레임워크 **"개발 논의" 개시**. (정식 MOU/제품 아님)
- ⚠️ 영어 매체의 "SBI Bank" 표기는 부정확 → 정확히는 **SBI Digital Finance**.
- **제품화 진척은 2026-06 현재 미확인.**
- 전략적 위치: SBI는 USDC(Circle JV)+JPYSC(자체 엔화)로 **발행 진영**. Bifrost는 경쟁자가 아닌 **"BTC 담보 수익·기관 BTC 관리" 보완재**.

### F-5. JPYC 자체 현황 (★ Bifrost는 발행체인 아님)
- **JPYC는 Bifrost Network에서 네이티브 발행되지 않음.** 발행 체인 = Ethereum/Polygon/Avalanche(+Kaia). Bifrost는 JPYC를 **"예치→수익" 자산으로 쓰는 렌딩 venue**일 뿐.
- JPYC 출시 2025-10-27 (일본 최초 규제준수 엔화 SC, 제2종 자금이동업, 송금 상한 10만엔).
- 발행량: 누적 ~21억엔(2026-04) → **30억엔 돌파(2026-05말)**. 활성지갑 13.7만. 목표 1조엔(→3년 10조엔).
- JPYC사 Series B 총 ~46억엔 (Metaplanet·北洋은행·住友生命·Sony Bank 등 참여).

### F-6. 기타 일본 파트너 (NEW)
- **AI Fusion Capital (2025-06-30):** 도쿄 **상장** AI 투자사. *상장 일본기업 최초* Bifrost 검증자 운영 + BTCFi를 BTC 재무 엔진 채택 (~24.6 BTC 보유 보도).
- **Animoca Brands Japan (2025-12-16):** 상장사 BTC 재무 솔루션 공동검증. Bifrost=미들웨어, ABJ=서비스 전달. ⚠️ ABJ는 Solv/Rootstock 등 경쟁 인프라도 병행 채택(양날).
- **Oasys (게임 체인):** BTCFi Boost가 BtcUSD를 Oasys로 **자동 브릿지** → Gaming DEX 풀 예치, 최대 ~40% APY. (CCCP 실가동 사례)
- **MOIN × JOC × Bifrost (2026-02-05):** 한국 송금 핀테크 MOIN 합류. KRW·JPY·EUR 다통화 스테이블코인 + 국경간 송금. MOIN(규제·송금), JOC(엔화 인프라), Bifrost(크로스체인 발행/송금).
- **JOC (2024-09-26):** 투자액 비공개. Bifrost 브릿지의 JOC 배포 + JOC의 BTCFi dApp.
- **BitTrade (2024-11-29):** 검증자. ⚠️ BFC 상장 등 후속은 미확인.

### F-7. 전략 해석 — 왜 일본인가
1. **규제 명확성:** 2023 스테이블코인 법제 + 2026 암호자산 FIEA 금융상품 재분류(세율 55%→20% 추진, 현물 ETF 길). 기관용 BTC 시장이 가장 또렷 → Bifrost는 "FSA 규제 부합 BTC 관리" 일관 메시지.
2. **BTCFi 포지셔닝:** 스테이블코인 발행 경쟁(JPYC/JPYSC/USDC) 회피, BtcUSD(BTC 담보)+BTCFi 수익으로 차별화. JPYC·USDC를 "예치 자산"으로 흡수 + 기업 BTC 재무(상장사 BTC 보유 붐) 정조준.
3. **4중 진입 레이어:** ①협회(JCBA·FAJ·BCCC) ②검증자(BitTrade·AIF) ③지갑/플랫폼(N.suite·HashPort·EXPO지갑) ④금융파트너(SBI·Animoca). 한국 본사 직접 영업 대신 현지 신뢰주체를 프런트로(규제 리스크 분산, 서비스 주체는 싱가포르 법인).
4. **크로스체인 허브화:** Oasys·JOC·MOIN으로 아시아 결제/RWA 허브 야망.
5. **경쟁:** 발행은 비경쟁. 기업 BTC 재무에선 Animoca×Solv, Animoca×Rootstock와 경쟁. 글로벌 BTCFi 규모(WBTC ~$63억, Babylon, Stacks)엔 열위 → 일본 규제우위+기관채널로 상쇄.

---

## G. 추적 필요 공백 (다음 루프 후보)
1. **HashPort 4% JPYC 렌딩 TVL/유치 규모** — 미공개, 발표 주시
2. **SBI Digital Finance 논의의 제품화** 진척
3. **BitTrade BFC 상장** 등 후속
4. BTC vault 멀티시그 임계값(M-of-N) 정확 수치 (musig 라이브러리 코드)
5. GitHub 정확 기여자/커밋 통계 (세션 권한 밖)
6. BtcUSD 토큰 컨트랙트 주소 (Bifrost L1 자체 발행이라 외부 익스플로러 인덱싱 제한)

---

### 핵심 소스
온체인: [ethplorer BFC](https://ethplorer.io/address/0x0c7d5ae016f806603cb1782bea29ac69471cab9c) · [BSC Socket](https://bscscan.com/address/0xb5Fa48E8B9b89760a9f9176388D1B64A8D4968dF) · [DefiLlama btcfi](https://api.llama.fi/protocol/btcfi) · [CoinGecko](https://www.coingecko.com/en/coins/bifrost)
GitHub: [config.mainnet.yaml](https://raw.githubusercontent.com/bifrost-platform/bifrost-relayer.rs/main/configs/config.mainnet.yaml) · [asset-info-v2](https://github.com/bifrost-platform/asset-info-v2) · [node releases](https://github.com/bifrost-platform/bifrost-node/releases) · [relayer releases](https://github.com/bifrost-platform/bifrost-relayer.rs/releases)
일본: [DJT 제휴(Medium)](https://bifrost.medium.com/bifrost-double-jump-tokyo-partnership-announcement-dc4685112106) · [DJT Treasury Plan](https://itbusinesstoday.com/fintech/blockchain/double-jump-tokyo-debuts-corporate-treasury-os-plan/) · [HashPort(JinaCoin)](https://jinacoin.ne.jp/jpyc-bifrost-hashport-20260602/) · [SBI(Medium)](https://bifrost.medium.com/bifrost-network-initiates-development-discussions-with-sbi-digital-finance-for-btcusd-usecases-06cf5fca798e) · [AIF(Medium)](https://bifrost.medium.com/bifrost-x-aif-ai-fusion-capital-group-partnership-0566d56021e3) · [Animoca JP(MEXC)](https://www.mexc.com/news/277830) · [MOIN×JOC(G.U.)](https://www.gu-group.com/news/joc-moin-bifrost) · [JPYC 발행량 PR](https://prtimes.jp/main/html/rd/p/000000313.000054018.html)
