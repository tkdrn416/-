#!/usr/bin/env python3
"""Bifrost(BFC) 모니터 — 와치리스트 경보 + 시계열 누적(history.csv) + 그래프 리포트.
사용:
  python3 monitor.py            # 점검 + 경보요약 + history.csv 1행 + 리포트 갱신
  python3 monitor.py --no-save  # 누적/갱신 없이 조회만
출력: 콘솔 🔔경보요약 / data/history.csv(엑셀) / data/monitor-baseline.json / data/monitor-events.log / bifrost-daily-report.html
"""
import json,urllib.request,time,os,sys,csv,datetime
API="https://explorer-backend.mainnet.thebifrost.io"
RPC="https://public-01.mainnet.bifrostnetwork.com/rpc"
HERE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(HERE,"..","data")
BASE=os.path.join(DATA,"monitor-baseline.json"); HIST=os.path.join(DATA,"history.csv"); LOG=os.path.join(DATA,"monitor-events.log")
ALERTS=[]; FETCH={"ok":0,"fail":0}
def alert(p,m): ALERTS.append((p,m))
CIRC=1_390_000_000  # 큐레이션 유통량(스테이킹비율 분모)
BTCUSD_VAULT="0xd85eb87cab9041ad00764b95796702b1104f42d7"  # BtcUSD 최대홀더(브릿지볼트)

WATCH=[
 ("업비트 콜드","0x50f187ef4447da6e5ff1d740439e91175bac955e","거래소"),
 ("업비트 핫","0x081a4ee55739f0da8abb8af40d07687527a268c3","거래소"),
 ("빗썸 콜드","0xdcd52f5f5af5022edefd59fd5353f4da3f2c8935","거래소"),
 ("빗썸 핫","0x39528d59132920ab0a637129d90cf9fb3650084d","거래소"),
 ("재단 Treasury","0x6d6f646c70792f74727372790000000000000000","재단핵심"),
 ("재단 BTCFi배포자 A30B97a5","0xa30b97a5485388d776c24c50dc82516726bb7a9b","재단"),
 ("재단 제네시스배포자 Dd505f3","0xdd505f3edb9b574d139e2f9d8b89deb6495de369","재단"),
 ("분배자 0x313b1578(클러스터연결)","0x313b157854f61bc4b3f37c45a6a6c69a0e2b3ae3","재단/클러스터연결"),
 ("순환클러스터 0x0c791e90","0x0c791e902d08b916218317d308156eb6a8a2d6d2","순환클러스터"),
 ("순환클러스터 0xeb76c926(UNDERWATER)","0xeb76c926e848e0bab9323e998eea16c9076563a5","순환클러스터"),
 ("운용자 가스허브 0x81c22bec","0x81c22bec01c83e5bff125d3a52634dbef60d93d4","운용자네트워크"),
 ("볼트운용 EOA 0xaff29bed","0xaff29bedb24cc4979477f271f8a426590855cfca","운용자네트워크"),
 ("클러스터컨트롤러 0xb878526f","0xb878526f6d1174be9e75d1f617ae9271e4f42285","운용자네트워크"),
 ("Boost볼트 0xbc0995ca","0xbc0995cae2218203262ed1b8557b7886d579e985","BiFi볼트"),
 ("BiFi BFC풀(#3리저브) 0x4bAE7","0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee","BiFi풀"),
 ("일본 JPYC venue 0x6894Ae31","0x6894ae31cae97f228590f6dc7bbea7449f4db980","일본"),
 ("HTX 운영지갑 0x09FCED81(MM활발)","0x09fced818439182812f13b006114da4382c4470e","거래소"),
]
EXCH_ADDRS=[a for _,a,c in WATCH if c=="거래소"]
# 물밑 프로젝트 조기신호 = 운용/배포 EOA가 '새 컨트랙트'를 배포하는 순간(기존 껍데기11개 재사용 가정에 의존하지 않음)
OPERATOR_EOAS=[
 ("가스허브 0x81c22bec","0x81c22bec01c83e5bff125d3a52634dbef60d93d4"),
 ("볼트운용 0xaff29bed","0xaff29bedb24cc4979477f271f8a426590855cfca"),
 ("클러스터컨트롤 0xb878526f","0xb878526f6d1174be9e75d1f617ae9271e4f42285"),
 ("BTCFi배포자 0xa30b97a5","0xa30b97a5485388d776c24c50dc82516726bb7a9b"),
 ("제네시스배포자 0xdd505f3","0xdd505f3edb9b574d139e2f9d8b89deb6495de369"),
]
TOKEN_WATCH=[
 ("Unified JPYC 총공급","0x84122a4a75bfe65ef455dba5f6d43d61359ca77e",500_000,"jpyc_supply"),
 ("BtcUSD 총공급","0x6906ccda405926fc3f04240187dd4fad5df6d555",500_000,"btcusd_supply"),
 ("Unified cbBTC(테스트)","0x74b73fd2ee237e9219df30dffdb206d237cbfc00",1,"cbbtc_supply"),
 ("BrBTC 네이티브BTC브릿지(테스트)","0xcb4e4f67b33eebfc17c82cf6e8c0b56d269aeb79",1,"brbtc_supply"),
 ("stBFC 유동스테이킹총량","0xeff8378c6419b50c9d87f749f6852d96d4cc5ae4",13_000_000,"stbfc_supply"),
 ("wstBFC 래핑총량","0x386f2f5d9a97659c86f3ca9b8b11fc3f76efddae",13_000_000,"wstbfc_supply"),
]
CAT_THRESH={"거래소":5_000_000,"재단핵심":1,"운용자네트워크":1_000_000}; DEFAULT_THRESH=2_000_000
STAGED_SHELLS=["0xF4394659BB0303fa7bc69295F6115771198F718D","0x94B9A18CfB4b7D21a86b909871fd3d7898fb2bba",
 "0xB9b05cEeABd239A86CdA0bD5cd4aBa3eBB0F5f4C","0x6dedf09e8Fd216B823f63959d8daC25FBBfb6E25",
 "0x3f0BA9107758FACBad8948E138a71e18778Cb9DF","0xd7768f3477531FF5990735287E8fDd5a6a43B2bd",
 "0xD06B9B6A4A4F2FF72Fc2C7F9101E54f85F8a4e68","0xF2C269184F002677CC40099171470BB5f80e2719",
 "0x11d91B18bCE6bB6fF63F23Ee7b2B7660697daCFd","0xb0dd98593B4e353D682Be495C80D4928fA512B3b",
 "0x4a6dDEeC476073173CAB6f7Ff023f89CdB198931"]
