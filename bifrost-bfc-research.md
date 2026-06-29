# Bifrost (BFC) 사전 리서치 — 파이랩테크놀로지

> 작성일: 2026-06-29 · 목적: 향후 루프 작업(온체인 분석, GitHub, 일본 기관, 기업 협력)을 위한 배경지식 베이스
> 대상: **한국 파이랩테크놀로지(Pi Lab Technology)의 Bifrost Network, 티커 BFC (바이프로스트)**
>
> 📎 **심화/정정판은 [`bifrost-bfc-research-followup.md`](./bifrost-bfc-research-followup.md) 참조** — 온체인 실측, 전체 컨트랙트 주소 풀셋, 일본 사업 타임라인, 검증/정정 사항이 들어 있습니다. 아래 본문과 후속 문서가 충돌하면 **후속 문서가 우선**합니다.
>
> **주요 정정 (후속 조사 결과):** ① BSC에 공식 BFC 토큰은 **존재하지 않음**(소스로 확정). ② Fantom `0x84c882...`는 자체 발행이 아닌 **Anyswap 브릿지 래퍼**. ③ eBTC/BitVM(bifrost.blue)은 **파이랩 제품 아님**(동명 별개 프로젝트). ④ JPYSC ↔ Bifrost **직접 연결 없음**(단 SBI Digital Finance와는 별도 제휴). ⑤ MJPY/MKRW/MUSD는 **상표 출원 단계**(실제 스테이블코인은 BtcUSD). ⑥ BFC 공급: 2022년 40%(16억) 소각 + 메인넷서 캡 폐지 → 인플레이션(메인넷 코드 13% 고정).

---

## ⚠️ 가장 중요한 디스앰비규에이션 (절대 혼동 금지)

| 구분 | ✅ 우리 대상 (BFC) | ❌ 혼동 대상 |
|---|---|---|
| **BFC = Bifrost Network** | 한국 **파이랩테크놀로지** L1 크로스체인 | — |
| BNC = Bifrost Finance | — | **Polkadot** 리퀴드 스테이킹 (bifrost.io, github.com/bifrost-io) |
| "Bifrost" (Cardano) | — | FluidTokens의 Bitcoin-Cardano 브릿지 |
| "Bifrost Wallet" | — | bifrostwallet.com (무관한 지갑) |
| `maximhq/bifrost` 등 | — | AI 게이트웨이/SDK (동명이인 GitHub) |

- 우리 대상 식별자: **ERC-20 컨트랙트 `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c`**, 도메인 **bifrostnetwork.com / thebifrost.io / pilab.co**, GitHub org **bifrost-platform**.
- ⚠️ 일부 가격/집계 사이트(예: CoinCodex)가 BFC를 BNC와 혼용함 → 시세·시총 인용 시 반드시 한국 파이랩 BFC인지 확인.

---

## 1. 회사 개요 — Pi Lab Technology (파이랩테크놀로지)

- **설립:** 2017년 (9월). ※ 일부 영문 2차 자료의 "2016년 설립/교수 2인 창업"은 부정확. 3월 14일은 'Pi Day' 브랜드 상징일이며 설립일 아님.
- **창업/경영진 (공동창업 3인):**
  - 박도현 (Dohyun Pak) — **CEO**
  - 이종협 (Jonghyup Lee) — **CTO**
  - 유창현 (Changhyun Yoo) — **COO**
- **본사:** 서울 성동구 성수일로8길 5 (성수동)
- **직원:** 약 38명 (원티드 기준)
- **투자유치:**
  - 2019년 시드 약 $3.3M (한국투자파트너스, 스틱벤처스 등)
  - 시리즈 A 약 $8.4M / ~100억 원 (한국투자파트너스 리드, 스틱벤처스, 유안타인베스트먼트)
  - 누적 약 140억 원
  - 별도 2022-03 **$57M(약 700억 원) 에코펀드** 출범 (생태계 확장용, 회사 투자유치와 구분. 첫 수혜: Delta Finance)
- **2025–2026 재포지셔닝:** "기관용 비트코인 금융 레이어 + 스테이블코인 인프라" — BTCFi, BTCFi-Boost, Pockie(지갑), Biplorer(온체인 분석)를 전면 배치.

