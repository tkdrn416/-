#!/usr/bin/env python3
"""Bifrost(BFC) 모니터 — 와치리스트 경보 + 시계열 누적(history.csv) + 그래프 리포트.
사용:
  python3 monitor.py            # 점검 + 경보요약 + history.csv 1행 추가 + 리포트 갱신
  python3 monitor.py --no-save  # 누적/갱신 없이 조회만
출력:
  - 콘솔: 🔔 오늘의 경보 요약 (✅이상무 / ⚠️사건 N건)
  - data/history.csv          : 매 실행 1행 누적(엑셀 열람용)
  - data/monitor-baseline.json: 전 실행 대비 델타·집합diff 기준
  - data/monitor-events.log   : P1/P2 경보 누적 로그
  - bifrost-daily-report.html : CSV 기반 SVG 시계열 그래프 리포트(report.py 생성)
"""
import json,urllib.request,time,os,sys,csv,datetime
API="https://explorer-backend.mainnet.thebifrost.io"
RPC="https://public-01.mainnet.bifrostnetwork.com/rpc"
HERE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(HERE,"..","data")
BASE=os.path.join(DATA,"monitor-baseline.json")
HIST=os.path.join(DATA,"history.csv")
LOG=os.path.join(DATA,"monitor-events.log")
ALERTS=[]
def alert(p,m): ALERTS.append((p,m))

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
 ("BiFi BFC풀(#3리저브) 0x4bAE7","0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee","재단핵심"),
 ("일본 JPYC venue 0x6894Ae31","0x6894ae31cae97f228590f6dc7bbea7449f4db980","일본"),
 ("액티브 유동성허브 0x09FCED81","0x09fced818439182812f13b006114da4382c4470e","유동성허브"),
]
TOKEN_WATCH=[
 ("Unified JPYC 총공급","0x84122a4a75bfe65ef455dba5f6d43d61359ca77e",500_000,"jpyc_supply"),
 ("BtcUSD 총공급","0x6906ccda405926fc3f04240187dd4fad5df6d555",500_000,"btcusd_supply"),
 ("Unified cbBTC(테스트)","0x74b73fd2ee237e9219df30dffdb206d237cbfc00",1,"cbbtc_supply"),
 ("BrBTC 네이티브BTC브릿지(테스트)","0xcb4e4f67b33eebfc17c82cf6e8c0b56d269aeb79",1,"brbtc_supply"),
 ("stBFC 유동스테이킹총량","0xeff8378c6419b50c9d87f749f6852d96d4cc5ae4",13_000_000,"stbfc_supply"),
 ("wstBFC 래핑총량","0x386f2f5d9a97659c86f3ca9b8b11fc3f76efddae",13_000_000,"wstbfc_supply"),
]
CAT_THRESH={"거래소":5_000_000,"재단핵심":1,"운용자네트워크":1_000_000}
DEFAULT_THRESH=2_000_000
STAGED_SHELLS=[
 "0xF4394659BB0303fa7bc69295F6115771198F718D","0x94B9A18CfB4b7D21a86b909871fd3d7898fb2bba",
 "0xB9b05cEeABd239A86CdA0bD5cd4aBa3eBB0F5f4C","0x6dedf09e8Fd216B823f63959d8daC25FBBfb6E25",
 "0x3f0BA9107758FACBad8948E138a71e18778Cb9DF","0xd7768f3477531FF5990735287E8fDd5a6a43B2bd",
 "0xD06B9B6A4A4F2FF72Fc2C7F9101E54f85F8a4e68","0xF2C269184F002677CC40099171470BB5f80e2719",
 "0x11d91B18bCE6bB6fF63F23Ee7b2B7660697daCFd","0xb0dd98593B4e353D682Be495C80D4928fA512B3b",
 "0x4a6dDEeC476073173CAB6f7Ff023f89CdB198931",
]
NEW_TOKEN_QUERIES=["JPYSC","JPYC","cbBTC","BrBTC","Bridged"]
# BiFi 핸들러(예치물량 트렌드용)
BIFI_BFC_POOL="0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee"
WSTBFC_TOKEN="0x386f2f5d9a97659c86f3ca9b8b11fc3f76efddae"
WSTBFC_HANDLER="0xf9b2f6d2a61923e61ad9f6daa78f52b7e1722b12"
BTCUSD_TOKEN="0x6906ccda405926fc3f04240187dd4fad5df6d555"
BTCUSD_HANDLER="0xcf2fc1d354018a39d5ef036aa865ad8cbf7b611e"
STAKING_PRECOMPILE="0x0000000000000000000000000000000000000400"
CANDIDATE_POOL_SEL="0x96b41b5b"
BFC_ERC20="0x0c7D5ae016f806603CB1782bEa29AC69471CAb9c"

