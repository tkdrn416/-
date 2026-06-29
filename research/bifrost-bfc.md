# Bifrost (BFC) 사전 리서치 노트

> 파이랩테크놀로지(PiLab Technology)가 개발한 **Bifrost Network / BFC**에 대한 사전 조사 문서.
> 앞으로의 루프(온체인 활동 · GitHub · 일본 기관 · 기업 협력)를 위한 기준 자료.
>
> - 작성일: 2026-06-29
> - 리서치 방식: 다중 소스 웹 검색 → 소스 페치 → 3표 적대적 검증(claim 25건 중 25건 confirmed, 0건 기각)
> - **중요 구분:** 이 문서의 대상은 **BFC = Bifrost Network**(한국 파이랩테크놀로지 L1)이며,
>   **BNC = Bifrost Finance**(폴카닷 파라체인)와는 **전혀 무관한 별개 프로젝트**임. 혼동 금지.

---

## 0. 핵심 요약 (TL;DR)

- **Bifrost Network(BFC)** 는 한국 파이랩테크놀로지가 만든 **Substrate 기반, EVM 호환 Layer-1** 블록체인.
  - 블록 생성: **Aura**, 파이널리티: **GRANDPA**, 검증자 모델: **라운드 기반 DPoS(위임지분증명)**.
  - 메인넷 ChainID **3068 (0xbfc — BFC 티커에서 따옴)**, 테스트넷 ChainID **49088**.
  - 네이티브 가스 토큰: **BFC**.
- **GitHub 개발은 활발함.** `bifrost-platform` 조직(34개 레포). 코어 노드와 크로스체인 릴레이어 모두
  리서치 시점(2026-06-29) 기준 **며칠 전(2026-06-24~26)에 릴리스/푸시** 됨.
- **일본 진출이 공격적.** SBI Digital Finance(SBI홀딩스 자회사)와 BTC 담보 스테이블코인(btcUSD) 협력,
  도쿄 상장사 AI Fusion Capital과 파트너십(검증자 운영), 일본 핀테크협회·JCBA·BCCC 가입.
- **관련 제품:** BiFi(DeFi 제품, 상대적으로 오래됨) → 현재는 btcUSD / BTCFi로 무게 중심 이동 추정.

---

## 1. 온체인 / 기술 구조 (영역 1)

### 1.1 체인 아키텍처
- **유형:** 퍼미션리스 Substrate 기반 EVM 호환 L1 (Frontier 사용).
- **블록 생성:** Aura / **파이널리티:** GRANDPA / **검증자 선출:** 라운드 기반 DPoS.
- **ChainID:**
  - 메인넷 **3068** (`0xbfc` — BFC 티커를 16진수로 표현, 의도적 네이밍)
  - 테스트넷 **49088**
  - `chainid.network/chain/3068`, `chainlist.org/chain/3068` 에서 독립 교차 확인됨.
- **신뢰도:** 높음 (코어 레포 runtime 소스 `runtime/mainnet/src/lib.rs`에서 직접 확인).

### 1.2 BFC 토큰 이코노믹스 / 스테이킹
- **검증자 되기:** BFC를 본딩(bonding)하여 candidate 풀에 진입.
- **위임(delegation/nomination):** 비검증자는 candidate에게 BFC를 위임.
- **선출:** 매 라운드마다 총 지분(self-bond + 위임) 상위 N개 candidate만 블록 생성에 선정.
- **수수료:** 검증자는 설정 가능한 커미션 부과.
- **보상:** **매일 자동 복리(auto-compounding)** — 동일 검증자에게 재스테이킹되어 수수료 절약.
- **리퀴드 스테이킹:** **Biquid** 서비스로 가능. 트랜잭션당 최대 **500,000 BFC** (계정당 한도는 없음).
- **신뢰도:** 높음 (공식 docs + Bifrost Medium 직접 확인).

### 1.3 크로스체인 (CCCP)
- **릴레이어:** `bifrost-relayer.rs` (Rust) — 기존 Python `bifrost-relayer.py`는 아카이브/폐기됨.
- **프로토콜:** **CCCP (Cross-Chain Communication Protocol)** — 크로스체인 트랜잭션 처리 + 가격 피드 등 데이터 전파.
- **통합 체인 9개:** Bifrost, Ethereum, BSC, Polygon, Base, Arbitrum, Bitcoin, Core, Oasys.
- **신뢰도:** 높음 (GitHub README + API 확인).

