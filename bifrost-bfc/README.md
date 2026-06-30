# Bifrost (BFC) 리서치 — 파이랩테크놀로지 · 인덱스

> 한국 **파이랩테크놀로지(Pi Lab Technology)**의 **Bifrost Network / BFC (바이프로스트)** 리서치 모음.
> 최종 갱신: **2026-06-30** · 용도: 정기 모니터링 루프의 배경지식 + 기준값(baseline).
> 📖 **처음 읽는 순서:** 이 README(전체 그림) → `01-overview`(기본) → `02-deep-dive`(정밀) → `03-monitoring-baseline`(루프용).

## ⚠️ 절대 혼동 금지
| ✅ 우리 대상 | ❌ 혼동 대상 |
|---|---|
| **BFC** = 한국 파이랩 Bifrost Network (EVM L1 + BTCFi) | **BNC** = Polkadot Bifrost Finance |
| `bifrostnetwork.com`, `thebifrost.io`, `medium.com/bifrost`, GitHub `bifrost-platform`, X `@Bifrost_Network` | `bifrost.io`, `bifrost.io/blog`, GitHub `bifrost-io`/`bifrost-finance`, vDOT/SLP/parachain |
| ERC-20 `0x0c7D5ae0…Cab9c`, 메인넷 chainId **3068** | — |

> ⚠️ CoinCodex·CMC "CMC AI updates" 등 일부 집계가 BNC/BFC를 섞음. DOT/Polkadot 항목은 항상 버릴 것.

---

## 📁 문서 구성

| 파일 | 내용 | 언제 보나 |
|---|---|---|
| **[01-overview.md](./01-overview.md)** | 회사·토큰·메인넷·브릿지·GitHub·일본 기관 기본 정리 + 연혁 | 전체 그림 파악 |
| **[02-deep-dive.md](./02-deep-dive.md)** | 온체인 실측, **전체 컨트랙트 주소 풀셋**, BTC vault 구조, 토크노믹스, 일본 사업 타임라인, **검증/정정** | 정확한 사실·주소 확인 |
| **[03-monitoring-baseline.md](./03-monitoring-baseline.md)** | **10개 차원 기준값 + 매 루프 재실행 쿼리/디프 대상** (+부록: 체크리스트·확장후보) | 루프 돌릴 때 매번 |
| **[data/validators-snapshot.md](./data/validators-snapshot.md)** | 검증자 24개 온체인 주소(controller/stash) | 노드 변동 대조용 |
| **[data/native-holders-analysis.md](./data/native-holders-analysis.md)** | 네이티브 홀더 전수분류·실질 BFC 익스포저(스테이킹/BiFi 합산)·BiFi 예치추적 | 홀더 분석 |
| **[data/foundation-tracking.md](./data/foundation-tracking.md)** | **★ 재단 추적** — TOP100 재단 플래그·재단 클러스터·물밑 프로젝트 감지 신호 | 재단 움직임 추적 |

충돌 시 우선순위: **03 > 02 > 01** (최신·정정 반영순).

---

## 핵심 요약 (executive summary)

**회사:** 2017년 설립, 박도현 CEO·이종협 CTO·유창현 COO, 서울 성수동, 직원 ~38명. 현재 "기관용 비트코인 금융 레이어 + 스테이블코인 인프라"로 재포지셔닝.

**제품:** Bifrost Network(EVM L1, chainId 3068, DPoS+Aura/GRANDPA, Substrate+Frontier) · **BTCFi/BtcUSD**(네이티브 BTC 담보 스테이블, 3.5%, CDP $9.17M) · **BiFi**(렌딩 $6.94M) · **Biquid**(리퀴드스테이킹 $3.17M, stBFC) · **Everdex**(DEX $2.69M) · Biport/Pockie(지갑) · The BIFROST Bridge(CCCP, 9체인).

**토큰:** BFC. ERC-20 `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c`. 메인넷 네이티브 가스코인. 시총 ~$16.6M(2026-06). 공급: 40억 발행 → 2022년 40%(16억) 소각 → 메인넷서 캡 폐지·인플레이션(코드 13%). (StableDAO 소각은 계획 발표만, 집행 미확인). 상장 업비트·빗썸·코빗·HTX.

**일본 전략(BTCFi 축):** HashPort Wallet(JPYC 4% 렌딩) · DJT N.suite · SBI Digital Finance · Animoca Brands Japan · AI Fusion Capital(검증자) · BitTrade(검증자) · JOC·MOIN · 협회(JCBA/FAJ/BCCC). **JPYC는 활용만, 발행 아님. JPYSC와는 무관.**

---

## 📌 자주 쓰는 레퍼런스

### 컨트랙트 (메인넷 Socket / Vault)
| 체인 | ChainID | Socket | Vault |
|---|---|---|---|
| Bifrost | 3068 | `0xd551F33Ca8eCb0Be83d8799D9C68a368BA36Dd52` | `0xD85EB87caB9041ad00764b95796702b1104F42D7` |
| Ethereum | 1 | `0x4A31FfeAc276CC5e508cAC0568d932d398C4DD84` | `0x2F95C102Cc26875406BC689Fb01aE382B82AA535` |
| BSC | 56 | `0xb5Fa48E8B9b89760a9f9176388D1B64A8D4968dF` | `0x78ae4c0FD4f02CA79A2d8738d3369A4Bc5D4E323` |
| Bitcoin Socket(메인넷) | 10000 | `0x73A9E443F51eE40C1469A740D9CCf0118e8FD9ca` | (동적 PSBT vault) |