출처: [PRNewswire(에코펀드)](https://www.prnewswire.com/news-releases/pilab-technology-bifrost-announces-a-57-million-eco-fund-to-expand-its-blockchain-ecosystem-301509950.html) · [Medium 공식](https://medium.com/bifrost/everything-you-need-to-know-about-bifrost-8f8943107ace) · [THE VC](https://thevc.kr/pilab) · [원티드](https://www.wanted.co.kr/company/2611) · [PiLab](https://www.pilab.co/)

---

## 2. 프로젝트 개요 & 제품군

**정체성:** 출발은 멀티체인 미들웨어 → 현재 **EVM 호환 L1 (Bifrost Network)** + BTCFi 중심.

**핵심 기술 — CCCP (Cross-Chain Communication Protocol):** 각 외부 체인에 배포한 **Socket Contract** + **Relayer(= 코어 검증자)** 조합으로 체인 간 메시지 전달. 다수결 서명 합의, timeout rollback(자산 잠김 방지).

**주요 제품:**
- **Bifrost Network** — EVM 호환 L1 코어 (메인넷)
- **BiFi** — 멀티체인 렌딩 (BTC 담보로 ETH 자산 차입; 랩드 토큰 없는 네이티브 크로스체인 렌딩). 배포: Ethereum, BSC, Avalanche. 거버넌스 토큰 BIFI 별도.
- **BiFi X** — 플래시론 기반 레버리지/마진
- **Biport Wallet** — 멀티체인 지갑 (ETH/BSC/AVAX/BTC). 후속 지갑 **Pockie**
- **ChainRunner Q** — DeFi 애그리게이터
- **BTCFi / BTCFi-Boost** (2024-04 출시) — 네이티브 BTC 담보 CDP, **BtcUSD** 민팅(고정금리 3.5%)

출처: [Medium 공식](https://medium.com/bifrost/everything-you-need-to-know-about-bifrost-8f8943107ace) · [docs(llms-full)](https://docs.bifrostnetwork.com/bifrost-network/llms-full.txt) · [ZDNet(BTCFi)](https://zdnet.co.kr/view/?no=20240417123558)

---

## 3. BFC 토큰

- **티커:** BFC
- **발행 체인 / 컨트랙트:**
  - **Ethereum ERC-20 (canonical):** `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c` (decimals 18)
  - **Fantom:** `0x84c882a4d8eb448ce086ea19418ca0f32f106117`
  - **Bifrost Network 메인넷:** 네이티브 가스/스테이킹 토큰 (별도 ERC-20 아님)
  - ⚠️ **BSC의 `0xf4b5cd30bb12955ab54e106003e79223639009ec` 는 가짜** ("HelloBEP20", 총공급 1만개). BFC로 취급 금지. 공식 BSC 컨트랙트는 미확정.
- **공급량:** 초기 설계 40억(4B) → 현재 시장데이터(CMC/CG) 총공급 약 23.7억~25.8억, 유통 약 13.8억, 최대공급 ∞ (DPoS 인플레이션). 정확값은 CG/CMC 실시간 확인 권장.
- **BFC vs BIFI:** BFC = 네이티브 코인(가스/스테이킹/거버넌스/검증자 인센티브). BIFI = DeFi 앱 BiFi의 거버넌스 토큰(별도). BiFi 사용 시 BFC 락업/지불 필요. BIFI 총발행 10억.
- **상장:** 업비트(BTC/KRW, 메인), 빗썸(KRW), HTX(USDT), Upbit Indonesia

출처: [Etherscan](https://etherscan.io/token/0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c) · [CoinGecko](https://www.coingecko.com/en/coins/bifrost) · [CoinMarketCap](https://coinmarketcap.com/currencies/bifrost/)

---

## 4. Bifrost Network 메인넷 (온체인 조회 핵심 정보)

| 항목 | 값 |
|---|---|
| **Chain ID** | **3068** (테스트넷 49088) |
| 네이티브 토큰 | BFC (decimals 18) |
| RPC | `https://public-01.mainnet.bifrostnetwork.com/rpc` , `https://public-02.mainnet.thebifrost.io/rpc` |
| **익스플로러** | **`https://explorer.mainnet.bifrostnetwork.com/`** |
| 합의 | **DPoS** + 블록생성 **AuRA(Authority Round)** + 파이널리티 **GRANDPA** |
| 아키텍처 | **Substrate(FRAME) + Frontier(EVM 호환)** — Cosmos/geth 아님 |
| EVM 호환 | 완전 호환 (Solidity, MetaMask, Web3/Ethers, HardHat, ERC-20/721) |
| 스펙 | 블록타임 ~3초, ~1,000 TPS, 매우 낮은 수수료 |
| 출시 | **2023-01-30** 메인넷 정식 전환 |
| 노드 요건 | Basic: self-bond 40만 BFC / 투표력 200만. Full(검증자+릴레이어): self-bond 40만 / 투표력 400만 |

**메인넷 시스템(precompile) 컨트랙트 (고정 주소):**
- Socket `0xd551F33Ca8eCb0Be83d8799D9C68a368BA36Dd52`
- Bitcoin Socket `0x73A9E443F51eE40C1469A740D9CCf0118e8FD9ca`
- Registration Pool `0x...0100` · Socket Queue `0x...0101` · Blaze `0x...0102`
- Authority `0x...0400` · Relay Executive `0x...0803` · Relayer Manager `0x...2000`

출처: [chainid.network/3068](https://chainid.network/chain/3068/) · [docs MetaMask](https://docs.bifrostnetwork.com/bifrost-network/add-network/metamask) · [docs Architecture](https://docs.bifrostnetwork.com/bifrost-network/bifrost-network-architecture) · [relayer 설정](https://docs.bifrostnetwork.com/bifrost-network/running-a-node/guide-for-operators/setting-up-a-relayer/bifrost-relayer.rs)

---

## 5. 크로스체인 브릿지 (The BIFROST Bridge / CCCP)

- **앱:** https://app.bifrost.io · 수수료 0.005%, 최대 ~15분
- **연결 체인 (9개):** Bifrost Network, Bitcoin, Ethereum, Base, Arbitrum, Core, BNB Chain, Polygon, Oasys
- **지원 자산:** BFC, BiFi, ETH, USDC, USDT, WBTC 등
- **구조:** Socket Contract(각 체인) + Relayer(=검증자) → CCC 이벤트 전달 → 다수결 서명 → primary relayer 일괄 제출 실행. Oracle Service가 BTC 블록해시·가격 등 제출(reorg-aware).

**체인별 Socket / Authority 컨트랙트 (메인넷) — 브릿지 플로우 추적용:**

| 체인 | Chain ID | Socket | Authority |
|---|---|---|---|
| Ethereum | 1 | `0x4A31FfeAc276CC5e508cAC0568d932d398C4DD84` | `0xAdcaa90cabDc730855064d5b0f5242c16A9B7E10` |
| BSC | 56 | `0xb5Fa48E8B9b89760a9f9176388D1B64A8D4968dF` | `0xF0500d77d5446665314722b963ab1F71872063E9` |
| Polygon | 137 | `0x050606CC2Bcd9504991Be2c309D6c6c832Bb5bd0` | `0x7F48909fBd1E38f1e05B5E326A44175fc2462B13` |
| Base | 8453 | `0xAe172D8c5E428D4b7C70f9E593b207F9daC9BF3e` | `0x4C7a44F3FB37A53F33D3fe3cCdE97A444F105239` |
| Arbitrum | 42161 | `0xac1552e30857A814a225BAa81145bcB071B46DDd` | `0xA069a57426Cd4c53925c1847Bec01aAB832A5118` |
| Core | 1116 | `0x4C7a44F3FB37A53F33D3fe3cCdE97A444F105239` | `0xA069a57426Cd4c53925c1847Bec01aAB832A5118` |
| Oasys | 248 | `0x4C7a44F3FB37A53F33D3fe3cCdE97A444F105239` | `0x48820089C1d4f5d768f6800CF647b4f5b8675CFA` |
| Bitcoin | 10000 | (네이티브 — Bitcoin Socket/vault 사용) | — |

출처: [Bridge Guide](https://docs.bifrostnetwork.com/bifrost-network/bridge/bridge-guide) · [CCCP](https://docs.bifrostnetwork.com/bifrost-network/bifrost-network-architecture/cross-chain-communication-protocol-cccp) · [Socket API](https://docs.bifrostnetwork.com/bifrost-network/developer-documentations/cross-chain-transaction-and-oracle-api/socket-contract-api)

---

## 6. 비트코인 / BTCFi

- **Bitcoin Socket:** 메인넷 `0x73A9E443F51eE40C1469A740D9CCf0118e8FD9ca` · Bitcoin chainId 10000(메인)/10001(테스트)
- **Registration Pool** `0x...0100`: 사용자별 BTC 주소 등록/매핑(peg-in 식별)
- **Oracle BTC 처리:** 릴레이어가 최신 BTC 블록해시 제출, reorg 시 정정
- **BTCFi** (https://www.btcfi.one): 네이티브 BTC 담보 CDP → **BtcUSD**(BTC 백드 스테이블) 민트, 고정금리 3.5%. Core, Stacks(STX/aBTC/sBTC), XLink/ALEX와 연동
- ⚠️ "eBTC를 BitVM으로 1:1 백킹" 류 서술은 타 프로젝트(bifrost.blue) 혼동 가능성 → 별도 검증 필요. Pi Lab 공식 BTC 자산은 **BtcUSD**

출처: [Stacks Foundation](https://stacks.foundation/bifrost-stacks-collaboration) · [BTCFi x Core](https://medium.com/bifrost/btcfi-by-bifrost-x-core-partnership-480123037e9f) · [Oracle Service](https://docs.bifrostnetwork.com/bifrost-network/bifrost-network-architecture/oracle-service)

---

## 7. GitHub — `bifrost-platform`

**확정 org:** https://github.com/bifrost-platform (Verified Domains: bifrostnetwork.com, thebifrost.io · 위치 South Korea · dev@thebifrost.io · @bifrost_network). ❌ `bifrost-io`/`bifrost-finance`(Polkadot BNC)와 무관.

**주요 레포 (총 34개):**

| 레포 | 설명 | 언어 | ★ |
|---|---|---|---|
| [bifrost-node](https://github.com/bifrost-platform/bifrost-node) | 메인넷 노드 클라이언트 (EVM L1) | Rust | 39 |
| [bifrost-relayer.rs](https://github.com/bifrost-platform/bifrost-relayer.rs) | 크로스체인 릴레이어 (CCCP, 현행) | Rust | 12 |
| bifrost-relayer.py | 릴레이어 (**DEPRECATED**) | Python | 7 |
| bifrost-frontier | Substrate용 EVM 호환 레이어(Frontier 포크) | Rust | 2 |
| bifrost-substrate / polkadot-sdk | Substrate/Polkadot SDK 포크 | Rust | - |
| bifrost-snapshots | 체인 스냅샷(노드 동기화) | - | 3 |
| [BIFI](https://github.com/bifrost-platform/BIFI) | DeFi 렌딩 컨트랙트 | Solidity | 27 |
| BiFi-X / BiFi-staking-protocol / BiFi-Bifrost-Extension-Contract | BiFi 계열 컨트랙트 | Solidity | - |
| rust-bitcoincore-rpc | Bitcoin Core RPC 포크(BTC 연동) | Rust | - |

**활동성:** 핵심 레포는 적극 유지 중 — bifrost-node **v2.2.0 (2026-06-24)**, bifrost-relayer.rs **v3.0.0 (2026-06-24)**. 반면 BiFi Solidity 계열은 2021~22년 이후 정체. org 팔로워 67.

**기술 스택:** Substrate(FRAME) + Frontier(EVM), 합의 Aura+GRANDPA, libp2p, 컨트랙트 Solidity. 릴레이어가 ETH/BSC/Polygon/Base/Arbitrum/BTC/Core/Oasys 연결.

**노드/밸리데이터 문서:** 코드 README엔 상세 없음 → GitBook [docs.bifrostnetwork.com](https://docs.bifrostnetwork.com/bifrost-network/running-a-node)에 정리 (Basic/Full/Endpoint 노드, Aura·GRANDPA·ImOnline 세션키). 별도 docs/SDK/wallet 전용 레포는 없음.

---

## 8. 일본 기관 / 파트너십 (BTCFi·스테이블코인 축)

### JPYC vs JPYSC — 결정적 구분 (혼동 금지)

| 구분 | **JPYC** | **JPYSC** |
|---|---|---|
| 발행사 | JPYC Inc. | SBI신세이신탁은행 (SBI + Startale) |
| 법적분류 | 자금이동형(~Type II), 100만엔 한도 | **신탁형(Type III), 한도 없음** |
| 발행 | 2025-10-27 (JPYC EX) | 2026-06-24 |
| 바이프로스트 연관 | ✅ **활용** (발행사 아님) | ❌ **직접 연관 근거 없음** |

### JPYC × 바이프로스트 (활용 관계, 발행사 아님)
- **(A) 더블점프도쿄(DJT) 제휴 (2025-10-23):** DJT의 기업용 지갑 **N.suite**에 BTCFi/BtcUSD/BiFi 통합, **BTC/JPYC 기업 재무·급여·정산 프레임워크** 공동설계. "일본 최초 기업 차원 스테이블코인 실무 운용". [Medium](https://bifrost.medium.com/bifrost-double-jump-tokyo-partnership-announcement-dc4685112106) · [디지털데일리](https://m.ddaily.co.kr/page/view/2025102309382762365)
- **(B) 해시포트 월렛 연동 (2026-06-01):** BTCFi가 HashPort Wallet에 통합 → **JPYC 예치 시 연 약 4.0% 고정수익**(락업·만기 없음). 3개월 여름 캠페인. 발표 직후 6/4 BFC 30%+ 급등. ※ 제공주체는 싱가포르 Bifrost(BTCFi Partners), 해시포트/JPYC 발행사 아님 명시. [news1](https://www.news1.kr/amp/finance/blockchain-fintech/6187719) · [JinaCoin(일)](https://jinacoin.ne.jp/jpyc-bifrost-hashport-20260602/)

### 해시포트 (HashPort) — 두 실체 구분
- ✅ **HashPort Wallet** (HashPort Inc., 2018 설립): EXPO2025 오사카 공식 결제앱 출신, 100만+ 다운로드, JPYC·USDC 지원 → **바이프로스트 제휴 대상**
- ❌ **hashport bridge** (hashport.network): 별개 브릿지, 2026-05-31 영구 폐쇄. 무관.
- (참고) 스미토모미쓰이신탁클럽 × 해시포트: 다이너스/트러스트클럽 포인트→JPYC 교환(2026-06-01). 바이프로스트 무관하나 해시포트가 JPYC 핵심 지갑 인프라임을 시사.

### 기타 일본 기관 (시간순)
- **2024-09-26:** Japan Open Chain(JOC) 전략적 투자. 크로스체인 기술지원, BTCFi DApp/브릿지 배포. (JOC는 소니·NTT도코모·후지쯔·덴츠 협력 엔화 SC 인프라 L1)
- **2024-11-29:** **비트트레이드(BitTrade, 구 Huobi Japan, FSA 인가)** — BTCFi 첫 일본 노드 검증자 합류
- **2025-02 말:** AWS Partner Network(APN) 가입
- **2025-03-04:** **일본 핀테크협회(FAJ)** Web3 부문 가입 (PayPal·SBI·미즈호·스미토모미쓰이 등 참여)
- **2025-08-13:** **SBI Digital Finance**와 BtcUSD 활용사례·규제준수 BTC 관리 프레임워크 공동개발 논의 (정식 MOU 아닌 "논의" 단계)
- **2025-11-04경:** **BCCC(블록체인 추진 협회)** 가입
- AI Fusion Capital(일본 AI 투자사) — 검증자 운영

출처: [SBI Medium](https://bifrost.medium.com/bifrost-network-initiates-development-discussions-with-sbi-digital-finance-for-btcusd-usecases-06cf5fca798e) · [BitTrade 디지털데일리](https://m.ddaily.co.kr/page/view/2024112914160416915) · [JOC Medium(한)](https://medium.com/bifrost-blog-kor/바이프로스트-일본-메인넷-japan-open-chain에-투자-5f4f86f0b828) · [FAJ cryptonews](https://cryptonews.com/news/bifrost-bfc-joins-fintech-association-of-japan-alongside-paypal-sbi-and-mizuho/) · [BCCC blockchainreporter](https://blockchainreporter.net/bifrost-network-joins-bccc-japan-cross-chain-innovation-and-strengthening-of-btcfi-ecosystem/)

---

## 9. 기타 글로벌·국내 협력 + 자체 스테이블코인 행보

- **Core / Stacks / XLink·ALEX:** BTCFi·BtcUSD·sBTC 연동 (비트코인 정렬 생태계)
- **가이아 프로토콜(Gaia Protocol):** 공식 파트너
- **파이랩 자체 SC 상표 출원 (2025-07-03, KIPRIS):** **MJPY(엔)·MKRW(원)·MUSD(달러)** 3건 → 자체 다통화 스테이블코인 인프라 구상. (7/6 BFC 11% 급등) [ainvest](https://www.ainvest.com/news/pilab-technology-files-trademarks-stablecoins-2507/)

---

## 10. 온체인 조회 방법 (퀵 레퍼런스)

| 목적 | 도구 / 주소 |
|---|---|
| BFC ERC-20 트랜잭션·홀더 | [Etherscan](https://etherscan.io/token/0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c) · [Ethplorer](https://ethplorer.io/address/0x0c7d5ae016f806603cb1782bea29ac69471cab9c) |
| BFC (Fantom) | [FTMScan](https://ftmscan.com/token/0x84c882a4d8eb448ce086ea19418ca0f32f106117) |
| 메인넷 네이티브 BFC·시스템 컨트랙트 | 익스플로러 `explorer.mainnet.bifrostnetwork.com` + JSON-RPC `public-01.mainnet.bifrostnetwork.com/rpc` |
| 브릿지 플로우 (Eth/BSC/Polygon/Base/Arb) | 각 체인 익스플로러에서 위 **Socket 주소** 이벤트 로그 파싱 |
| 비트코인 peg-in/out | Bitcoin Socket `0x73A9E443...` + Registration Pool `0x...0100` 이벤트 → mempool.space 교차확인 |
| 가격/공급/플랫폼 목록 | [CoinGecko](https://www.coingecko.com/en/coins/bifrost) · [CoinMarketCap](https://coinmarketcap.com/currencies/bifrost/) |
| 컨트랙트 ABI/소스/deployment | [GitHub bifrost-platform](https://github.com/bifrost-platform) (relayer.rs, BiFi-*-Contract) |
| 커스텀 대시보드 | Dune Analytics — ETH 토큰 + 각 체인 Socket 주소 기준 직접 구축 (전용 공식 대시보드 미확인) |

---

## 11. 후속 조사가 필요한 미확정 항목

1. 공식 **BSC BFC 토큰 컨트랙트** (가짜 `0xf4b5cd30...` 제외한 진짜)
2. **BiFi/Biport의 구체 EVM 컨트랙트 주소** → bifrost-platform deployment 파일 또는 앱에서 확보
3. BFC 현재 정확 공급량 (40억 설계 vs 시장데이터 차이 — 메인넷 전환 토크노믹스)
4. eBTC/BitVM 관련 서술의 진위 (타 프로젝트 혼동 여부)
5. JPYSC–바이프로스트 향후 연관 가능성 (현재 근거 없음, SBI 협력은 별개 실재)

---

### 주요 1차/공식 출처
[PiLab](https://www.pilab.co/) · [Bifrost Network](https://bifrostnetwork.com/) · [공식 docs](https://docs.bifrostnetwork.com/) · [GitHub bifrost-platform](https://github.com/bifrost-platform) · [공식 Medium](https://medium.com/bifrost) · [Etherscan BFC](https://etherscan.io/token/0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c) · [CoinGecko](https://www.coingecko.com/en/coins/bifrost) · [CoinMarketCap](https://coinmarketcap.com/currencies/bifrost/)