### 1.4 온체인 인프라 (조회 대상)
- **메인넷 익스플로러:** `explorer.mainnet.bifrostnetwork.com` (**Blockscout** 기반 → REST API v2 보유).
- **테스트넷 익스플로러:** `explorer.testnet.bifrostnetwork.com`.
- **공개 RPC(JSON-RPC):** `public-01/02.mainnet.bifrostnetwork.com/rpc` (thirdweb 등에도 등재).
- **BFC ERC-20(이더리움):** `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c` — 브릿지된 BFC, Etherscan 추적 가능.

### ⚠️ 온체인 분석 가능성 / 현재 환경 제약 (★ 중요)
현재 이 실행 환경에서는 **직접 온체인 조회가 막혀 있음** (2026-06-29 테스트):
- **직접 `curl`:** 네트워크 정책 allowlist가 GitHub·패키지 레지스트리만 허용 →
  RPC/익스플로러/CoinGecko/DefiLlama 모두 **403 정책 차단(connect_rejected)**.
- **WebFetch:** Anthropic 인프라 경유로 일반 웹은 되지만, 익스플로러·Etherscan·CoinGecko API는
  **안티봇(Cloudflare)으로 403** → 원시 트랜잭션/브릿지 로그 조회 불가.
- **WebSearch:** 요약 스니펫만 가능, 원시 온체인 쿼리 불가.
- **결론:** 트랜잭션·브릿지 기록·`eth_getLogs` 같은 **실제 온체인 분석은 현재 환경에선 불가.**
  → 이를 풀려면 **환경의 네트워크 정책을 완화**(전체 egress 또는 커스텀 allowlist에
  `*.bifrostnetwork.com`, `api.coingecko.com`, `api.llama.fi`, `api.etherscan.io` 추가)해야 함.
  정책 완화 후엔 RPC `POST`(eth_getBlockByNumber/eth_getLogs/eth_call)와 Blockscout API로 정밀 분석 가능.

### ⚠️ 미확인 (네트워크 정책 완화 후 보완)
- **TVL, 일일 트랜잭션 볼륨, BFC 총/유통 공급량, 활성 검증자 수** — 요청 영역이나 환경 제약으로 미확보.

---

## 2. GitHub 개발 활동 (영역 2)

> 아래는 **공개 GitHub REST API 직접 조회**(2026-06-29 실측) 기반. MCP 스코프(`tkdrn416/-` 한정)와
> 무관하게 `curl api.github.com/...`로 전수 조회 가능함(레이트리밋 15,000/시간). 시간에 따라 수치는 변동.

### 2.1 조직: `bifrost-platform` (org id 45643413)
- **공개 레포 34개** = 비포크 활성 ~13개 + 포크 ~12개(polkadot-sdk, bifrost-frontier, ethers-rs, subxt,
  evm, DefiLlama-Adapters, rust-bitcoincore-rpc 등) + 아카이브 ~9개.
- topics: `bfc`, `bifrost`, `cross-chain-communication-protocol`, `evm`, `rust` → **BNC 아닌 BFC 확정.**

### 2.2 코어 노드: `bifrost-node` (★ 가장 활발)
- 언어: **Rust 64.6% / TS 31.7% / Solidity 3.3%**. 커밋 **318개**, 스타 39, 포크 16.
- 릴리스: **v2.2.0 (2026-06-24)**, v2.1.0 (2025-09-11), v2.0.1 (2024-12-02) → 연 2~3회 메이저, 마이너 잦음.
- 최근 커밋: 2026-06-25 "deps: update docker setup", 메인넷 런타임 v2045 (2026-06-16) → **리서치 시점 활발.**

### 2.3 릴레이어: `bifrost-relayer.rs` (CCCP 크로스체인)
- Rust. 커밋 **225개**, 릴리스 최신 **v3.0.0 (2026-06-24)**, v2.2.3 (2026-05-06). 스타 12, 포크 6.
- 🔑 최근 커밋 "**fix: sign psbt through snapshot members**" (2026-06-18) → **비트코인 PSBT 멀티시그/임계서명**
  기반 BTC 브릿지 구현 정황. btcUSD/BTCFi(SBI 협력)와 코드 레벨에서 연결됨.
