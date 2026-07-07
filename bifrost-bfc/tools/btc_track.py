#!/usr/bin/env python3
# Bifrost BTCFi — BTC 예치지갑 추적기(수동 단계; 검증 후 데일리 루프 편입 예정)
#
# 대상: 바이프로스트에 native BTC를 브릿지-인해 담보로 맡긴 지갑들.
# 메커니즘(온체인 규명):
#   비트코인 L1 → 브릿지 → 'Unified BTC'(심볼 BTC, 0xB000F62A, 8dec) 민팅(from 0x0)
#   → 사용자가 담보볼트 0x59d36e5C 로 예치(lock) → BtcUSD(0x6906ccda…) 발행/차입
# 예치자 신원 = ①Unified BTC 민팅 수신자(브릿지-in) + ②담보볼트로 예치한 from 주소.
# (BrBTC 0xcb4e4f67 은 시스템 내부 회계용이라 개인 신원 안 보임 → Unified BTC 기준으로 추적)
#
# 사용: python3 tools/btc_track.py            # 스냅샷 출력 + baseline 저장(변화 diff)
#       python3 tools/btc_track.py --no-save  # 저장 없이 출력만
import urllib.request,json,time,urllib.parse,os,sys,datetime

API="https://explorer-backend.mainnet.thebifrost.io"
RPC="https://public-01.mainnet.bifrostnetwork.com/rpc"
UBTC="0xB000F62Ae7FB5E1D93E7358258B1abA754E0166A"    # Unified BTC 토큰(=유저 랩드BTC)
VAULT="0x59d36e5c61b1c4b55e250be9bc2dc5efa75603c6"   # BTC 담보볼트(잠금)
BTCUSD="0x6906ccda405926fc3f04240187dd4fad5df6d555"  # Bitcoin USD 스테이블
ZERO="0x0000000000000000000000000000000000000000"
TRACK_MIN=1.0   # 추적대상 기준: 누적 1 BTC 이상 예치한/예치했던 지갑(잠금유지·전액인출 모두 포함)
# 비트코인 L1 커스터디(유저 제보 앵커로 확립): Fireblocks P2WSH. 잔액≈Bifrost BTC볼트 잠금.
#   예치=여기로 입금(sender=예치자 BTC지갑) / 인출=여기서 출금(수취=예치자 BTC지갑, Bifrost 소각과 시각대조로 귀속)
BTC_CUSTODY="bc1qrrsnncu05rlappc4txuuf0rfltyc3crvewe49gqah83yaf3x4p7smnz47x"
MEMPOOL="https://mempool.space/api"
DATA=os.path.join(os.path.dirname(__file__),"..","data")
STATE=os.path.join(DATA,"btc-depositors.json")
L1STATE=os.path.join(DATA,"btc-l1-state.json")

def get(u):
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(API+u,timeout=25))
        except Exception: time.sleep(0.5)
    return {}
def mget(u):
    for _ in range(3):
        try:
            req=urllib.request.Request(MEMPOOL+u,headers={"User-Agent":"Mozilla/5.0"})
            return json.load(urllib.request.urlopen(req,timeout=25))
        except Exception: time.sleep(0.6)
    return None
def rpc(method,params):
    try:
        req=urllib.request.Request(RPC,data=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode(),headers={"Content-Type":"application/json"})
        return json.load(urllib.request.urlopen(req,timeout=20)).get("result")
    except Exception: return None
def erc20bal(tok,a,dec):
    r=rpc("eth_call",[{"to":tok,"data":"0x70a08231"+a[2:].rjust(64,"0")},"latest"])
    return int(r,16)/10**dec if r and r!="0x" else 0.0

def scan_transfers(maxpages=40):
    """Unified BTC 전송 전수 스캔 → 주소별 민팅/예치/인출 누적."""
    mint={}; dep={}; wd={}; nxt=None; n=0
    for _ in range(maxpages):
        u=f"/api/v2/tokens/{UBTC}/transfers"+("?"+urllib.parse.urlencode(nxt) if nxt else "")
        d=get(u); its=d.get("items",[])
        if not its: break
        for t in its:
            f=t.get("from",{}).get("hash","").lower(); to=t.get("to",{}).get("hash","").lower()
            try: amt=int(t.get("total",{}).get("value",0))/1e8
            except: amt=0
            if amt<=0: continue
            if f==ZERO: mint[to]=mint.get(to,0)+amt          # 브릿지-in(민팅)
            if to==VAULT: dep[f]=dep.get(f,0)+amt            # 담보 예치(lock)
            if f==VAULT and to!=ZERO: wd[to]=wd.get(to,0)+amt# 담보 인출(unlock)
        n+=len(its); nxt=d.get("next_page_params")
        if not nxt: break
        time.sleep(0.12)
    return mint,dep,wd,n

