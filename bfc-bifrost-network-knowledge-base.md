# BFC / Bifrost Network — 사전 리서치 지식베이스

> **대상**: **Bifrost Network (티커 BFC)** — 한국 블록체인 기업 **파이랩테크놀로지(PiLab Technology)**가 개발한 EVM 호환 레이어1 멀티체인 인프라.
> **⚠️ 절대 혼동 금지**: 폴카닷 리퀴드 스테이킹 **Bifrost (BNC)** 와는 **완전히 다른 프로젝트**(다른 팀·체인·토큰). 같은 "바이프로스트" 이름이지만 무관.
> 작성일: 2026-06-29 · 용도: 향후 루프(온체인 활동·깃허브·일본 기관·기업 협력) 질의용 사전지식.

---

## 0. ⚠️ BFC vs BNC 구분표 (가장 중요)

| 구분 | **BFC (이 문서)** | BNC (혼동 대상) |
|---|---|---|
| 프로젝트 | **Bifrost Network** | Bifrost (Staking Yield Layer) |
| 개발사 | **파이랩테크놀로지 (한국)** | (별개 팀) |
| 체인 | 자체 EVM 호환 L1 (Substrate 기반) | 폴카닷/쿠사마 파라체인 |
| 핵심 사업 | **멀티체인 미들웨어 + BTCFi(비트코인 담보 DeFi)** | 리퀴드 스테이킹(vDOT 등) |
| 최대공급 | **42억 BFC** | 8천만 BNC |
| 키워드 | CCCP, 릴레이어, BtcUSD, SBI, 일본 | vToken, SLPx, 폴카닷 |

> 루프 중 "바이프로스트"라는 단어만 보이면 항상 **BFC(파이랩/Network)** 기준으로 해석. BNC/폴카닷/vToken/SLPx 얘기가 나오면 그건 다른 프로젝트이므로 분리해서 처리.

---

## 1. 회사 — 파이랩테크놀로지 (PiLab Technology)

| 항목 | 내용 |
|---|---|
| 설립 | 2017년 9월 7일 |
| 공동창업 | 박도현(대표), 이종협, 유창현 |
| 본사 | 서울 성동구 |
| 직원수 | ~38명 (최근 1년 ~20→50명대로 빠르게 확대) |
| 투자 | 시드 40억 + 시리즈A 100억 (한국투자파트너스·스틱벤처스 등 70억 규모 참여 보도) |
| 슬로건 | "The Full-Stack Builder for Institutions" (pilab.co) |
| 주력 제품 | **Bifrost Network**(자체 L1) + **BTCFi**(비트코인 담보 DeFi) |

이름 유래: 북유럽 신화의 무지개다리 "비프로스트"(미드가르드↔아스가르드) → "블록체인을 잇는 다리".

---

## 2. Bifrost Network 기술 개요

- **정체성**: EVM 호환 L1 블록체인 (Substrate 프레임워크 기반), 멀티체인 미들웨어. BTC·EVM·non-EVM을 연결.
- **CCCP (Cross-Chain Communication Protocol)**: 핵심. 외부검증형 메시지 패싱 네트워크. 분리된 체인 간 안전·신속 메시지 전송.
- **릴레이어 = 코어 검증자**: 밸리데이터가 동시에 릴레이어 역할 → 크로스체인 메시지 전송 + 가격 피드 등 데이터 전파.
- **합의**: PoS. nominator가 validator에게 BFC 위임, 보상/슬래싱. **자동 복리(auto-compounding)** 스테이킹 보상(일 단위).
- **주력 서비스 BTCFi**: BTC 보유자가 비트코인을 담보로 **BtcUSD**(BTC 담보 스테이블코인) 발행 → Bifrost Network 및 BtcUSD 지원처에서 DeFi 활용. 다양한 체인에서 BTC 입금 지원.
- **브릿지 지원 자산**: BFC, BiFi, ETH, USDC, USDT, DAI, BtcUSD, BTCB, WBTC, cbBTC, BTC, BNB, POL, CORE 등.

---

## 3. 토큰 — BFC

| 지표 | 값 | 비고 |
|---|---|---|
| 최대 공급 | **4,200,000,000 BFC** | |
| 총 공급 | ~2.37B BFC (출처별 상이) | |
| 유통 공급 | ~1.39–1.4B BFC | |
| 가격 | **출처별 편차 큼** ($0.0117 ~ $0.0500) | 거래소/시점별 상이 → 루프 시 재확인 필요 |
| 시가총액 | ~$23M ~ $69M (가격에 따라) | |
| 용도 | 가스, 스테이킹(검증/위임), 거버넌스, 브릿지 수수료 | |