def get(u):
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(API+u,timeout=20))
        except: time.sleep(0.6)
    return {}
def get_url(u,timeout=15):
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        return json.load(urllib.request.urlopen(req,timeout=timeout))
    except: return None
def rpc(to,data):
    try:
        req=urllib.request.Request(RPC,data=json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":to,"data":data},"latest"]}).encode(),headers={"Content-Type":"application/json"})
        return json.load(urllib.request.urlopen(req,timeout=15)).get("result")
    except: return None
def bal(a): return int(get(f"/api/v2/addresses/{a}").get('coin_balance') or 0)/1e18
def erc20_bal(token,holder):
    r=rpc(token,"0x70a08231"+holder.lower().replace("0x","").rjust(64,"0"))
    return int(r,16)/1e18 if r and r!="0x" else None
def fmt(v): return f"{v:+,.0f}" if v else "0"

def snapshot():
    snap={"_ts":int(time.time())}
    st=get("/api/v2/stats")
    snap["_price"]=float(st.get('coin_price') or 0)
    snap["_total_txns"]=st.get('total_transactions'); snap["_total_addr"]=st.get('total_addresses')
    for lab,a,cat in WATCH: snap[a]=bal(a)
    return snap

def balances(cur,old,row):
    print(f"\n{'라벨':<32}{'카테고리':<18}{'잔액BFC':>16}{'Δ':>14}")
    up=bt=0
    for lab,a,cat in WATCH:
        v=cur[a]; d=v-old.get(a,v) if old else 0
        if "업비트" in lab: up+=v
        if "빗썸" in lab: bt+=v
        th=CAT_THRESH.get(cat,DEFAULT_THRESH); flag=""
        if old and abs(d)>=th:
            flag=" ⚠️"
            if cat=="재단핵심" and d<0: alert("P1",f"★재단핵심 출금! {lab} {fmt(d)} BFC (첫 집행/매도 신호)")
            elif cat=="거래소" and d>0: alert("P1",f"거래소 콜드 순유입 {lab} {fmt(d)} BFC (매도압력)")
            elif cat=="거래소": alert("P2",f"거래소 출금 {lab} {fmt(d)} BFC")
            else: alert("P2",f"{cat} 잔액변동 {lab} {fmt(d)} BFC")
        print(f"{lab:<32}{cat:<18}{v:>16,.0f}{fmt(d):>14}{flag}")
    row["upbit_bfc"]=round(up); row["bithumb_bfc"]=round(bt); row["exch_total"]=round(up+bt)
    row["treasury_bfc"]=round(cur.get("0x6d6f646c70792f74727372790000000000000000",0))

def token_check(old,row):
    print("\n# 토큰 공급 추세:")
    snap={}
    for lab,addr,th,col in TOKEN_WATCH:
        t=get(f"/api/v2/tokens/{addr}")
        sup=int(t.get('total_supply') or 0)/10**int(t.get('decimals') or 18); hld=t.get('holders')
        snap[addr]=sup; row[col]=round(sup)
        if col=="btcusd_supply": row["btcusd_holders"]=hld
        d=sup-old.get("tok_"+addr,sup) if old else 0
        flag=" ⚠️" if old and abs(d)>=th else ""
        if flag: alert("P2",f"{lab} 공급 {fmt(d)} (현 {sup:,.0f})")
        print(f"  {lab:<22} {sup:>16,.0f}  (홀더 {hld})  Δ{fmt(d)}{flag}")
    return snap

def bifi_check(row):
    print("\n# BiFi 예치물량(담보) 추세:")
    bfc=bal(BIFI_BFC_POOL); wst=erc20_bal(WSTBFC_TOKEN,WSTBFC_HANDLER); btc=erc20_bal(BTCUSD_TOKEN,BTCUSD_HANDLER)
    row["bifi_bfc_pool"]=round(bfc or 0); row["bifi_wstbfc"]=round(wst or 0); row["bifi_btcusd"]=round(btc or 0)
    print(f"  BiFi BFC풀 {bfc:,.0f} · wstBFC 담보 {wst or 0:,.0f} · BtcUSD 담보 {btc or 0:,.0f}")

def validator_check(old,row):
    print("\n# 검증자 집합·스테이크:")
    r=rpc(STAKING_PRECOMPILE,CANDIDATE_POOL_SEL)
    if not r or len(r)<130: print("  (조회 실패)"); return
    b=r[2:]
    try:
        o1=int(b[0:64],16)*2; o2=int(b[64:128],16)*2
        n=int(b[o1:o1+64],16); m=int(b[o2:o2+64],16)
        addrs=set("0x"+b[o1+64+i*64+24:o1+64+(i+1)*64] for i in range(n))
        stakes=[int(b[o2+64+i*64:o2+64+(i+1)*64],16)/1e18 for i in range(m)]
    except: print("  (디코딩 실패)"); return
    tot=sum(stakes); ss=sorted(stakes,reverse=True); cum=0; nak=0
    for i,s in enumerate(ss,1):
        cum+=s
        if cum>tot*0.333: nak=i; break
    row["val_count"]=n; row["val_total_stake"]=round(tot); row["nakamoto33"]=nak
    print(f"  검증자 {n}개 · 총스테이크 {tot:,.0f} · Nakamoto(33%) {nak}")
    prev=set(filter(None,(old.get("val_addrs") or "").split(","))) if old else set()
    if prev:
        new=addrs-prev; gone=prev-addrs
        for x in new: alert("P1",f"★신규 검증자 등장 {x[:12]} (집합 변동)")
        for x in gone: alert("P1",f"★검증자 이탈 {x[:12]} (집합 변동)")
    row["_val_addrs"]=",".join(sorted(addrs))

def shell_check():
    print("\n# 스테이징 껍데기 11개 (자금유입=신제품 런칭):")
    act=0
    for a in STAGED_SHELLS:
        c=get(f"/api/v2/addresses/{a}/counters"); tt=int(c.get('token_transfers_count') or 0); bl=bal(a)
        if tt>0 or bl>0:
            act+=1; print(f"  ⚠️ 활성화! {a[:12]} xfers={tt} bal={bl:,.0f}"); alert("P1",f"★신제품 런칭! 껍데기 {a[:12]} 활성화(xfers={tt},bal={bl:,.0f})")
    if act==0: print("  전부 빈 상태(런칭 신호 없음).")

def new_token_scan(old):
    print("\n# 신규 토큰 출현 스캔(JPYSC·신규 브릿지):")
    known=set(filter(None,(old.get("known_tokens") or "").split("|"))); cur=set(); n=0
    for q in NEW_TOKEN_QUERIES:
        for it in (get(f"/api/v2/tokens?q={q}").get('items') or [])[:12]:
            addr=(it.get('address') or '').lower(); sym=it.get('symbol') or ''
            if not addr: continue
            cur.add(addr)
            if 'JPYSC' in (sym+(it.get('name') or '')).upper():
                n+=1; print(f"  🚨 JPYSC! {sym} {addr[:14]}"); alert("P1",f"🚨 JPYSC 계열 토큰 등장! {sym} {addr[:14]}")
            elif known and addr not in known:
                n+=1; print(f"  ⚠️ 신규 {sym} {addr[:14]}"); alert("P2",f"신규 토큰 {sym} {addr[:14]}")
    if n==0: print("  신규 없음(JPYSC 미등장).")
    return "|".join(sorted(cur))

def exchange_check(cur,old,row):
    print("\n# 거래소 시세·입출금:")
    row["price_usd"]=cur["_price"]
    bt=(get_url("https://api.bithumb.com/public/ticker/BFC_KRW") or {}).get('data') or {}
    if bt:
        row["price_krw"]=bt.get('closing_price'); print(f"  빗썸 {bt.get('closing_price')}원 · 24h대금 {float(bt.get('acc_trade_value_24H') or 0)/1e8:,.1f}억")
    ast=(get_url("https://api.bithumb.com/public/assetsstatus/BFC_KRW") or {}).get('data') or {}
    if ast:
        dep,wd=ast.get('deposit_status'),ast.get('withdrawal_status'); print(f"  빗썸 입금={dep} 출금={wd}")
        if dep==0 or wd==0: alert("P1",f"★빗썸 입출금 중단! 입금={dep} 출금={wd}")
    # 가격 급변(전 실행 대비 ±10%)
    if old.get("_price"):
        ch=(cur["_price"]-old["_price"])/old["_price"]*100
        if abs(ch)>=10: alert("P1",f"★가격 급변 {ch:+.1f}% (${old['_price']:.5f}→${cur['_price']:.5f})")

def defi_tvl(row):
    chains=get_url("https://api.llama.fi/v2/chains") or []
    for c in chains if isinstance(chains,list) else []:
        if 'bifrost' in (c.get('name','').lower()) and 'network' in (c.get('name','').lower()):
            row["defi_tvl_usd"]=round(c.get('tvl') or 0); print(f"\n# DefiLlama 체인 TVL: ${row['defi_tvl_usd']:,.0f}"); return

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
    info=get_url(f"https://api.ethplorer.io/getAddressInfo/0x000000000000000000000000000000000000dEaD?apiKey=freekey",20)
    if not info: return None
    for tk in (info.get('tokens') or []):
        if (tk.get('tokenInfo') or {}).get('address','').lower()==BFC_ERC20.lower():
            v=float(tk.get('rawBalance',0))/1e18
            if old.get("burn_dead") and v>old["burn_dead"]+1: alert("P1",f"★소각 재개! dead +{v-old['burn_dead']:,.0f} BFC")
            return v
    return None

def summary(save):
    print("\n"+"═"*56)
    p1=[m for p,m in ALERTS if p=="P1"]; p2=[m for p,m in ALERTS if p=="P2"]
    if not ALERTS: print("🔔 오늘의 경보 요약:  ✅ 이상 무 — 전부 평소 범위")
    else:
        print(f"🔔 오늘의 경보 요약:  ⚠️ 사건 {len(ALERTS)}건 (P1 {len(p1)}·P2 {len(p2)})")
        for m in p1: print(f"  🔴 P1  {m}")
        for m in p2: print(f"  🟡 P2  {m}")
    print("═"*56)
    if save and ALERTS:
        try:
            with open(LOG,"a") as f:
                for p,m in ALERTS: f.write(f"{datetime.datetime.now().isoformat()}\t{p}\t{m}\n")
        except: pass

CSV_COLS=["date","price_usd","price_krw","upbit_bfc","bithumb_bfc","exch_total","treasury_bfc",
 "jpyc_supply","btcusd_supply","btcusd_holders","stbfc_supply","wstbfc_supply","cbbtc_supply","brbtc_supply",
 "bifi_bfc_pool","bifi_wstbfc","bifi_btcusd","val_count","val_total_stake","nakamoto33","defi_tvl_usd",
 "chain_txns","chain_addrs"]
def append_csv(row):
    row=dict(row); row["date"]=datetime.date.today().isoformat()
    new=not os.path.exists(HIST)
    # 같은 날짜 행 있으면 갱신(중복 방지)
    rows=[]
    if not new:
        with open(HIST) as f: rows=list(csv.DictReader(f))
        rows=[r for r in rows if r.get("date")!=row["date"]]
    rows.append({k:row.get(k,"") for k in CSV_COLS})
    with open(HIST,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=CSV_COLS); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"[history.csv {len(rows)}행 · 오늘({row['date']}) 기록]")

