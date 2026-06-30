# Bifrost 검증자 24개 온체인 주소 스냅샷

> 스냅샷: 2026-06-29 (라운드 2524) · 출처: explorer.mainnet.bifrostnetwork.com/validators (RSC) + explorer-backend
> 형식: `controller / stash`. 루프에서 이 주소집합과 현재 검증자 집합을 diff → 신규/이탈 감지.
> ⚠️ 실명↔주소 매핑은 불가(Substrate, 온체인 identity 없음). 기명 검증자(BitTrade/AIF/KICA/DeSpread)도 주소 미공개.

## Basic 노드 (9)
| # | controller | stash |
|---|---|---|
| 1 | `0x11714Fb669055A7e46ecF3919eAC1c8E35555619` | `0x09C6334710fF9C622A24feCCC5a099c56F161015` |
| 2 | `0x0C7660B5BD6652450297C5ECE5A4D5d80D4b5067` | `0xf37c2853D84Fbfa5e8145FE4724B18c15E05bD36` |
| 3 | `0x60dfC03fbeF5d72de9af492d512Bfb60371F0903` | `0x4964A07a7249D1eA4d800b4a3fa9Af2C6E2d0937` |
| 4 | `0x4aCcce9Cc8597BDF25520407B29634e6692D013F` | `0x79dB2e2BB09856A35508F10A1AB8E54C682E4731` |
| 5 | `0x1048af71BEF72fB530c8a08a48ca53470F5B57f4` | `0xd19Ff3d1e34C09f6DFF33Dd033F064E85eE5cEe3` |
| 6 | `0x6Dac1b5F47d7f8685D7fc167676889fAe3d78c61` | `0x44A01F474D33584442110649a492e6551426534F` |
| 7 | `0xf86988800CBBc9130eE4B01AB039CBD1Aedf050c` | `0x8bbBfdB11764528070aF6c3b82971cFdEE6f615b` |
| 8 | `0x53D7ae30F7c9236BD58cABfb3721E0e6057f033a` | `0x6c7C332a090c8D2085857cf3220eA01C6d45a723` |
| 9 | `0xB680eD6c7AD3F53C63e368A929bd1a8A6468b816` | `0x36B264524a51DbFC2D56ae99621F13987474eb11` |

## Full 노드 (15) — 검증자+릴레이어
| # | controller | stash |
|---|---|---|
| 1 | `0x7CE6C4c6C5F1a6Ce274114dCf5343d5Cd1954dFb` | `0x56a942EC66B0b786c8D4c5Ed9B05D27E47F3dFC7` |
| 2 | `0x81bd2b2213cf3A3c7b1A436522026D24C6Dfc293` | `0x8f79b5ce86297fA4E45E6067b632c34eE48cD715` |
| 3 | `0xE4A4A88546F04f4bE726Acc84b859A146b668Db4` | `0x414343b7B4D88dAa7Fa532c1C15C684011d40080` |
| 4 | `0x03FCBa6842bc2e0538Cc5360328ff3cb72038d43` | `0xE5679a8BEfF465dC8243E652A402aBCf48233C78` |
| 5 | `0xC3Aa59c9De22079A45f85a79C9805D8c3Be71B43` | `0x4b4E6cbfa431be0358805b2E6D703299BEBdFb9a` |
| 6 | `0xAc41868A869d505B72C2a0FA9681Da323dd41E44` | `0xD5a2C25774258bc73BCaC61cA1BDE933e589d0FA` |
| 7 | `0x222561C7E3844F7143bF70C7E2f017410DCEd08d` | `0x4F53ce85C14c8334BD3CC4a5bb64Ad7D9780C7Ac` |
| 8 | `0x5623c7Ef271E414ec4F5A9Bf03C8321A1941422D` | `0x603a147D09235429D669e0021B54f3A9F9bdc57b` |
| 9 | `0x37e4C972B1C34706c711cB28D5533B3E52d4807a` | `0x7c45DcD37a7bfD17B32Dd4E96E65f00996ef4F82` |
| 10 | `0x416227815dd837698c165f5e8f19360ba874de27` | `0x3F7fF9B0a6026FD759E5e8d8ad39b519b959617e` |
| 11 | `0x6bEf93e6d6bC1e02B9D697b4FB8606152C200b29` | `0x11924ffE0FcCBEC5064D4886627Cc96aE70CB2aD` |
| 12 | `0x30f9C4515C8246F4119aA30402d1a80017D0eda6` | `0xE3e90e5b60293DDe85559f9d2983F6A97307B1E5` |
| 13 | `0x544b0c943358c29b643B795a09e80623C6844eDC` | `0x355b784757473741133911042bcD215B3d8EE289` |
| 14 | `0x400343AB85aC371A6615f25aeB9628e4cb950377` | `0xffFaAC4Ea0972C21c2834a0410A0582e4AbfF741` |
| 15 | `0x94dc0047c5ad7D57f3168C1F32Ba9a1b1D785B16` | `0x330d76197a25721357e05368179EbA8d0be9Be0e` |

