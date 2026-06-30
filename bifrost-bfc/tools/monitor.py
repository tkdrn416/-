#!/usr/bin/env python3
"""Bifrost(BFC) 정기 모니터링 — "딱 한 번 돌리면" 와치리스트 + 경보요약 + 오늘 판정.
사용:
  python3 monitor.py            # 스냅샷 + baseline 델타 + 🔔경보요약, baseline 갱신
  python3 monitor.py --no-save  # 갱신 없이 조회만
baseline: data/monitor-baseline.json (첫 실행이 생성, 델타·신규토큰 감지는 다음 실행부터)
출력 맨 아래 ═ 🔔 오늘의 경보 요약 ═ 만 봐도 "사건 발생 여부"를 즉시 판단 가능.
"""
import json,urllib.request,time,os,sys
API="https://explorer-backend.mainnet.thebifrost.io"
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.join(HERE,"..","data","monitor-baseline.json")
LOG=os.path.join(HERE,"..","data","monitor-events.log")
ALERTS=[]  # (priority 'P1'/'P2', message)
def alert(p,msg): ALERTS.append((p,msg))

WATCH=[
 # (라벨, 주소, 카테고리)
 ("업비트 콜드","0x50f187ef4447da6e5ff1d740439e91175bac955e","거래소"),
 ("업비트 핫","0x081a4ee55739f0da8abb8af40d07687527a268c3","거래소"),
 ("빗썸 콜드","0xdcd52f5f5af5022edefd59fd5353f4da3f2c8935","거래소"),
 ("빗썸 핫","0x39528d59132920ab0a637129d90cf9fb3650084d","거래소"),
 ("재단 Treasury","0x6d6f646c70792f74727372790000000000000000","재단핵심"),
 ("재단 BTCFi배포자 A30B97a5","0xa30b97a5485388d776c24c50dc82516726bb7a9b","재단"),
 ("재단 제네시스배포자 Dd505f3","0xdd505f3edb9b574d139e2f9d8b89deb6495de369","재단"),
 ("분배자 0x704cb96d","0x704cb96de875587bdde29a926d3a9cd6cbe7ad2f","재단"),
 ("분배자 0x313b1578(클러스터연결)","0x313b157854f61bc4b3f37c45a6a6c69a0e2b3ae3","재단/클러스터연결"),
 ("분배자 0x54c29770","0x54c2977027d7c25f2c733d754109550b8f88495f","재단"),
 ("순환클러스터 0x0c791e90","0x0c791e902d08b916218317d308156eb6a8a2d6d2","순환클러스터"),
 ("순환클러스터 0x4d0bbd3b","0x4d0bbd3bbcebbf7d826b00a57683f2fff643d184","순환클러스터"),
 ("순환클러스터 0xeb76c926","0xeb76c926e848e0bab9323e998eea16c9076563a5","순환클러스터"),
 ("순환클러스터 0xda50a0ff","0xda50a0ff48eda9b67a8fb2ba8274eec1e6351843","순환클러스터"),
 ("운용자 가스허브 0x81c22bec","0x81c22bec01c83e5bff125d3a52634dbef60d93d4","운용자네트워크"),
 ("볼트운용 EOA 0xaff29bed","0xaff29bedb24cc4979477f271f8a426590855cfca","운용자네트워크"),
 ("클러스터컨트롤러 0xb878526f","0xb878526f6d1174be9e75d1f617ae9271e4f42285","운용자네트워크"),
 ("InvestVault/Boost볼트 0xbc0995ca","0xbc0995cae2218203262ed1b8557b7886d579e985","BiFi볼트"),
 ("BiFi BFC풀(#3리저브) 0x4bAE7","0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee","재단핵심"),
 ("일본 JPYC venue 0x6894Ae31","0x6894ae31cae97f228590f6dc7bbea7449f4db980","일본"),
 ("BtcUSD시드 0x85b44cf6","0x85b44cf6d007e8a6ca16ee277e33c3223bb7db92","BtcUSD시드"),
 ("BtcUSD시드 0xcca25978","0xcca259780b2fbfa18f4ce3afb868f1be53220df6","BtcUSD시드"),
 ("액티브 유동성허브 0x09FCED81","0x09fced818439182812f13b006114da4382c4470e","유동성허브"),
]
TOKEN_WATCH=[
 ("Unified JPYC 총공급","0x84122a4a75bfe65ef455dba5f6d43d61359ca77e",500_000),
 ("BtcUSD 총공급","0x6906ccda405926fc3f04240187dd4fad5df6d555",500_000),
 ("Unified cbBTC(테스트)","0x74b73fd2ee237e9219df30dffdb206d237cbfc00",1),
 ("BrBTC 네이티브BTC브릿지(테스트)","0xcb4e4f67b33eebfc17c82cf6e8c0b56d269aeb79",1),
 ("stBFC 유동스테이킹총량","0xeff8378c6419b50c9d87f749f6852d96d4cc5ae4",13_000_000),
 ("wstBFC 래핑총량","0x386f2f5d9a97659c86f3ca9b8b11fc3f76efddae",13_000_000),
]
# 카테고리별 잔액변동 임계(BFC). 재단핵심(Treasury·#3리저브)=한번도 안 움직인 곳→어떤 변화든 P1.
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