NEW_TOKEN_QUERIES=["JPYSC","JPYC","cbBTC","BrBTC","Bridged"]
BIFI_BFC_POOL="0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee"
WSTBFC_TOKEN="0x386f2f5d9a97659c86f3ca9b8b11fc3f76efddae"; WSTBFC_HANDLER="0xf9b2f6d2a61923e61ad9f6daa78f52b7e1722b12"
BTCUSD_TOKEN="0x6906ccda405926fc3f04240187dd4fad5df6d555"; BTCUSD_HANDLER="0xcf2fc1d354018a39d5ef036aa865ad8cbf7b611e"
# BiFi 달러코인 대출 핸들러(getBorrowTotalAmount, 전부 1e18 정규화)
DOLLAR_HANDLERS=[("btcusd","0xcf2fc1d354018a39d5ef036aa865ad8cbf7b611e"),("usdc","0x168b2d7dd6b9812392f99ba01a14db03ed06dedc"),
 ("usdt","0xed7b0974dc5d98b9e7c83695c415d68b8781b0f8"),("dai","0x2168dab12a6a93181bbad9c9dc769307c36fb45c")]
BORROW_SEL="0x3763d0db"  # getBorrowTotalAmount()
BIFI_CG="https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0x2791BfD60D232150Bff86b39B7146c0eaAA2BA81&vs_currencies=usd,krw&include_market_cap=true"
STAKING_PRECOMPILE="0x0000000000000000000000000000000000000400"; CANDIDATE_POOL_SEL="0x96b41b5b"
# BiFi 청산건전성 자동추적: 대형 차입자 워치리스트(TOP100 BiFi예치/볼트 38 + Boost볼트). Manager로 UNDERWATER 자동집계.
MGR_MANAGER="0x6541342bc39a399c274092652b5c50890dca6fca"
CRD_SEL="0x314d59fc"  # getUserTotalIntraCreditAsset(address)→(limit,currentBorrowUSD)
LIM_SEL="0x7d170e26"  # getUserLimitIntraAsset(address)→(borrowLimitUSD,liqThresholdUSD)
BORROWER_WATCH=["0xbc0995cae2218203262ed1b8557b7886d579e985","0x0c791e902d08b916218317d308156eb6a8a2d6d2","0xfd561fbd4dd43ea04733adfa31949b25c0595818","0xd7c19693f9ca21511847b1707242773d37c1c391","0xeb76c926e848e0bab9323e998eea16c9076563a5","0xd05aa73ec4adfda929c52ef03db6e27f21da7005","0xbbcc95860e9a60b12dca99c78f82dda32dec6337","0x412b9646515cdb87d58041d31aa7f1f016b6fc6e","0x91c4094bb5e97a1c8968add7499b16e3bc2c3a87","0x6abaa3950d0e0f0b731d8e453ec0b2ca0237bc26","0x0e9b3cfab21f9b31d797fae2b34928ce38496b88","0xbabdc92221b4de2d8413412b6aa9798dd54afcbf","0x10982101db09142dfdec7ad75712093c45c075b3","0x2a3e8fd86a304168b8e7d187b63c07feb5efef83","0x902a21c0fa4e223e07d51ac2608fc19b7c303582","0xc7275255ae6da1bc1e103d6b5d16d39f7f252204","0xb6bd9f069ef653999ced2c8c7b0b8ec45f553fb5","0xc54347d6d873875795a49465fda7a047fb1d1b8b","0x2b6745618ff2ee48be7b52347c2d67c4c9eb0973","0x080c1ee5df627c56a849a04c46af1f533ee290bc","0x106f60267cd1368641633f86dec41a028dbcb147","0xdd2398e8bd9f8a1f34cc013b7d0ca5f85a08470d","0xc1f2a6ea484ab0f0041a158dc86e132d1612cdf4","0x556f8c585d4efe5f379e56fe373bdf9827f2f7cd","0x4d0bbd3bbcebbf7d826b00a57683f2fff643d184","0x77d6941a54ac5fa21930b871ac0183dc01b2ddd3","0x9610386e89a16809f1c341dbcfdb92ce69daed4a","0xb290781ada49ebb068615090dd04dbe8a9439c9b","0xbb9f02945073a2edf7b8632557f20414d96a9d20","0xf614497937555ef5d6ee945c15658ad46ba114c2","0x35d8a3d697df071e3de2d5f681198910d4c3e84a","0x5e5cc1a3ad7202408f2a37b2b8d69f414c7235bd","0x8c5ce7cd747971736cf67c7b80033607581fc3b1","0xa4147540b0552fd5ec5e66490f4b9e38786ddc33","0x6666a49b7339998dfbc494f649710a1f3cd66666","0x0cb9964d54f66f576567c45e5cbba591e24bbb11","0xda50a0ff48eda9b67a8fb2ba8274eec1e6351843","0xd22dbc1f123a363cc68f1c4d383fc4575f9067d1"]
BFC_ERC20="0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c"

