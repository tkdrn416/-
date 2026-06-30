#!/usr/bin/env python3
"""Bifrost(BFC) 정기 모니터링 — 와치리스트 잔액/지표 스냅샷 + 전일 대비 델타.
사용:
  python3 monitor.py            # 스냅샷 출력 + baseline과 델타, baseline 갱신
  python3 monitor.py --no-save  # 갱신 없이 조회만
baseline: data/monitor-baseline.json (없으면 첫 실행이 생성, 델타는 다음 실행부터)
용도: 루프에서 거래소 순유입/출, 재단·순환클러스터 재가동, BiFi 볼트 변동 감시.
"""
import json,urllib.request,time,os,sys
API="https://explorer-backend.mainnet.thebifrost.io"
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.join(HERE,"..","data","monitor-baseline.json")
WATCH=[
 # (라벨, 주소, 카테고리)
 ("업비트 콜드","0x50f187ef4447da6e5ff1d740439e91175bac955e","거래소"),
 ("업비트 핫","0x081a4ee55739f0da8abb8af40d07687527a268c3","거래소"),
 ("빗썸 콜드","0xdcd52f5f5af5022edefd59fd5353f4da3f2c8935","거래소"),
 ("빗썸 핫","0x39528d59132920ab0a637129d90cf9fb3650084d","거래소"),
 ("재단 Treasury","0x6d6f646c70792f74727372790000000000000000","재단"),
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
 ("InvestVault 0xbc0995ca","0xbc0995cae2218203262ed1b8557b7886d579e985","BiFi볼트"),
 ("BiFi BFC풀 0x4bAE7","0x4bae7ba39e4e71660307dce780f1ec9b7b7666ee","BiFi풀"),
 ("일본 JPYC venue 0x6894Ae31","0x6894ae31cae97f228590f6dc7bbea7449f4db980","일본"),
 ("BtcUSD시드 0x85b44cf6","0x85b44cf6d007e8a6ca16ee277e33c3223bb7db92","BtcUSD시드"),
 ("BtcUSD시드 0xcca25978","0xcca259780b2fbfa18f4ce3afb868f1be53220df6","BtcUSD시드"),
]
# 토큰 잔액 감시(네이티브 아님): (라벨, 토큰주소, 보유주소) — 일본/BtcUSD 추세
TOKEN_WATCH=[
 ("Unified JPYC 총공급","0x84122a4a75bfe65ef455dba5f6d43d61359ca77e",None),
 ("BtcUSD 총공급","0x6906ccda405926fc3f04240187dd4fad5df6d555",None),
]
def get(u):
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(API+u,timeout=20))
        except: time.sleep(0.6)
    return {}
def bal(a): return int(get(f"/api/v2/addresses/{a}").get('coin_balance') or 0)/1e18
def snapshot():
    snap={"_ts":int(time.time())}
    st=get("/api/v2/stats")
    snap["_price"]=float(st.get('coin_price') or 0)
    snap["_total_txns"]=st.get('total_transactions')
    snap["_total_addr"]=st.get('total_addresses')
    for lab,a,cat in WATCH: snap[a]=bal(a)
    return snap
# 운용자(0xb878526f)가 2026 배포한 빈 업그레이더블-프록시 볼트 껍데기.
# 자금/토큰 받기 시작(token_transfers_count>0 or 잔액>0) = 신제품 런칭 신호.
STAGED_SHELLS=[
 "0xF4394659BB0303fa7bc69295F6115771198F718D","0x94B9A18CfB4b7D21a86b909871fd3d7898fb2bba",
 "0xB9b05cEeABd239A86CdA0bD5cd4aBa3eBB0F5f4C","0x6dedf09e8Fd216B823f63959d8daC25FBBfb6E25",
 "0x3f0BA9107758FACBad8948E138a71e18778Cb9DF","0xd7768f3477531FF5990735287E8fDd5a6a43B2bd",
 "0xD06B9B6A4A4F2FF72Fc2C7F9101E54f85F8a4e68","0xF2C269184F002677CC40099171470BB5f80e2719",
 "0x11d91B18bCE6bB6fF63F23Ee7b2B7660697daCFd","0xb0dd98593B4e353D682Be495C80D4928fA512B3b",
 "0x4a6dDEeC476073173CAB6f7Ff023f89CdB198931",
]
def shell_check():
    print("\n# 스테이징 껍데기 활성화 점검 (토큰유입=신제품 런칭 신호):")
    act=0
    for a in STAGED_SHELLS:
        c=get(f"/api/v2/addresses/{a}/counters")
        tt=int(c.get('token_transfers_count') or 0); bl=bal(a)
        if tt>0 or bl>0:
            act+=1; print(f"  ⚠️ 활성화! {a[:12]} token_xfers={tt} bal={bl:,.0f}BFC ← 신제품 런칭 가능")
    if act==0: print("  전부 빈 상태 유지(런칭 신호 없음).")
def token_supply(addr):
    t=get(f"/api/v2/tokens/{addr}")
    return int(t.get('total_supply') or 0)/10**int(t.get('decimals') or 18), t.get('holders')
def token_check(old):
    print("\n# 일본/스테이블 토큰 공급 추세:")
    snap={}
    for lab,addr,_ in TOKEN_WATCH:
        sup,hld=token_supply(addr); snap[addr]=sup
        d=sup-old.get("tok_"+addr,sup) if old else 0
        print(f"  {lab:<22} {sup:>16,.0f}  (홀더 {hld})  Δ{fmt(d)}")
    return snap
def fmt(v): return f"{v:+,.0f}" if v else "0"
def main():
    save="--no-save" not in sys.argv
    cur=snapshot()
    old={}
    if os.path.exists(BASE):
        old=json.load(open(BASE))
    print(f"# BFC 모니터 스냅샷  price=${cur['_price']:.6f}  txns={cur['_total_txns']}  addrs={cur['_total_addr']}")
    if old.get("_ts"):
        import datetime
        dt=(cur["_ts"]-old["_ts"])/3600
        print(f"# 전 baseline 대비 (~{dt:.1f}h 경과)")
    print(f"{'라벨':<26}{'카테고리':<16}{'잔액BFC':>16}{'Δ전일':>14}")
    cat_delta={}
    for lab,a,cat in WATCH:
        v=cur[a]; d=v-old.get(a,v) if old else 0
        cat_delta[cat]=cat_delta.get(cat,0)+d
        flag=" ⚠️" if old and abs(d)>100000 else ""
        print(f"{lab:<26}{cat:<16}{v:>16,.0f}{fmt(d):>14}{flag}")
    if old:
        print("\n# 카테고리별 순변동(Δ):")
        for c,d in sorted(cat_delta.items(),key=lambda x:-abs(x[1])):
            sig="유입(매도압?)" if (c=='거래소' and d>0) else ("출금" if c=='거래소' and d<0 else "")
            print(f"  {c}: {fmt(d)} BFC  {sig}")
    toksnap=token_check(old)
    for k,v in toksnap.items(): cur["tok_"+k]=v
    shell_check()
    if save:
        os.makedirs(os.path.dirname(BASE),exist_ok=True)
        json.dump(cur,open(BASE,"w"))
        print(f"\n[baseline 갱신: {os.path.relpath(BASE,HERE)}]")
if __name__=="__main__": main()