> ⚠️ BFC 가격/시총은 소스 간 편차가 커서(거래소·스냅샷 차이) **수치 인용 시 반드시 시점·출처 명기**. 정밀 값 필요 시 CoinGecko/CMC 재조회.

---

## 4. 온체인 — 현황 & 본 환경에서의 조회 가능성

### 이 환경에서 직접 온체인 조회는 **제한적** (중요)
- **직접 차단(403, 조직 이그레스 정책)**: Blockscout 익스플로러(`explorer.mainnet.bifrostnetwork.com`), DefiLlama, 체인 RPC, Subscan API 등 **직접 호출/페이지 fetch 불가**.
- **가능한 것**: Claude 내장 **WebSearch**로 검색엔진에 인덱싱된 익스플로러/DefiLlama/리서치 수치를 **간접 수집** 가능.
- **불가능한 것(현 환경)**: 특정 트랜잭션 해시 조회, 주소별 잔액/이력, 블록 단위 집계, 브릿지 입출금 레코드 실시간 추적 → **RPC/익스플로러 API가 허용된 환경 또는 API 키**가 있어야 함.

### 트랜잭션·브릿지 기록 조회를 제대로 하려면 (루프 전 셋업 권장)
1. **Blockscout API** (`explorer.mainnet.bifrostnetwork.com/api`) 또는 **공개 RPC 엔드포인트**를 이그레스 허용목록에 추가.
2. 또는 **EVM 호환**이므로 표준 `eth_getTransactionByHash`, `eth_getLogs`(브릿지 컨트랙트 이벤트), `eth_getBalance` 등으로 조회 가능 — RPC만 열리면 트랜잭션/브릿지 이벤트 추적 가능.
3. BtcUSD mint/redeem, 브릿지 lock/release는 **컨트랙트 이벤트 로그**로 추적 — 컨트랙트 주소 확보 필요(다음 루프에서 docs/깃허브로 수집 예정).

### 알려진 온체인 지표 (간접/리포트 기준)
- 2024 연간 리포트: **TVL $100M 돌파**, 프로토콜 매출 **$7.92M**.
- DefiLlama에 `chain/Bifrost Network`, `protocol/btcfi`, stablecoin 페이지 존재(수치는 차단되어 미취득 → 재조회 대상).

---

## 5. 깃허브 — `bifrost-platform`

조직: https://github.com/bifrost-platform (총 ~34 repos)

| 레포 | 언어 | 설명 | 최근 업데이트 | ★ |
|---|---|---|---|---|
| **bifrost-node** | Rust | EVM 호환 L1 본체(멀티체인 DApp 올인원 환경) | **2026-06-26** (활발) | 39 |
| **bifrost-relayer.rs** | Rust | 릴레이어 Rust 구현(ETH/BTC/Bifrost/CCCP) | **2026-06-26** (활발) | 12 |
| bifrost-frontier | Rust | EVM 호환 레이어(Frontier 포크) | 2026-03 | 39 |
| polkadot-sdk | Rust | (포크) | 2026-03 | — |
| bifrost-relayer.py | Python | **DEPRECATED** (Rust로 이관됨) | 2022–23 | — |

- **핵심 활성 개발**: `bifrost-node`, `bifrost-relayer.rs` (둘 다 2026-06 최신 커밋, 메인 포커스).
- 릴레이어는 **Python → Rust 마이그레이션 완료**(성능·안전성). 신규는 Rust 버전 사용 권장.
- ⚠️ 본 세션 GitHub MCP 권한은 `tkdrn416/-`로 한정 → `bifrost-platform` repo는 **MCP로 직접 못 읽음**. 깃허브 분석은 WebSearch/WebFetch로 수행하거나, 필요 시 권한 확장 요청.

---

## 6. 일본 기관 & 협력 (루프 핵심 주제) — BTCFi 중심

| 상대 | 내용 | 비고 |
|---|---|---|
| **SBI (SBI Digital Finance / SBI Bank)** | 비트코인 담보 스테이블코인 **BtcUSD** 공동 개발, 규제준수 BTC 운용 프레임워크. 일본 BTC 기관 채택 가속. | 최대 하이라이트 |
| **Fintech Association of Japan (FAJ)** | 가입(2025-03). PayPal·SBI·Mizuho 등과 함께 BTCFi 확산. | |
| **Animoca Brands Japan (ABJ)** | 기업급 BTC 트레저리 솔루션 공동 검증(일본 FSA 규제 대응). | |
| **Japan Open Chain** | 일본 기업 운영 이더리움 호환 퍼블릭 체인과 협력. | |
| **BCCC (Blockchain Collaborative Consortium)** | 일본 블록체인 컨소시엄 가입. | |
| **AI퓨전(일본 상장사)** | 300억원 규모 비트코인 전략 펀드를 **바이프로스트 BTCFi로 운용 개시** (2025-06 보도). | 실제 자금 운용 사례 |