def main():
    save="--no-save" not in sys.argv
    cur=snapshot(); old=json.load(open(BASE)) if os.path.exists(BASE) else {}
    row={"chain_txns":cur["_total_txns"],"chain_addrs":cur["_total_addr"]}
    print(f"# BFC 모니터 {datetime.date.today()}  price=${cur['_price']:.6f}  txns={cur['_total_txns']}")
    print(f"# 전 baseline 대비 ~{(cur['_ts']-old['_ts'])/3600:.1f}h" if old.get("_ts") else "# (첫 실행 — baseline 생성)")
    balances(cur,old,row)
    toksnap=token_check(old,row)
    bifi_check(row)
    validator_check(old,row)
    shell_check()
    kt=new_token_scan(old)
    exchange_check(cur,old,row)
    defi_tvl(row)
    github_check(old)
    burn=burn_check(old)
    summary(save)
    if save:
        os.makedirs(DATA,exist_ok=True)
        for k,v in toksnap.items(): cur["tok_"+k]=v
        cur["known_tokens"]=kt; cur["val_addrs"]=row.pop("_val_addrs","")
        cur.update({k:v for k,v in github_check.tags.items()})
        if burn is not None: cur["burn_dead"]=burn
        json.dump(cur,open(BASE,"w"))
        append_csv(row)
        try:
            import report; report.generate(); print("[bifrost-daily-report.html 갱신]")
        except Exception as e: print(f"[리포트 생성 건너뜀: {e}]")
if __name__=="__main__": main()