> [추정] Full 13~15는 자기본딩 400만 BFC 정액·위임 0·낮은 productivity로 재단/팀 자체노드 가능성. 위임 붙은 노드는 외부 기관 가능성. (실명 연결 근거 없음)
> 참고: stash `0x355b78…`(Full13), `0x330d76…`(Full15), `0xffFaAC…`(Full14)는 차원1 ETH 리치리스트가 아닌 네이티브 리치리스트 상위에도 등장.

## ★ 검증자 식별(네이밍) 최대치 — funder+최초tx 휴리스틱 (2026-06-30)
> Substrate는 온체인 identity 없음 + stash는 staking pallet/genesis로 자금받아 EVM funder가 대부분 안 잡힘. 그래서 **"기명 검증자 ↔ 주소" 정확 매핑은 불가**. 아래는 자금출처·최초활동일·자기본딩 규모로 분류한 **정황 추정**(실명 확정 아님).

**공개 기명 검증자(주소 미공개·발표만):** BitTrade(日, 2024-11-29) · AI Fusion Capital(日 상장사, 2025-06-30) · KICA(한국정보인증) · DeSpread(컨설팅).

| 분류 | 노드(stash) | 근거 |
|---|---|---|
| **재단/팀 플래그십(거대 자기본딩)** | F13 `0x355b78`(6.67M)·F14 `0xffFaAC`(6.85M)·F15 `0x330d76`(6.78M) | 6.6~6.8M 자기본딩·EVM funder 없음 |
| **재단/제네시스 초기집합** | B1~B6·B9·F2·F3 `0x414343`(2023-02)·F4(2023-03)·F5·F6·F9·F11(2023-02) | 메인넷 초기, EVM funder 없음(pallet/genesis) |
| **운용/BTCFi Boost망 gas-funded 릴레이어** | B7(←0x4d0bbd3b)·B8 `0x6c7C33`(←0x52c78774,2025-03)·F8(←0x52c78774,2025-04)·F10(←0x52c78774,2025-03)·F12(←0x52c78774,2025-04) | 클러스터/Boost 운용망(0x52c78774 등)이 free잔액 충전 → 팀/운용 릴레이어군 |
| **BitTrade 후보(시점일치)** | F1 `0x56a942`(최초tx **2024-11-22**) | BitTrade 발표(2024-11-29) 직전 활성화 — 정황상 후보(미확정) |
| **신규 검증자(2026)** | F7 `0x4F53ce`(최초tx **2026-04-13**) | 최근 합류 — 신규 기관/노드 가능성, 감시대상 |

> ⚠️ 0x52c78774 등 "Boost 운용망"이 다수 Full(릴레이어) 노드의 free잔액을 충전 = **릴레이어 인프라의 상당부분이 팀/운용망 운영** 정황. 단 gas충전≠소유이므로 단정 아님.
> 감시: F7(2026-04 신규)처럼 **신규 stash 등장 + 기명 발표(KICA/DeSpread/AIF) 시점 교차**로 추후 매핑 정밀화 가능.

## ★ BfcStaking precompile (EVM 조회 가능 — 2026-06-30 발견)
> 이전 "Substrate 팔레트라 위임자 분포 불가"는 정정. precompile `0x0000000000000000000000000000000000000400`이 eth_call 가능.
- `candidate_count()` → 24 · `latest_round()`/`round_info()` → 2525 · `candidate_pool()` → (address[] 컨트롤러, uint256[] 총스테이크)
- **실측: 총 풀스테이크 405,645,895 BFC / 24노드**. 분포 균등(최대 6.1%), 상위5 30.4%·상위10 59.8%. 티어: 상위~12 ≈24M(Full급)·하위~12 ≈9.6M(Basic급).
- 루프 활용: 매번 candidate_pool 디프 → 검증자 집합 변동·스테이크 이동·신규 검증자(예: F7 2026-04 합류) 자동 추적. 추가 메서드: `candidate_state(address)`(self-bond·위임 분리), `selected_candidates()`.