- 구버전 `bifrost-relayer.py`는 아카이브(2025-04).

### 2.4 기타 활성 레포
- `asset-info-v2` (Python, 56커밋, v3.0.7 2026-03): 자산 메타데이터 레지스트리. 미러봇 태깅 자동화.
- `bifrost-snapshots` (4커밋, 2026-03): 노드 체인 스냅샷 배포.
- `Bifrost-Node-AdminPanel` (JS, 25커밋, 2026-02): **withdraw(브릿지 출금) UI** 포함 관리 패널.
- `bifrost-frontier` (Rust 포크, 2026-03): EVM 레이어(Frontier) 커스텀.

### 2.5 BiFi 관련 (레거시)
- `BIFI`(15커밋, 전부 2021, 스타27 — Theori/CertiK 감사보고서), `BiFi-staking-protocol`(2022-01 푸시 후 휴면),
  `BiFi-X`, `BiFi-Bifrost-Extension-Contract` 등 → 모두 **2021~22년 이후 정체**. BiFi는 구 제품, BTCFi로 이행.

### 2.6 개발 인력 구조 (주목)
- **핵심 기여자 `dnjscksdn98`** 이 노드(262/318)·릴레이어(156/225) **양대 핵심 레포 모두에서 압도적 1위**
  → 소수 코어팀 집중, **버스 팩터(bus factor) 리스크** 존재.
- 보조: `alstjd0921`(노드53/릴레이어58), `Alex Won`(머지/PR 관리), `noah-jang`, `jormal`(asset-info),
  `woogie96`(admin panel), `pilab-*` 계정(파이랩 직원), `jonghyuplee`(초기 BiFi).

---

## 3. 일본 기관 / 기업 협력 (영역 3)

### 3.1 SBI Digital Finance (★ 플래그십)
- **상대:** SBI Digital Finance (일본 **SBI홀딩스 자회사**, HashHub Lending 운영).
- **내용:** 일본 내 기관 비트코인 채택 가속 — **BTC 담보 스테이블코인 btcUSD** 유스케이스,
  비트코인 통합 금융서비스, **일본 법 / FSA 규제 준수 BTC 관리 프레임워크** 구축.
- **발표:** 2025-08-13 (Bifrost 공식 Medium).
- **⚠️ 뉘앙스:** Bifrost 본인 표현은 "development discussions를 시작"으로, "파트너십 체결"보다 약함.
  **확정/출시된 제품이 아닌 미래지향적 의향** 단계. 2차 매체 헤드라인은 이를 완료된 "파트너십"으로 과장하는 경향.

### 3.2 AI Fusion Capital Group (AIF)
- **상대:** 도쿄 상장, 일본 AI 중심 투자사.
- **내용:** AIF가 **도쿄에서 Bifrost Network 검증자(validator) 운영**, BTCFi를 비트코인 트레저리 관리에 채택.
- AIF는 실제 공개 BTC 보유사로 확인됨(약 24.63 BTC, bitcointreasuries.net).
- 2025년, 자체 홍보성이나 존재 자체는 다툼 없음.

### 3.3 일본 업계 단체 가입 (신뢰도: 중)
- **일본 핀테크협회 (FAJ):** ~2025-03 가입. FAJ 멤버에 PayPal, SBI홀딩스, 미쓰이스미토모, 미즈호 포함.
- **JCBA (일본 암호자산 비즈니스 협회):** 가입 (Bifrost Medium).
- **BCCC (Blockchain Collaborative Consortium):** 2025-11 가입. BCCC 공식 멤버 리스트에 "株式会社Bifrost" 확인.
- **⚠️ 캐비엇:** 2차 보도가 암호화폐 PR성 매체 위주, BCCC 클레임은 검증 투표 2-1. 가입 자체는 평범한 수준이며
  BCCC는 공식 리스트로 확인됨.

---

## 4. 기타 기업 / 생태계 협력 (영역 4)