def get(u):  # bifrost explorer
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(API+u,timeout=20))
        except: time.sleep(0.6)
    return {}
def get_url(u):  # 외부 거래소 API
    try:
        req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
        return json.load(urllib.request.urlopen(req,timeout=15))
    except: return {}
def bal(a): return int(get(f"/api/v2/addresses/{a}").get('coin_balance') or 0)/1e18
def fmt(v): return f"{v:+,.0f}" if v else "0"

def snapshot():
    snap={"_ts":int(time.time())}
    st=get("/api/v2/stats")
    snap["_price"]=float(st.get('coin_price') or 0)
    snap["_total_txns"]=st.get('total_transactions'); snap["_total_addr"]=st.get('total_addresses')
    for lab,a,cat in WATCH: snap[a]=bal(a)
    return snap

def balances(cur,old):
    print(f"\n{'라벨':<30}{'카테고리':<18}{'잔액BFC':>16}{'Δ':>14}")
    cat_delta={}
    for lab,a,cat in WATCH:
        v=cur[a]; d=v-old.get(a,v) if old else 0
        cat_delta[cat]=cat_delta.get(cat,0)+d
        th=CAT_THRESH.get(cat,DEFAULT_THRESH)
        flag=""
        if old and abs(d)>=th:
            flag=" ⚠️"
            if cat=="재단핵심" and d<0: alert("P1",f"★재단핵심 출금! {lab} {fmt(d)} BFC (한번도 안 움직이던 곳 → 첫 집행/매도 신호)")
            elif cat=="거래소" and d>0: alert("P1",f"거래소 콜드 순유입 {lab} {fmt(d)} BFC (매도압력)")
            elif cat=="거래소" and d<0: alert("P2",f"거래소 출금 {lab} {fmt(d)} BFC")
            else: alert("P2",f"{cat} 잔액변동 {lab} {fmt(d)} BFC")
        print(f"{lab:<30}{cat:<18}{v:>16,.0f}{fmt(d):>14}{flag}")
    if old:
        print("\n# 카테고리별 순변동:")
        for c,d in sorted(cat_delta.items(),key=lambda x:-abs(x[1])):
            print(f"  {c}: {fmt(d)} BFC")

def token_check(old):
    print("\n# 토큰 공급 추세:")
    snap={}
    for lab,addr,th in TOKEN_WATCH:
        t=get(f"/api/v2/tokens/{addr}")
        sup=int(t.get('total_supply') or 0)/10**int(t.get('decimals') or 18); hld=t.get('holders')
        snap[addr]=sup; d=sup-old.get("tok_"+addr,sup) if old else 0
        flag=" ⚠️" if old and abs(d)>=th else ""
        if flag: alert("P2",f"{lab} 공급 {fmt(d)} (현 {sup:,.0f})")
        print(f"  {lab:<22} {sup:>16,.0f}  (홀더 {hld})  Δ{fmt(d)}{flag}")
    return snap

def shell_check():
    print("\n# 스테이징 껍데기 11개 (자금유입=신제품 런칭):")
    act=0
    for a in STAGED_SHELLS:
        c=get(f"/api/v2/addresses/{a}/counters"); tt=int(c.get('token_transfers_count') or 0); bl=bal(a)
        if tt>0 or bl>0:
            act+=1; print(f"  ⚠️ 활성화! {a[:12]} token_xfers={tt} bal={bl:,.0f}BFC")
            alert("P1",f"★신제품 런칭 신호! 껍데기 {a[:12]} 활성화 (token_xfers={tt}, bal={bl:,.0f})")
    if act==0: print("  전부 빈 상태 유지(런칭 신호 없음).")