(Polygon/Base/Arbitrum/Oasys 포함 전체 표 → [02-deep-dive.md](./02-deep-dive.md) B-1)

토큰: BFC ERC-20 `0x0c7D5ae0…Cab9c` · BiFi ETH `0x2791BfD60D232150Bff86b39B7146c0eaAA2BA81` · BiFiB(BSC) `0x1378e33a09d8bd8e449CFD8A5aBCa0439286d645` · **BtcUSD(Bifrost3068) `0x6906Ccda405926FC3f04240187dd4fAd5DF6d555`**
❌ 가짜(차단): BSC `0xf4b5cd30…09ec`, BSC `0x5Dec5345…68dC9`

### 온체인 조회 엔드포인트
- ETH ERC-20: `https://api.ethplorer.io/getTokenInfo/0x0c7D5ae0…Cab9c?apiKey=freekey`
- 메인넷 RPC: `https://public-01.mainnet.bifrostnetwork.com/rpc` (chainId 3068)
- 메인넷 익스플로러 백엔드(Blockscout): `https://explorer-backend.mainnet.thebifrost.io/api/v2/...`
- GitHub: `https://api.github.com/orgs/bifrost-platform/...`

### 핵심 추적 지표 (베이스라인 2026-06-29~30)
- 거래소 보유: **업비트 ≈348M · 빗썸 ≈143.7M** (클러스터 잔액 합)
- 검증자: **24개**(Full15/Basic9), 스테이킹 **406M BFC** · 주소목록 [data/validators-snapshot.md](./data/validators-snapshot.md)
- 브릿지 Vault TVL: ETH **BFC 863.5M**+USDC$607K · BSC **BTCB 44.3**(~$4.7M)
- **DeFi:** BTCFi CDP $9.17M(BtcUSD 8.06M) · **BiFi 렌딩 $6.94M** · **Biquid 리퀴드스테이킹 $3.17M**(stBFC) · Everdex $2.69M · 체인 TVL $11.84M
- 소셜: TG Notice 860/Global 7,129 · Medium 7,500 · X ~82K

### 🔔 최우선 감시 신호
1. Vault/소각 주소 대형 이동, 거래소 클러스터 잔액 급변(순유입=매도압력)
2. **BFC의 BitTrade(일본) 상장**, 빗썸/업비트 입출금 중단(`assetsstatus`=0)
3. HashPort/N.suite JPYC 렌딩 **첫 TVL 수치** + **BtcUSD 발행량 급증**(교차검증)
4. **CCCP v2 메인넷 전환** (현재 testnet)
5. 검증자 집합 변동, 신규 GitHub 레포/릴리스, 워터마크(2026-06-02) 이후 신규 뉴스

---

## 거래소 보유 클러스터 (확정 — 03 차원8 상세)
- **업비트** ≈ 348M BFC: 콜드허브 `0x50F187Ef…955E`(332.5M) + 핫월렛들 — 사용자 출금이력으로 확정
- **빗썸** ≈ 143.7M BFC: 콜드 `0xDCd52f5f…8935`(137.5M) + 핫 `0x39528D59…084D`(6.3M) — 앱 공시값 143,666,510과 온체인 합 일치로 확정
- 추적: `explorer-backend.mainnet.thebifrost.io` 잔액 합 일별 델타 = 거래소 순유입/출 프록시

## 빗썸 공시 자동수집 (해결 — 03 차원8)
- 빗썸 정확 공시값(내부유통량/보유자/순입금)은 **로그인+봇차단**으로 자동수집 불가 → **온체인 클러스터 합**(143.7M)으로 대체(공시 143.67M과 일치).
- 공개 API는 자동수집 OK: 빗썸 `api.bithumb.com/public/ticker/BFC_KRW`·`/assetsstatus/BFC_KRW`(입출금 중단 감지), 업비트 `api.upbit.com/v1/ticker?markets=BTC-BFC`(BTC마켓만).

## 10개 모니터링 차원 (03 문서)
1 상위홀더 **★네이티브 우선★** · 2 노드/검증자 · 3 브릿지+Vault TVL+BtcUSD · 4 트랜잭션 **★네이티브 우선★** · 5 GitHub · 6 뉴스 · 7 일본파트너 · 8 한국거래소(업비트/빗썸) · 9 글로벌거래소 · 10 소셜
> ※ 차원1·4는 메인넷 전환 이후 **네이티브 체인(3068) 데이터가 핵심**, ETH ERC-20은 보조.

## 미해결 / 후속 과제 (난이도 높음)
- 온체인 거버넌스(제안/투표) 추적 가능 여부
- 토큰 언락/베스팅 일정 (대형 컨트랙트 해제 패턴)
- BTC vault 멀티시그 임계값(M-of-N)
- 검증자 실명↔주소 매핑(Substrate identity 부재로 원천 제약)
- (해결됨) `0x4bAE7…6Ee` 87M = **BiFi BFC 렌딩 예치풀**(미식별 콜드 아님) · `0xcF2FC1d3` = BiFi BtcUSD 풀