def get(u):
    for _ in range(3):
        try: r=json.load(urllib.request.urlopen(API+u,timeout=20)); FETCH["ok"]+=1; return r
        except: time.sleep(0.6)
    FETCH["fail"]+=1; return {}
def get_url(u,timeout=15):
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        r=json.load(urllib.request.urlopen(req,timeout=timeout)); FETCH["ok"]+=1; return r
    except: FETCH["fail"]+=1; return None
def rpc(to,data):
    try:
        req=urllib.request.Request(RPC,data=json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":to,"data":data},"latest"]}).encode(),headers={"Content-Type":"application/json"})
        r=json.load(urllib.request.urlopen(req,timeout=15)).get("result"); FETCH["ok"]+=1; return r
    except: FETCH["fail"]+=1; return None
def bal(a): return int(get(f"/api/v2/addresses/{a}").get('coin_balance') or 0)/1e18
def erc20_bal(token,holder):
    r=rpc(token,"0x70a08231"+holder.lower().replace("0x","").rjust(64,"0"))
    return int(r,16)/1e18 if r and r!="0x" else None  # None=조회실패(0과 구분)
def fmt(v): return f"{v:+,.0f}" if v else "0"
def rnd(v): return round(v) if v is not None else ""   # None은 빈칸(차트가 가짜 0 안 찍게)

def snapshot():
    snap={"_ts":int(time.time())}; st=get("/api/v2/stats")
    snap["_price"]=float(st.get('coin_price') or 0); snap["_mcap"]=float(st.get('market_cap') or 0)
    snap["_total_txns"]=int(st.get('total_transactions') or 0); snap["_total_addr"]=int(st.get('total_addresses') or 0)
    for lab,a,cat in WATCH: snap[a]=bal(a)
    return snap

def balances(cur,old,row):
    print(f"\n{'라벨':<32}{'카테고리':<18}{'잔액BFC':>16}{'Δ':>14}")
    up=bt=htx=0
    for lab,a,cat in WATCH:
        v=cur[a]; d=v-old.get(a,v) if old else 0
        if "업비트" in lab: up+=v
        if "빗썸" in lab: bt+=v
        if "HTX" in lab: htx+=v
        th=CAT_THRESH.get(cat,DEFAULT_THRESH); flag=""
        if old and abs(d)>=th:
            flag=" ⚠️"
            if cat=="재단핵심" and d<0: alert("P1",f"★재단핵심 출금! {lab} {fmt(d)} BFC (첫 집행/매도 신호)")
            elif cat=="거래소" and d>0: alert("P1",f"거래소 콜드 순유입 {lab} {fmt(d)} BFC (매도압력)")
            elif cat=="거래소": alert("P2",f"거래소 출금 {lab} {fmt(d)} BFC")
            else: alert("P2",f"{cat} 잔액변동 {lab} {fmt(d)} BFC")
        print(f"{lab:<32}{cat:<18}{v:>16,.0f}{fmt(d):>14}{flag}")
    row["upbit_bfc"]=round(up); row["bithumb_bfc"]=round(bt); row["htx_bfc"]=round(htx); row["exch_total"]=round(up+bt+htx)
    row["treasury_bfc"]=round(cur.get("0x6d6f646c70792f74727372790000000000000000",0))
    if old:
        prev_exch=sum(old.get(a,0) for a in EXCH_ADDRS)
        row["exch_net_flow"]=round((up+bt+htx)-prev_exch)
        print(f"  └ 거래소 순흐름(전 실행 대비): {fmt(row['exch_net_flow'])} BFC")

def token_check(old,row):
    print("\n# 토큰 공급 추세:"); snap={}
    for lab,addr,th,col in TOKEN_WATCH:
        t=get(f"/api/v2/tokens/{addr}")
        ts=t.get('total_supply')
        sup=int(ts)/10**int(t.get('decimals') or 18) if ts else None
        snap[addr]=sup if sup is not None else old.get("tok_"+addr); row[col]=rnd(sup)
        if col=="btcusd_supply": row["btcusd_holders"]=t.get('holders')
        d=(sup-old.get("tok_"+addr,sup)) if (old and sup is not None and old.get("tok_"+addr) is not None) else 0
        flag=" ⚠️" if old and abs(d)>=th else ""
        if flag: alert("P2",f"{lab} 공급 {fmt(d)} (현 {sup:,.0f})")
        print(f"  {lab:<22} {(f'{sup:,.0f}' if sup is not None else 'n/a'):>16}  (홀더 {t.get('holders')})  Δ{fmt(d)}{flag}")
    return snap

def bifi_check(row):
    print("\n# BiFi 예치물량(담보) 추세:")
    bfc=bal(BIFI_BFC_POOL); wst=erc20_bal(WSTBFC_TOKEN,WSTBFC_HANDLER); btc=erc20_bal(BTCUSD_TOKEN,BTCUSD_HANDLER)
    row["bifi_bfc_pool"]=rnd(bfc); row["bifi_wstbfc"]=rnd(wst); row["bifi_btcusd"]=rnd(btc)
    sw=f"{wst:,.0f}" if wst is not None else "n/a"; sb=f"{btc:,.0f}" if btc is not None else "n/a"
    print(f"  담보: BFC풀 {bfc:,.0f} · wstBFC {sw} · BtcUSD {sb}")
    # BiFi 대출량(getBorrowTotalAmount, 1e18) — 달러코인(BtcUSD·USDC·USDT·DAI) 개별 + 합계
    print("\n# BiFi 대출량(달러코인):")
    tot=0; anyok=False
    for nm,h in DOLLAR_HANDLERS:
        r=rpc(h,BORROW_SEL); v=int(r,16)/1e18 if r and r!="0x" else None
        row["bifi_borrow_"+nm]=rnd(v)
        if v is not None: tot+=v; anyok=True; print(f"  {nm.upper():<7} {v:,.0f}")
        else: print(f"  {nm.upper():<7} n/a")
    row["bifi_borrow_dollar"]=round(tot) if anyok else ""
    if anyok: print(f"  → 달러코인 대출 합계 {tot:,.0f}")

def validator_check(old,row):
    print("\n# 검증자 집합·스테이크:")
    r=rpc(STAKING_PRECOMPILE,CANDIDATE_POOL_SEL)
    if not r or len(r)<130: print("  (조회 실패 — 이번 행 검증자 칼럼 공백)"); return
    b=r[2:]
    try:
        o1=int(b[0:64],16)*2; o2=int(b[64:128],16)*2
        n=int(b[o1:o1+64],16); m=int(b[o2:o2+64],16)
        if n!=m: print(f"  ⚠️ 배열길이 불일치 n={n} m={m} — 디코딩 의심, 스킵"); return
        addrs=["0x"+b[o1+64+i*64+24:o1+64+(i+1)*64] for i in range(n)]
        stakes=[int(b[o2+64+i*64:o2+64+(i+1)*64],16)/1e18 for i in range(m)]
    except: print("  (디코딩 실패)"); return
    tot=sum(stakes); ss=sorted(stakes,reverse=True); cum=0; nak=0
    for i,s in enumerate(ss,1):
        cum+=s
        if cum>tot*0.333: nak=i; break
    row["val_count"]=n; row["val_total_stake"]=round(tot); row["nakamoto33"]=nak
    print(f"  검증자 {n} · 총스테이크 {tot:,.0f}(=self+위임) · Nakamoto(33%) {nak}")
    prev=set(filter(None,(old.get("val_addrs") or "").split(","))) if old else set(); curset=set(addrs)
    if prev:
        for x in curset-prev: alert("P1",f"★신규 검증자 등장 {x[:12]}")
        for x in prev-curset: alert("P1",f"★검증자 이탈 {x[:12]}")
    row["_val_addrs"]=",".join(sorted(curset))

def bifi_health_check(old,row):
    # 대형 차입자 워치리스트 전수 → UNDERWATER 자동집계(직접 확인 불필요)
    print("\n# BiFi 청산건전성 자동추적(대형 차입자 워치리스트):")
    def w(r,i): return int(r[2+i*64:2+(i+1)*64],16)/1e18 if r and len(r)>=2+(i+1)*64 and r!="0x" else None
    borrowers=0; uw=0; uwdebt=0; uwlist=[]
    for a in BORROWER_WATCH:
        c=rpc(MGR_MANAGER,CRD_SEL+a[2:].rjust(64,"0")); borrow=w(c,1)
        if borrow is None or borrow<=100: continue  # 100달러 미만 dust 제외
        borrowers+=1
        l=rpc(MGR_MANAGER,LIM_SEL+a[2:].rjust(64,"0")); liq=w(l,1)
        if liq is not None and borrow>liq: uw+=1; uwdebt+=borrow; uwlist.append((a[:12],borrow,liq))
    row["bifi_borrowers"]=borrowers; row["bifi_uw_count"]=uw; row["bifi_uw_debt"]=round(uwdebt)
    print(f"  차입자 {borrowers}명 · UNDERWATER {uw}명 · 부채합 ${uwdebt:,.0f}")
    for ad,b,li in sorted(uwlist,key=lambda t:-t[1])[:5]: print(f"    {ad} 차입 ${b:,.0f} > 임계 ${li:,.0f}")
    prev=_int(old.get("bifi_uw_count")) if old else None
    if prev is not None and uw>prev: alert("P2",f"BiFi UNDERWATER 증가 {prev}→{uw}명(부채 ${uwdebt:,.0f}) — 신규 청산권 발생")
    if uwdebt>2_000_000: alert("P1",f"★BiFi UNDERWATER 부채 급증 ${uwdebt:,.0f} — 청산리스크 확대")

def _int(v):
    try: return int(float(v))
    except: return None
def _flt(v):
    try: return float(v)
    except: return None

def deployer_scan(old,row):
    # 핵심 감시: 운용/배포 EOA의 신규 컨트랙트 배포 = 물밑 프로젝트의 가장 이른 신호
    # (껍데기11개 재사용 가정에 안 갇힘 — 완전 새 주소 배포도 포착)
    print("\n# 운용자/배포자 EOA 신규 컨트랙트 배포 스캔(물밑 조기신호):")
    known=set(filter(None,(old.get("seen_contracts") or "").split("|"))); cur=set(known); newc=0
    for lab,a in OPERATOR_EOAS:
        items=(get(f"/api/v2/addresses/{a}/transactions") or {}).get('items') or []
        for it in items[:30]:
            cc=it.get('created_contract') or {}
            h=(cc.get('hash') or '').lower()
            if not h: continue
            cur.add(h)
            if known and h not in known:
                newc+=1; print(f"  🚨 신규 컨트랙트 {lab} → {h[:16]}")
                alert("P1",f"★운용자 신규 컨트랙트 배포! {lab}→{h[:14]} — 물밑 프로젝트/신제품 가능")
    if newc==0: print(f"  신규 배포 없음(추적중 컨트랙트 {len(cur)}개).")
    row["new_contracts"]=newc
    return "|".join(sorted(cur))

def slow_drift_check(row):
    # 누적드리프트: 단발Δ가 임계 아래로 '쪼개진' 완만한 유출/유입을 history.csv 기준선(~7행 전)으로 포착
    if not os.path.exists(HIST): return
    try: hist=list(csv.DictReader(open(HIST)))
    except: return
    if len(hist)<3: print("\n# 누적드리프트: 데이터 부족(3행+부터)"); return
    base=hist[-7] if len(hist)>=7 else hist[0]; span=min(len(hist),7)
    print(f"\n# 누적드리프트 점검(최근 {span}행 대비):")
    def dv(k): a=_flt(row.get(k)); b=_flt(base.get(k)); return (a-b) if (a is not None and b is not None) else None
    checks=[("exch_total","거래소 보유",10_000_000,False),("btcusd_supply","BtcUSD 발행",1_000_000,None),
            ("bifi_borrow_dollar","BiFi 달러대출",1_000_000,None),("treasury_bfc","Treasury",1,False)]
    any_hit=False
    for k,lab,thr,updown in checks:
        d=dv(k)
        if d is None or abs(d)<thr: continue
        any_hit=True; print(f"  ⚠️ {lab} {span}행 누적 {fmt(d)}")
        if k=="treasury_bfc" and d<0: alert("P1",f"★Treasury 누적 유출 {fmt(d)}(최근 {span}행) — 단발 임계 아래로 분할 집행 정황")
        elif k=="exch_total" and d>0: alert("P2",f"거래소 누적 순유입 {fmt(d)}(최근 {span}행) — 완만한 매도압 축적")
        else: alert("P2",f"{lab} 누적 변동 {fmt(d)}(최근 {span}행)")
    if not any_hit: print("  완만한 누적드리프트 없음.")

def shell_check(old,row):
    # 자금유입/토큰전송/tx 증가 = 신제품 런칭. tx는 기준선 대비 '증가'로 판정(셋업7tx 프록시 오탐 방지)
    print("\n# 스테이징 껍데기 11개 (자금·전송·tx 변화=신제품 런칭):"); act=0; state={}
    for a in STAGED_SHELLS:
        c=get(f"/api/v2/addresses/{a}/counters"); tt=int(c.get('token_transfers_count') or 0)
        tx=int(c.get('transactions_count') or 0); bl=bal(a); k=a.lower()
        state["sh_"+k]=f"{tt},{tx}"; ptt,ptx=0,0
        pv=(old.get("sh_"+k) or "").split(",")
        if len(pv)==2: ptt,ptx=_int(pv[0]) or 0,_int(pv[1]) or 0
        # 활성 신호: 잔액>0 / 토큰전송 발생 / 기준선 대비 tx 증가(신규 상호작용)
        if bl>0 or tt>0 or (old and tx>ptx):
            act+=1; print(f"  ⚠️ 활성화! {a[:12]} xfers={tt} tx={tx}(전 {ptx}) bal={bl:,.0f}")
            alert("P1",f"★신제품 런칭! 껍데기 {a[:12]} 활성화(xfers={tt},tx {ptx}→{tx},bal={bl:,.0f})")
    if act==0: print("  전부 빈 상태(런칭 신호 없음).")
    row["shells_active"]=act; return state

def new_token_scan(old):
    print("\n# 신규 토큰 출현 스캔(JPYSC·신규 브릿지):")
    known=set(filter(None,(old.get("known_tokens") or "").split("|"))); cur=set(); n=0; jpysc=0
    for q in NEW_TOKEN_QUERIES:
        for it in (get(f"/api/v2/tokens?q={q}").get('items') or [])[:12]:
            addr=(it.get('address') or '').lower(); sym=it.get('symbol') or ''
            if not addr: continue
            cur.add(addr)
            if 'JPYSC' in (sym+(it.get('name') or '')).upper(): n+=1; jpysc=1; print(f"  🚨 JPYSC! {sym} {addr[:14]}"); alert("P1",f"🚨 JPYSC 계열 토큰 등장! {sym} {addr[:14]}")
            elif known and addr not in known: n+=1; print(f"  ⚠️ 신규 {sym} {addr[:14]}"); alert("P2",f"신규 토큰 {sym} {addr[:14]}")
    if n==0: print("  신규 없음(JPYSC 미등장).")
    return "|".join(sorted(cur)), jpysc

def exchange_check(cur,old):
    print("\n# 거래소 시세·입출금:")
    bt=(get_url("https://api.bithumb.com/public/ticker/BFC_KRW") or {}).get('data') or {}
    krw=None
    if bt: krw=float(bt.get('closing_price') or 0); print(f"  빗썸 {krw}원 · 24h대금 {float(bt.get('acc_trade_value_24H') or 0)/1e8:,.1f}억")
    ast=(get_url("https://api.bithumb.com/public/assetsstatus/BFC_KRW") or {}).get('data') or {}
    if ast:
        dep,wd=ast.get('deposit_status'),ast.get('withdrawal_status'); print(f"  빗썸 입금={dep} 출금={wd}")
        if dep==0 or wd==0: alert("P1",f"★빗썸 입출금 중단! 입금={dep} 출금={wd}")
    if old.get("_price") and cur["_price"]:
        ch=(cur["_price"]-old["_price"])/old["_price"]*100
        if abs(ch)>=10: alert("P1",f"★가격 급변 {ch:+.1f}% (${old['_price']:.5f}→${cur['_price']:.5f})")
    return krw

def bifi_price(row):
    # BIFI = 파이랩의 BiFi 거버넌스토큰(곡괭이토큰). 컨트랙트로 조회(Beefy BIFI 혼동 회피)
    d=get_url(BIFI_CG) or {}
    v=d.get("0x2791bfd60d232150bff86b39b7146c0eaaa2ba81") or {}
    if v.get("usd"):
        row["bifi_price_usd"]=v.get("usd"); row["bifi_price_krw"]=v.get("krw"); row["bifi_mcap_usd"]=round(v.get("usd_market_cap") or 0)
        print(f"\n# BIFI 토큰(곡괭이) 가격: ${v.get('usd')} / {v.get('krw')}원 · 시총 ${row['bifi_mcap_usd']:,.0f}")
    else: print("\n# BIFI 가격: 조회 실패(칼럼 공백)")

def defi_tvl(row):
    chains=get_url("https://api.llama.fi/v2/chains") or []
    for c in (chains if isinstance(chains,list) else []):
        nm=c.get('name','').lower()
        if 'bifrost' in nm and 'network' in nm:  # BNC('Bifrost') 오염 방지 위해 'network' 필수
            row["defi_tvl_usd"]=round(c.get('tvl') or 0); print(f"\n# DefiLlama 체인 TVL: ${row['defi_tvl_usd']:,.0f}"); return
    print("\n# DefiLlama: Bifrost Network 체인 미발견(칼럼 공백)")

def github_check(old):
    for repo in ["bifrost-node","bifrost-relayer.rs"]:
        rel=get_url(f"https://api.github.com/repos/bifrost-platform/{repo}/releases/latest")
        tag=(rel or {}).get('tag_name')
        if tag:
            key=f"gh_{repo}"
            if old.get(key) and old[key]!=tag: alert("P2",f"★GitHub 신규 릴리스 {repo} {old[key]}→{tag}")
            github_check.tags[key]=tag
github_check.tags={}

def burn_check(old):
    info=get_url("https://api.ethplorer.io/getAddressInfo/0x000000000000000000000000000000000000dEaD?apiKey=freekey",20)
    if not info: return None
    for tk in (info.get('tokens') or []):
        if (tk.get('tokenInfo') or {}).get('address','').lower()==BFC_ERC20.lower():
            v=float(tk.get('rawBalance',0))/1e18
            if old.get("burn_dead") and v>old["burn_dead"]+1: alert("P1",f"★소각 재개! dead +{v-old['burn_dead']:,.0f} BFC")
            return v
    return None

def summary():
    print("\n"+"═"*56)
    p1=[m for p,m in ALERTS if p=="P1"]; p2=[m for p,m in ALERTS if p=="P2"]
    fail=FETCH["fail"]
    if not ALERTS:
        if fail==0: print("🔔 오늘의 경보 요약:  ✅ 이상 무 — 전부 평소 범위(조회 100% 성공=확인됨)")
        else: print(f"🔔 오늘의 경보 요약:  ⚠️ 경보 0건이나 조회실패 {fail}건 — '이상 무' 아님, '일부 미확인'. 실패지표는 재실행 확인 필요")
    else:
        note=f" · ⚠️조회실패 {fail}건(미확인 존재)" if fail else ""
        print(f"🔔 오늘의 경보 요약:  ⚠️ 사건 {len(ALERTS)}건 (P1 {len(p1)}·P2 {len(p2)}){note}")
        for m in p1: print(f"  🔴 P1  {m}")
        for m in p2: print(f"  🟡 P2  {m}")
    print("═"*56)
    return len(p1),len(p2)

CSV_COLS=["date","price_usd","price_krw","bfc_mcap_usd","bifi_price_usd","bifi_price_krw","bifi_mcap_usd","upbit_bfc","bithumb_bfc","htx_bfc","exch_total","exch_net_flow","treasury_bfc",
 "jpyc_supply","btcusd_supply","btcusd_holders","stbfc_supply","wstbfc_supply","cbbtc_supply","brbtc_supply",
 "bifi_bfc_pool","bifi_wstbfc","bifi_btcusd","bifi_borrow_btcusd","bifi_borrow_usdc","bifi_borrow_usdt","bifi_borrow_dai","bifi_borrow_dollar",
 "bifi_borrowers","bifi_uw_count","bifi_uw_debt",
 "val_count","val_total_stake","nakamoto33","shells_active","new_contracts","jpysc_found","defi_tvl_usd","alert_p1","alert_p2","data_quality","chain_txns","chain_addrs"]
def append_csv(row):
    row=dict(row); row["date"]=datetime.date.today().isoformat()
    nonempty=lambda r:sum(1 for k in CSV_COLS if str(r.get(k,"")).strip()!="")
    rows=[]
    if os.path.exists(HIST):
        with open(HIST) as f: rows=list(csv.DictReader(f))
    same=[r for r in rows if r.get("date")==row["date"]]
    if same and nonempty(same[0])>nonempty(row):
        print(f"[history.csv: 오늘행 보존 — 기존 {nonempty(same[0])}열 > 이번 {nonempty(row)}열(부분실패 추정), 덮어쓰기 생략]"); return
    rows=[r for r in rows if r.get("date")!=row["date"]]+[{k:row.get(k,"") for k in CSV_COLS}]
    with open(HIST,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=CSV_COLS); w.writeheader()
        for r in rows: w.writerow({k:r.get(k,"") for k in CSV_COLS})
    print(f"[history.csv {len(rows)}행 · 오늘({row['date']}) 기록]")

def main():
    save="--no-save" not in sys.argv
    cur=snapshot(); old=json.load(open(BASE)) if os.path.exists(BASE) else {}
    row={"chain_txns":cur["_total_txns"],"chain_addrs":cur["_total_addr"],"price_usd":cur["_price"],"bfc_mcap_usd":round(cur["_mcap"])}
    print(f"# BFC 모니터 {datetime.date.today()}  price=${cur['_price']:.6f}  txns={cur['_total_txns']:,}")
    print(f"# 전 baseline 대비 ~{(cur['_ts']-old['_ts'])/3600:.1f}h" if old.get("_ts") else "# (첫 실행 — baseline 생성, Δ·집합diff는 다음 실행부터)")
    balances(cur,old,row)
    toksnap=token_check(old,row)
    bifi_check(row)
    validator_check(old,row)
    bifi_health_check(old,row)
    shellstate=shell_check(old,row)
    sc=deployer_scan(old,row)
    kt,jf=new_token_scan(old); row["jpysc_found"]=jf
    krw=exchange_check(cur,old); row["price_krw"]=krw if krw else ""
    bifi_price(row)
    defi_tvl(row)
    github_check(old); burn=burn_check(old)
    slow_drift_check(row)
    p1,p2=summary()
    row["alert_p1"]=p1; row["alert_p2"]=p2
    row["data_quality"]=f"{FETCH['ok']}/{FETCH['ok']+FETCH['fail']}"
    print(f"# 데이터품질(성공/시도 fetch): {row['data_quality']}")
    if save:
        os.makedirs(DATA,exist_ok=True)
        for k,v in toksnap.items():
            if v is not None: cur["tok_"+k]=v
        cur["known_tokens"]=kt; cur["val_addrs"]=row.pop("_val_addrs","")
        cur["seen_contracts"]=sc; cur.update(shellstate)
        cur.update(github_check.tags)
        if burn is not None: cur["burn_dead"]=burn
        json.dump(cur,open(BASE,"w"))
        append_csv(row)
        try:
            import report; report.generate(); print("[bifrost-daily-report.html 갱신]")
        except Exception as e: print(f"[리포트 생성 건너뜀: {e}]")
    else:
        row.pop("_val_addrs",None)
if __name__=="__main__": main()