> 일본 전략 = **BTCFi/BtcUSD를 일본 규제권 내 기관 비트코인 금융 인프라로 포지셔닝**. SBI·Mizuho·Animoca·상장사 펀드까지 연결.

---

## 7. 국내·기타 기업 협력

| 상대 | 내용 |
|---|---|
| **한국정보인증(KICA) + CODE** | 3자 MOU(2023-11): Web3 인증 인프라. 파이랩=메인넷 환경, KICA=KYC, CODE=AML/트래블룰(빗썸·코인원·업비트 등 ~60개사 회원). |
| **한국정보인증** | 네임서비스 결합 Web3 인증 인프라 공동 구축, KYC Web3 사업. |
| **FluidTokens (Cardano)** | BIFROST Bridge로 BTC 유휴자본을 Cardano DeFi에 연결(2026-01). |

---

## 8. 루프 대비 — 다음에 채워야 할 빈칸(후속 수집 항목)

1. **온체인 실데이터**: 익스플로러/RPC 허용 시 → 총 트랜잭션·블록·활성주소, 일별 tx, 브릿지 입출금량, BtcUSD 발행/상환량.
2. **컨트랙트 주소 맵**: BFC/BiFi/BtcUSD 토큰, 브릿지·CCCP·스테이킹 컨트랙트 주소(docs/깃허브에서).
3. **BFC 정확 시세/시총**: 시점 명기해 재조회(소스 편차 큼).
4. **깃허브 커밋 활동**: bifrost-node/relayer.rs 커밋 빈도·기여자·릴리스 케이던스(권한 확장 또는 web).
5. **밸리데이터/릴레이어 세트**: 검증자 수, 스테이킹 총량, 탈중앙화 정도.
6. **SBI BtcUSD 진행상황**: 출시 여부·운용 규모 업데이트.

### 환경 셋업 제안 (온체인 분석 제대로 하려면)
- 이그레스 허용목록에 추가: `explorer.mainnet.bifrostnetwork.com`, Bifrost RPC 엔드포인트, `api.llama.fi`, `coingecko.com`.
- 그러면 EVM 표준 RPC + Blockscout API로 **트랜잭션·브릿지·이벤트 로그 직접 조회 가능**.

---

## 9. 출처

- [PILAB 공식](https://www.pilab.co/) · [파이랩 기업정보(THE VC)](https://thevc.kr/pilab) · [넥스트유니콘](https://www.nextunicorn.kr/company/de77a47519f2b948)
- [BIFROST Network Docs](https://docs.bifrostnetwork.com/bifrost-network) · [About BTCFi](https://docs.bifrostnetwork.com/eng.btcfi.one)
- [Bifrost Network Explorer (Blockscout)](https://explorer.mainnet.bifrostnetwork.com/) · [DefiLlama — Bifrost Network](https://defillama.com/chain/Bifrost%20Network)
- [GitHub — bifrost-platform](https://github.com/bifrost-platform) · [bifrost-node](https://github.com/bifrost-platform/bifrost-node) · [bifrost-relayer.rs](https://github.com/bifrost-platform/bifrost-relayer.rs)
- [Messari — Bifrost Network](https://messari.io/project/bifrost-network) · [CoinGecko — BFC](https://www.coingecko.com/en/coins/bifrost) · [CoinMarketCap — BFC](https://coinmarketcap.com/currencies/bifrost/)
- [Bifrost×SBI (BlockchainReporter)](https://blockchainreporter.net/cross-chain-l1-bifrost-network-collaborates-with-sbi-bank-to-expedite-japan-bitcoin-institutional-adoption) · [Bifrost joins FAJ (CryptoNews)](https://cryptonews.com/news/bifrost-bfc-joins-fintech-association-of-japan-alongside-paypal-sbi-and-mizuho/)
- [파이랩·한국정보인증·코드 3자 MOU (Medium)](https://medium.com/bifrost-blog-kor) · [AI퓨전 300억 BTC 펀드, 바이프로스트 BTCFi 운용(전자신문)](https://www.etnews.com/20250630000278)

---

*면책: 본 문서는 사전 리서치용 정보 정리이며 투자 권유가 아님. 수치는 직접 온체인 질의가 차단된 환경에서 공개 자료를 교차 확인해 취합 — 시점·출처별 편차 존재. BFC(파이랩/Network)와 BNC(폴카닷)는 별개 프로젝트임을 항상 유의.*
