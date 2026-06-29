# Bifrost (BNC) 온체인 분석 리포트

> 대상: **Bifrost — Staking Yield Layer** (폴카닷/쿠사마 파라체인, 토큰 BNC)
> 작성일: 2026-06-29
> 작성: 온체인 데이터 수집 세션 (`claude/bifrost-onchain-analysis`)

---

## 0. 방법론 & 데이터 한계 (먼저 읽어주세요)

이 분석은 **온체인 데이터를 직접 RPC/API로 질의하지 못하는 환경**에서 수행되었습니다.

- 본 세션의 네트워크 정책상 DefiLlama API, Subscan API, 체인 RPC 등에 대한 **직접 호출이 이그레스 정책으로 차단(403)** 되었습니다.
- 따라서 수치는 **공개 집계 사이트(Subscan 대시보드, DefiLlama, CoinGecko/CMC) 및 Bifrost 공식 리포트**를 웹 검색으로 교차 확인하여 취합했습니다.
- 출처마다 **집계 방식·스냅샷 시점이 달라 TVL 수치가 상이**합니다(§4 참고). 이 리포트는 그 차이를 숨기지 않고 그대로 병기합니다.
- 정밀한 실시간 온체인 지표(블록 단위 홀더 분포, 일별 mint/redeem 플로우, 가스 사용량 등)가 필요하면, **Subscan API 키 또는 체인 RPC 접근이 허용된 환경에서 재실행**해야 합니다.

데이터 신뢰도 등급: **공식 리포트/Subscan 대시보드 = 中~高**, **3rd-party 가격 사이트 = 中**.

---

## 1. 요약 (Executive Summary)

- **포지셔닝**: Bifrost는 폴카닷 생태계 최대 리퀴드 스테이킹(LST) 프로토콜로, vDOT·vKSM 등 vToken을 통해 폴카닷 LST 시장의 **60%+** (일부 파라체인에서는 사실상 100%)를 점유.
- **제품 진화**: 단일 체인 LST → **SLPx 옴니체인 스테이킹**(vETH 3.0: Ethereum/Base/Arbitrum/Optimism에서 브리지 없이 스테이킹) → SLPx 2.0 + HyperBridge로 멀티 L1/L2 확장.
- **펀더멘털 vs 토큰 가격의 괴리**: 2025년 프로토콜 매출 **$8.07M**, 총 거래 **63만+**, 활성 주소 **약 3.9만**으로 실사용은 견조하나, **BNC 시가총액은 2026년 6월 기준 약 $0.8M까지 하락** — 토큰 가치 포착(value capture)이 사용량을 따라가지 못하는 전형적 괴리.
- **2026년 수축 신호**: 일부 온체인 스냅샷에서 vDOT 발행량이 2025년 피크(~18–24M) 대비 크게 줄어든 수치(~4.9M)가 관측됨. TVL도 2025년 7월 피크 $98M에서 2026년 들어 $28–44M대로 하락. **(주의: 스냅샷 일관성에 대한 검증 필요 — §4·§10)**

---

## 2. 프로토콜 개요

| 항목 | 내용 |
|---|---|
| 정체성 | Substrate 기반 크로스체인 리퀴드 스테이킹/파생 프로토콜 ("Staking Yield Layer") |
| 베이스 체인 | Bifrost 파라체인 (폴카닷 / 쿠사마) |
| 핵심 상품 | vToken(LST), SLPx(옴니체인 스테이킹), 수익공유 프로그램(RSP) |
| 발행 vToken (9종) | vDOT, vKSM, vETH, vMANTA, vGLMR, vMOVR, vASTR, vFIL, vBNC |
| 토큰 | BNC (거버넌스/스테이킹), veBNC (OpenGov 투표) |

**vToken 메커니즘**: 사용자가 자산을 예치하면 수익 누적형(yield-bearing) vToken을 1:N으로 수취. vToken은 폴카닷 XCM을 통해 파라체인 간 이동 가능한 크로스체인 담보로 활용됨(예: Moonbeam·Astar·Hydration DeFi에서 담보·LP).

---

## 3. 토큰 이코노믹스 — BNC

| 지표 | 값 | 출처 시점 |
|---|---|---|
| 최대 공급 | **80,000,000 BNC** (무인플레이션) | Docs |
| 유통 공급 | **~38.04M BNC** (출처별 37.4M~44.6M) | 2026-06 |
| 가격 | **~$0.0217** | 2026-06 |
| 시가총액 | **~$0.82M** | 2026-06 |
| FDV | **~$1.67M** | 2026-06 |
| 24h 거래량 | ~$0.61M | 2026-06 |
| 시총 순위 | ~3,051위 | 2026-06 |

**배분 구조(주요)**: 팀 16,000,000 BNC(TGE +180일 후부터 2년 선형 언락), 그 외 크라우드론·트레저리·생태계.