def btc_l1_check(save=True):
    """비트코인 L1 커스터디 감시 — 잔액·신규 예치(입금)·신규 인출(출금) 경보."""
    s=mget(f"/address/{BTC_CUSTODY}")
    if not s:
        print("\n# 비트코인 L1 커스터디: 조회 실패(mempool.space)"); return
    cs=s["chain_stats"]; bal=(cs["funded_txo_sum"]-cs["spent_txo_sum"])/1e8
    txn=cs["tx_count"]
    print(f"\n# 비트코인 L1 커스터디(bc1qrrsnncu…) 잔액 {bal:,.4f} BTC · tx {txn}")
    old=json.load(open(L1STATE)) if os.path.exists(L1STATE) else {}
    seen=set(old.get("seen_txids",[])); first=not seen
    txs=mget(f"/address/{BTC_CUSTODY}/txs") or []   # 최신 ~50건
    new_dep=[]; new_wd=[]
    for t in txs:
        txid=t.get("txid")
        if not txid or txid in seen: continue
        intoc=sum(v["value"] for v in t.get("vout",[]) if v.get("scriptpubkey_address")==BTC_CUSTODY)
        outofc=sum(v["prevout"]["value"] for v in t.get("vin",[]) if v.get("prevout",{}).get("scriptpubkey_address")==BTC_CUSTODY)
        if intoc>outofc:   # 예치(신규 자본 유입)
            sd=[v["prevout"].get("scriptpubkey_address") for v in t.get("vin",[]) if v.get("prevout",{}).get("scriptpubkey_address")!=BTC_CUSTODY]
            new_dep.append(((intoc-outofc)/1e8, sd[0] if sd else "?"))
        elif outofc>intoc: # 인출(이탈)
            rc=[v.get("scriptpubkey_address") for v in t.get("vout",[]) if v.get("scriptpubkey_address")!=BTC_CUSTODY and v["value"]>1e6]
            new_wd.append(((outofc-intoc)/1e8, rc[0] if rc else "?"))
        seen.add(txid)
    if first:
        print(f"  (첫 실행 — 커스터디 tx {len(txs)}건 시드, 다음 실행부터 신규분 경보)")
    else:
        for amt,who in new_dep:
            tag="P2" if amt>=1 else ""
            print(f"  ➕ 신규 BTC 예치 {amt:.4f} BTC ← {who[:20]}"+(f"  [{tag} ≥1BTC 신규 자본]" if tag else ""))
        for amt,who in new_wd:
            print(f"  ➖ BTC 인출(이탈) {amt:.4f} BTC → {who[:20]}"+("  [P1 대량 이탈]" if amt>=5 else "  [P2 이탈]"))
        if not new_dep and not new_wd: print("  변화 없음(신규 예치·인출 없음)")
    if save:
        os.makedirs(DATA,exist_ok=True)
        json.dump({"balance":round(bal,8),"tx_count":txn,
                   "seen_txids":list(seen)[-300:]},open(L1STATE,"w"))

def main():
    save="--no-save" not in sys.argv
    if "--l1" in sys.argv:   # 비트코인 L1만 빠르게 점검
        btc_l1_check(save); return
    mint,dep,wd,n=scan_transfers()
    # 시스템/볼트 자기자신·0x0 제외
    SYS={VAULT,UBTC.lower(),ZERO}
    addrs=sorted((set(mint)|set(dep))-SYS, key=lambda a:-(dep.get(a,0)))
    today=datetime.date.today().isoformat()
    print(f"# BTC 예치지갑 추적 {today}  (Unified BTC 전송 {n}건 스캔)")
    print(f"# 담보볼트 0x59d3 현재 잠금: {erc20bal(UBTC,VAULT,8):.6f} BTC · 예치자 {len(addrs)}명")
    print(f"\n{'주소':44}{'누적예치':>12}{'인출':>10}{'순예치BTC':>12}{'현BtcUSD':>12}")
    snap={}
    for a in addrs:
        net=dep.get(a,0)-wd.get(a,0)
        bu=erc20bal(BTCUSD,a,18)
        snap[a]={"minted":round(mint.get(a,0),8),"deposited":round(dep.get(a,0),8),
                 "withdrawn":round(wd.get(a,0),8),"net":round(net,8),"btcusd":round(bu,4)}
        if dep.get(a,0)>=0.01 or net>=0.01:  # 유의미분만 표시(먼지 테스터 생략)
            print(f"{a:44}{dep.get(a,0):>12,.5f}{wd.get(a,0):>10,.4f}{net:>12,.5f}{bu:>12,.2f}")
        time.sleep(0.03)
    # 추적대상(≥1 BTC 예치) 명시 — 잠금유지/전액인출(exit) 구분
    track={a:v for a,v in snap.items() if v["deposited"]>=TRACK_MIN}
    print(f"\n=== ★추적대상(누적예치 ≥{TRACK_MIN} BTC): {len(track)}명 · 누적 {sum(v['deposited'] for v in track.values()):.2f} BTC ===")
    for a,v in sorted(track.items(),key=lambda x:-x[1]['deposited']):
        st="잠금유지" if v['net']>=0.01 else "전액인출(exit)"
        print(f"  {a}  누적{v['deposited']:>8.3f} 순{v['net']:>8.3f} BTC  {st}")

    # 이전 baseline과 diff(신규 예치자/추가 예치/인출 감지)
    if os.path.exists(STATE):
        old=json.load(open(STATE)).get("depositors",{})
        print("\n=== 전 스냅샷 대비 변화 ===")
        chg=0
        for a,v in snap.items():
            ov=old.get(a)
            if ov is None:
                print(f"  🆕 신규 예치자 {a}  순예치 {v['net']:.5f} BTC"); chg+=1
            else:
                dd=v["deposited"]-ov.get("deposited",0); dw=v["withdrawn"]-ov.get("withdrawn",0)
                if dd>1e-6: print(f"  ➕ 추가예치 {a}  +{dd:.5f} BTC"); chg+=1
                if dw>1e-6: print(f"  ➖ 인출 {a}  -{dw:.5f} BTC (다른 서비스 이동 가능성 점검)"); chg+=1
        if not chg: print("  변화 없음")
    if save:
        os.makedirs(DATA,exist_ok=True)
        json.dump({"date":today,"vault_locked":round(erc20bal(UBTC,VAULT,8),8),
                   "track_min":TRACK_MIN,"tracked":sorted(track.keys()),
                   "depositors":snap},open(STATE,"w"),indent=1)
        print(f"\n[btc-depositors.json 저장 · 예치자 {len(snap)}명]")
    btc_l1_check(save)   # 비트코인 L1 커스터디 감시(잔액·신규 예치/인출)

if __name__=="__main__": main()