def new_token_scan(old):
    print("\n# 신규 토큰 출현 스캔(JPYSC 통합·신규 브릿지자산):")
    known=set(filter(None,(old.get("known_tokens") or "").split("|"))); cur=set(); n=0
    for q in NEW_TOKEN_QUERIES:
        for it in (get(f"/api/v2/tokens?q={q}").get('items') or [])[:12]:
            addr=(it.get('address') or '').lower(); sym=it.get('symbol') or ''
            if not addr: continue
            cur.add(addr)
            if 'JPYSC' in (sym+(it.get('name') or '')).upper():
                n+=1; print(f"  🚨 JPYSC 계열! {sym} {addr[:14]}"); alert("P1",f"🚨 JPYSC 계열 토큰 등장! {sym} {addr[:14]} (엔SC 통합 개시)")
            elif known and addr not in known:
                n+=1; print(f"  ⚠️ 신규: {sym} {addr[:14]}"); alert("P2",f"신규 토큰 등장: {sym} {addr[:14]}")
    if n==0: print("  신규 토큰 없음(JPYSC 미등장).")
    return "|".join(sorted(cur))

def exchange_check():
    print("\n# 거래소 시세·입출금 상태:")
    bt=get_url("https://api.bithumb.com/public/ticker/BFC_KRW").get('data') or {}
    if bt: print(f"  빗썸 BFC/KRW {bt.get('closing_price')}원 · 24h거래대금 {float(bt.get('acc_trade_value_24H') or 0)/1e8:,.1f}억")
    ast=get_url("https://api.bithumb.com/public/assetsstatus/BFC_KRW").get('data') or {}
    if ast:
        dep,wd=ast.get('deposit_status'),ast.get('withdrawal_status')
        print(f"  빗썸 입금={dep} 출금={wd} (1=정상,0=중단)")
        if dep==0 or wd==0: alert("P1",f"★빗썸 입출금 중단! 입금={dep} 출금={wd} (상장폐지/사고 신호 가능)")
    up=get_url("https://api.upbit.com/v1/ticker?markets=BTC-BFC")
    if isinstance(up,list) and up: print(f"  업비트 BTC-BFC {up[0].get('trade_price')} BTC · 24h변동 {float(up[0].get('signed_change_rate') or 0)*100:+.1f}%")

def summary(save):
    print("\n"+"═"*54)
    p1=[m for pr,m in ALERTS if pr=="P1"]; p2=[m for pr,m in ALERTS if pr=="P2"]
    if not ALERTS:
        print("🔔 오늘의 경보 요약:  ✅ 이상 무 — 감시 대상 전부 평소 범위")
    else:
        print(f"🔔 오늘의 경보 요약:  ⚠️ 사건 {len(ALERTS)}건 (P1 {len(p1)} · P2 {len(p2)})")
        for m in p1: print(f"  🔴 P1  {m}")
        for m in p2: print(f"  🟡 P2  {m}")
    print("═"*54)
    if save and ALERTS:
        try:
            import datetime
            with open(LOG,"a") as f:
                for pr,m in ALERTS: f.write(f"{int(time.time())}\t{pr}\t{m}\n")
        except: pass

def main():
    save="--no-save" not in sys.argv
    cur=snapshot()
    old=json.load(open(BASE)) if os.path.exists(BASE) else {}
    print(f"# BFC 모니터  price=${cur['_price']:.6f}  txns={cur['_total_txns']}  addrs={cur['_total_addr']}")
    if old.get("_ts"):
        print(f"# 전 baseline 대비 ~{(cur['_ts']-old['_ts'])/3600:.1f}h 경과")
    else:
        print("# (첫 실행 — baseline 생성. 델타·신규토큰 감지는 다음 실행부터)")
    balances(cur,old)
    toksnap=token_check(old)
    for k,v in toksnap.items(): cur["tok_"+k]=v
    shell_check()
    cur["known_tokens"]=new_token_scan(old)
    exchange_check()
    summary(save)
    if save:
        os.makedirs(os.path.dirname(BASE),exist_ok=True)
        json.dump(cur,open(BASE,"w"))
        print(f"[baseline 갱신: {os.path.relpath(BASE,HERE)} · 경보는 data/monitor-events.log 누적]")
if __name__=="__main__": main()
