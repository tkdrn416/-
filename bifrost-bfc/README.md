# Bifrost (BFC) 리서치 — 파이랩테크놀로지 · 인덱스

> 한국 **파이랩테크놀로지(Pi Lab Technology)**의 **Bifrost Network / BFC (바이프로스트)** 리서치 모음.
> 최종 갱신: **2026-06-29** · 용도: 정기 모니터링 루프의 배경지식 + 기준값(baseline).

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
| **[03-monitoring-baseline.md](./03-monitoring-baseline.md)** | **8개 차원 기준값 + 매 루프 재실행 쿼리/디프 대상** | 루프 돌릴 때 매번 |

충돌 시 우선순위: **03 > 02 > 01** (최신·정정 반영순).

---

## 핵심 요약 (executive summary)

**회사:** 2017년 설립, 박도현 CEO·이종협 CTO·유창현 COO, 서울 성수동, 직원 ~38명. 현재 "기관용 비트코인 금융 레이어 + 스테이블코인 인프라"로 재포지셔닝.

**제품:** Bifrost Network(EVM L1, chainId 3068, DPoS+Aura/GRANDPA, Substrate+Frontier) · **BTCFi/BtcUSD**(네이티브 BTC 담보 스테이블, 3.5%) · BiFi(렌딩) · Biport/Pockie(지갑) · The BIFROST Bridge(CCCP, 9체인).

**토큰:** BFC. ERC-20 `0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c`. 메인넷 네이티브 가스코인. 시총 ~$16.6M(2026-06). 공급: 40억 발행 → 2022년 40%(16억) 소각 → 메인넷서 캡 폐지·인플레이션(코드 13%) → StableDAO 소각. 상장 업비트·빗썸·HTX.

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

토큰: BFC ERC-20 `0x0c7D5ae0…Cab9c` · BiFi ETH `0x2791BfD60D232150Bff86b39B7146c0eaAA2BA81` · BiFiB(BSC) `0x1378e33a09d8bd8e449CFD8A5aBCa0439286d645`
❌ 가짜(차단): BSC `0xf4b5cd30…09ec`, BSC `0x5Dec5345…68dC9`

### 온체인 조회 엔드포인트
- ETH ERC-20: `https://api.ethplorer.io/getTokenInfo/0x0c7D5ae0…Cab9c?apiKey=freekey`
- 메인넷 RPC: `https://public-01.mainnet.bifrostnetwork.com/rpc` (chainId 3068)
- 메인넷 익스플로러 백엔드(Blockscout): `https://explorer-backend.mainnet.thebifrost.io/api/v2/...`
- GitHub: `https://api.github.com/orgs/bifrost-platform/...`

### 🔔 최우선 감시 신호
1. Vault/소각 주소 대형 이동, 네이티브 리치리스트 대형 변동
2. **BFC의 BitTrade(일본) 상장**
3. HashPort/N.suite JPYC 렌딩 **첫 TVL 수치**
4. **CCCP v2 메인넷 전환** (현재 testnet)
5. 검증자 집합 변동, 신규 GitHub 레포/릴리스, 워터마크(2026-06-02) 이후 신규 뉴스

---

## 미해결 / 후속 과제
- 네이티브 거래소(업비트/빗썸) 주소 **확정 귀속** — 공개 라벨 부재, **테스트 입금**만이 확정 경로 (후보는 03 차원8)
- 빗썸 BFC 준비금 수치 — 공시 페이지 JS 동적로딩, 백엔드 JSON 엔드포인트 탐색 필요
- BtcUSD 토큰 컨트랙트 주소 (네이티브 L1 발행이라 외부 인덱싱 제한)
- BTC vault 멀티시그 임계값(M-of-N)