**가치 포착**: BNC/veBNC는 OpenGov 거버넌스 + 수수료/수익 분배에 연결. 다만 위 시총·FDV가 보여주듯 **프로토콜 매출($8.07M/2025) 대비 토큰 시가총액(~$0.8M)이 극단적으로 낮음** → 시장이 BNC의 캐시플로우 귀속을 거의 반영하지 않거나, 토큰의 매출 청구권이 약하다는 신호. (P/S 관점에서 비정상적으로 낮은 멀티플.)

---

## 4. TVL & 자금 흐름 — ⚠️ 출처별 수치 상이

| 출처 / 시점 | TVL | 비고 |
|---|---|---|
| Subscan 대시보드 (최근) | **$128.78M** | 프로토콜 전체 집계, 89,168 주소, 누적 매출 $3.89M |
| 2025 연간 (7월 피크) | **$98.33M** | 공식 연간 리포트 |
| 2025-09 | $86.24M | vDOT TVL 기준 |
| DefiLlama (2026-01) | **$44.08M** | LST 카테고리 한정 집계 |
| DefiLlama (2026-04) | **$28.34M** | 주간 -10%, LST 카테고리 한정 |

**왜 차이가 나나**: ① DefiLlama "liquid-staking"은 특정 자산군만 카운트하고 크로스체인 중복을 제거 → 가장 보수적. ② Subscan 대시보드는 프로토콜 전체(vBNC 등 포함)를 합산 → 가장 큼. ③ 가격 변동(BNC·DOT 하락)이 USD TVL을 크게 흔듦.

**해석**: 어떤 기준을 쓰든 **2025년 중반 피크($86–98M) → 2026년 상반기 수축($28–44M, LST 기준)** 추세는 일관됨. USD 기준 하락의 상당 부분은 토큰 가격 하락 + 일부 순유출(redeem)로 추정.

---

## 5. vToken별 온체인 지표

| vToken | 발행량 / TVS | TVL | 홀더 | APY | 비고 |
|---|---|---|---|---|---|
| **vDOT** | 4,940,953 vDOT* | ~$74.4M | 4,455 | **15.34%** (base 15.17 + reward 0.17) | 폴카닷 LST 60%+ 점유. 홀더 분포: Bifrost 2,551 / Moonbeam 389 / Astar 223 |
| **vKSM** | ~350K (피크 ~500K) | — | — | ~10%대 | 쿠사마 LST 60%+ 점유 |
| **vBNC** | TVS 20.67M | ~$1.21M | — | — | 2026-01 기준 MoM **+37%** |
| **vASTR** | ~100M (연중 50M→100M, 2x) | — | — | — | Astar |
| vETH / vMANTA / vGLMR / vMOVR / vFIL | — | — | — | vETH ~8% | vETH 3.0로 멀티체인 확장 |

\* **주의**: 이 vDOT 발행량(~4.94M)은 2025년 연간 리포트의 발행량(연초 ~7M → 연말 ~18M, 피크 24M)과 큰 괴리가 있음. (a) 2026년 대규모 redeem에 따른 실제 수축이거나, (b) 스냅샷/지표 정의 차이일 수 있음 → **재검증 필요**(§10).

**크로스체인 사용 사례**: Hydration 트레저리가 868,784 vDOT(=1,280,204 DOT 스테이킹) 발행 — vToken이 타 파라체인 트레저리의 수익자산으로 채택되는 대표 사례.

---

## 6. 사용자 · 활동 지표 (2025 연간 기준)

| 지표 | 값 |
|---|---|
| 총 거래 수 | **634,000+** |
| 활성 주소 | **~39,000** |
| 누적 주소 (Subscan) | **89,168** |
| dApp 누적 페이지뷰 | 1.16M+ |
| dApp 순 방문자 | ~39,000 |

활성 주소 대비 누적 주소 비율을 보면 **재방문/락인된 코어 유저층**이 존재하나, 절대 규모(활성 ~3.9만)는 중소형 프로토콜 수준.

---

## 7. 수익률 & 경쟁 비교

| 프로토콜 | 생태계 | 대표 수익률 | TVL(규모) | 특징 |
|---|---|---|---|---|
| **Bifrost** | Polkadot/멀티체인 | vDOT **~15.3%**, vETH ~8% | $28–128M (기준별) | 고수익 + 옴니체인(SLPx), 폴카닷 사실상 독점 |
| Lido | Ethereum 등 | stETH ~2.4% net (수수료 10%) | **~$38B** | 시장 지배자, 최대 유동성/DeFi 통합 |

**핵심 차별점**: Bifrost는 Lido와 직접 경쟁이 아니라 **폴카닷·고수익 니치 + 크로스체인 스테이킹 인프라(SLPx)**로 포지셔닝. vDOT를 멀티체인 Uniswap 풀(BSC/ETH/Base/Arbitrum)에 공급하면 스테이킹+LP 결합으로 25%+ APY도 가능(단, IL·스마트컨트랙트 리스크 수반).