- **BiFi (DeFi 제품):** 동일 조직 산하. 단 코어 레포 2022-01 이후 휴면 → btcUSD/BTCFi로 대체/이행 추정.
- **CCCP 통합 체인들(생태계 연결):** Oasys, Core 등 — 단순 기술 통합인지 별도 사업 제휴인지는 미확인.
- **파이랩테크놀로지 자체:** 스테이블코인 관련 상표 출원 정황(ainvest 보도, 신뢰도 낮음 — 확인 필요).

### ⚠️ 미확인 (다음 루프 보완)
- 일본 외 기업/엔터프라이즈 협력의 범위와 현황 (Japan Open Chain, Oasys, Core 등 각각의 성격/단계).

---

## 5. 핵심 미해결 질문 (Open Questions)

1. **온체인 수치:** 현재 TVL, 일일 트랜잭션 볼륨, BFC 총/유통 공급량, 활성 검증자 수는?
2. **SBI 협력 현황:** "development discussions"를 넘어 정식 계약/btcUSD 제품 출시로 진전됐나? FSA 준수 프레임워크 실제 런칭 여부?
3. **BiFi 상태:** 핵심 스테이킹 레포가 2022-01 이후 휴면 — BiFi는 여전히 운영 중인가, btcUSD/BTCFi로 대체됐나?
4. **일본 외 협력:** Oasys, Core, Japan Open Chain 등 기타 엔터프라이즈 협력의 범위/단계는?

---

## 6. 리서치 방법론 & 신뢰도 경고

- **강한 1차 소스 기반:** 체인 아키텍처/토큰 메커니즘/GitHub 활동은 GitHub REST·Linguist API,
  공식 Bifrost docs·Medium, EVM 체인 레지스트리 등 1차 소스로 검증.
- **일본 파트너십은 일부 2차/PR 매체 의존**(blockchainreporter, beincrypto, ittimes, fxdailyreport — 하위 티어).
  단 주요 건은 모두 Bifrost 공식 Medium으로 교차 확인, BCCC는 공식 멤버 리스트로 확인.
- **파트너십 성숙도 주의:** 여러 건(특히 SBI)이 Bifrost 본인 표현상 "논의 중"/"목표" 단계. 2차 헤드라인이 완료된 것처럼 과장함.
- **시점 민감성:** GitHub 지표(커밋/스타/포크/릴리스/푸시일/언어비율)는 2026-06-29 검증값이며 지속적으로 변동.
  당시 매우 신선했음(node v2.2.0, relayer v3.0.0 모두 2026-06-24 릴리스).
- **docs.bifrostnetwork.com 직접 페치는 HTTP 403(안티봇)** → 인용은 검색 인덱스 스니펫 경유(verbatim·교차확인됨).
- **정체성 구분:** BFC(파이랩 Bifrost Network) ≠ BNC(폴카닷 Bifrost Finance 파라체인) — 반복 확인됨.
- **데이터 접근 경로(이 환경):** GitHub 공개 API는 직접 `curl` 가능(권장). 그 외 일반 웹은 WebFetch/WebSearch.
  온체인 RPC·익스플로러·시세 API는 네트워크 정책+안티봇으로 현재 차단 → §1.4 참조.

---

## 7. 주요 소스 (품질 등급)

| 품질 | URL |
|------|-----|
| primary | https://github.com/bifrost-platform/bifrost-node |
| primary | https://github.com/bifrost-platform/bifrost-relayer.rs |
| primary | https://github.com/orgs/bifrost-platform/repositories |
| primary | https://docs.bifrostnetwork.com/bifrost-network/staking/staking-guide/stake-bfc |
| primary(레지스트리) | https://chainid.network/chain/3068 · https://chainlist.org/chain/3068 |
| 1차(공식 발표) | https://bifrost.medium.com (SBI btcUSD / AIF 파트너십 / BFC staking 소개글) |
| secondary | https://beincrypto.com/south-koreas-bifrost-partners-with-japans-sbi-to-drive-bitcoin-adoption/ |
| secondary | https://blockchainreporter.net/bifrost-network-joins-bccc-japan-cross-chain-innovation-and-strengthening-of-btcfi-ecosystem/ |
| secondary | https://www.ittimes.com/news/articleView.html?idxno=79055 |
| 멤버리스트 | https://bccc.global/ja/members (株式会社Bifrost) |