---

## 8. 2026년 제품 · 동향

- **SLPx (옴니체인 스테이킹)**: 원격 호출로 멀티체인 스테이킹 수익에 접근하는 개발자 툴킷. DeFi·스테이블코인·RWA 타깃.
- **vETH 3.0**: Ethereum/Base/Arbitrum/Optimism/Polkadot에서 **브리지 없이** 리퀴드 스테이킹.
- **SLPx 2.0 + HyperBridge**: mint/redeem UX·크로스체인 효율 개선, 더 많은 L1/L2로 확장.
- **스테이블코인/RWA 수익 솔루션**: 2026 로드맵의 핵심 축 (vUSD 등 스테이킹 기반 스테이블코인 실험 — 외부 기고 다수).
- **에이전트 경제 연동**: Bifrost가 Claude/ChatGPT 등과 연동되는 "SLPx Skill"(키는 로컬 보관, 자율 스테이킹/언스테이킹, APY·TVL 질의)을 발표 — 본 분석 환경과도 연계 가능성.

---

## 9. 강점 / 약점

**강점**
- 폴카닷·쿠사마 LST 사실상 독점(60–100% 점유), XCM 기반 크로스체인 담보 네트워크.
- 무인플레이션 토큰(80M 고정), 2025년 흑자 전환($8.07M 매출, $1.2M 총이익).
- SLPx로 멀티체인 인프라 레이어로 진화 → 폴카닷 의존도 분산 시도.

**약점 / 리스크**
- **토큰 가치 포착 실패 신호**: 매출 대비 시총 극단적 저평가($0.8M mcap). 토큰 보유 인센티브 의문.
- **USD TVL 수축**: 2025 피크 대비 LST TVL 큰 폭 하락 + (검증 필요한) vDOT 발행 수축.
- **폴카닷 생태계 리스크**: DOT 가격·OpenGov·파라체인 활동에 매출이 강하게 연동.
- **유동성/시장 리스크**: BNC 일 거래량 $0.6M대, 시총 순위 ~3,000위 → 유동성·변동성 취약.

---

## 10. 후속 검증 권장 항목 (데이터 접근 허용 시)

1. **vDOT 발행량 시계열 재확인**: Subscan API로 2025-피크 → 2026-현재 mint/redeem 일별 플로우 직접 추출 (§5의 4.94M vs 18–24M 괴리 해소).
2. **순유출 vs 가격효과 분해**: USD TVL 하락 중 토큰가격 하락분과 실제 redeem 물량분 분리.
3. **홀더 집중도**: vDOT/BNC 상위 홀더 분포(고래·트레저리·CEX) 온체인 추출.
4. **매출-토큰 연결 검증**: 프로토콜 수수료가 실제 BNC 바이백/veBNC 보상으로 흐르는 비중 확인.
5. **크로스체인 분포**: Moonbeam/Astar/Hydration 등 파라체인별 vToken 잔액 정밀 집계.

---

## 11. 출처

- [Bifrost Liquid Staking — DefiLlama](https://defillama.com/protocol/bifrost-liquid-staking)
- [Subscan — Bifrost Account Dashboard](https://bifrost.subscan.io/account)
- [BNC — Bifrost Docs (Tokenomics 2.0)](https://docs.bifrost.io/tokenomics-2.0/bnc-bifrost-native-coin)
- [Bifrost 2025 Annual Report](https://bifrost.io/blog/bifrost-2025-annual-report)
- [Bifrost Monthly Report — January 2026](https://bifrost.io/blog/bifrost-monthly-report-january-2026)
- [SLPx — Omnichain Liquid Staking](https://bifrost.io/slpx)
- [SLPx 2.0 — Liquidity Infrastructure for Crypto Staking](https://bifrost.io/blog/slpx-the-liquidity-infrastructure-for-crypto-staking)
- [Bifrost (BNC) — CoinGecko](https://www.coingecko.com/en/coins/bifrost-native-coin)
- [Bifrost (BNC) — CoinMarketCap](https://coinmarketcap.com/currencies/bifrost-bnc/)
- [vDOT — Bifrost Docs](https://docs.bifrost.io/faq/what-are-vtokens/vdot)
- [How Bifrost Grew to Be The Largest Liquid Staking Platform on Polkadot](https://bifrost.io/blog/how-bifrost-grow-to-be-the-largest-liquid-staking-platform-on-polkadot)

---

*면책: 본 리포트는 정보 제공 목적이며 투자 권유가 아닙니다. 수치는 직접 온체인 질의가 차단된 환경에서 공개 집계 자료를 교차 확인해 취합한 것으로, 시점·집계 방식에 따라 오차가 있을 수 있습니다.*
