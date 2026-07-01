#!/usr/bin/env python3
"""data/history.csv → bifrost-daily-report.html
레이아웃(위→아래): 신호등 상태보드 → 핵심 KPI(변화·색상) → 전일/전주 Δ표 → 핵심차트6 → 기타차트(접기) → 경보 → 커스텀 빌더.
외부 의존 0. monitor.py가 report.generate() 호출. 단독: python3 report.py
"""
import os,csv,json,datetime
HERE=os.path.dirname(os.path.abspath(__file__))
HIST=os.path.join(HERE,"..","data","history.csv"); LOG=os.path.join(HERE,"..","data","monitor-events.log")
OUT=os.path.join(HERE,"..","bifrost-daily-report.html")
WST_RATE=1.137; CIRC=1_390_000_000

def _num(v):
    try: return float(v)
    except: return None
def _fmt(v,unit=""):
    if v is None: return "—"
    a=abs(v)
    if unit=="$": return f'${v:,.5f}' if a<1 else f'${v:,.2f}'
    if unit=="원": return f'{v:,.2f}원' if a<10 else f'{v:,.1f}원'
    if unit=="%": return f'{v:,.1f}%'
    if a>=1e8: return f'{v/1e6:,.0f}M'
    if a>=1e6: return f'{v/1e6:,.2f}M'
    if a>=1e3: return f'{v/1e3:,.0f}K'
    return f'{v:,.0f}'
def _fmtc(v,unit=""):
    """표·타일용 압축 표기: 큰 금액도 M/K로(스캔성). 소액 가격은 원형 유지."""
    if v is None: return "—"
    a=abs(v)
    if unit=="%": return f'{v:,.1f}%'
    if unit in ("$","원") and a<1000:  # 가격류 소액은 정밀
        return _fmt(v,unit)
    pfx="$" if unit=="$" else ""; sfx="원" if unit=="원" else ""
    if a>=1e8: return f'{pfx}{v/1e6:,.0f}M{sfx}'
    if a>=1e6: return f'{pfx}{v/1e6:,.2f}M{sfx}'
    if a>=1e3: return f'{pfx}{v/1e3:,.1f}K{sfx}'
    return f'{pfx}{v:,.0f}{sfx}'

def augment(rows):
    for r in rows:
        p=_num(r.get("price_usd")); bfc=_num(r.get("bifi_bfc_pool")); wst=_num(r.get("bifi_wstbfc")); btc=_num(r.get("bifi_btcusd"))
        r["coll_bfc_usd"]=round(bfc*p) if (bfc is not None and p) else ""
        r["coll_wstbfc_usd"]=round(wst*p*WST_RATE) if (wst is not None and p) else ""
        r["coll_btcusd_usd"]=round(btc) if btc is not None else ""
        parts=[_num(r.get(k)) for k in ("coll_bfc_usd","coll_wstbfc_usd","coll_btcusd_usd")]
        ct=sum(x for x in parts if x is not None) if any(x is not None for x in parts) else None
        r["coll_total_usd"]=round(ct) if ct is not None else ""
        bo=_num(r.get("bifi_borrow_dollar"))
        r["util_pct"]=round(bo/ct*100,1) if (bo is not None and ct) else ""
        r["collat_ratio"]=round(ct/bo*100,1) if (bo and ct is not None) else ""
        ex=_num(r.get("exch_total")); r["exch_pct"]=round(ex/CIRC*100,1) if ex is not None else ""
    return rows

CATALOG=[
 ("price_usd","BFC 가격($)","$"),("price_krw","BFC 가격(원)","원"),("bfc_mcap_usd","BFC 시총($)","$"),("bifi_price_usd","BIFI 가격($)","$"),("bifi_price_krw","BIFI 가격(원)","원"),("bifi_mcap_usd","BIFI 시총($)","$"),
 ("coll_total_usd","BiFi 예치합계($)","$"),("bifi_borrow_dollar","BiFi 달러대출($)","$"),("util_pct","BiFi 이용률(%)","%"),
 ("coll_bfc_usd","BiFi BFC담보($)","$"),("coll_wstbfc_usd","BiFi wstBFC담보($)","$"),("coll_btcusd_usd","BiFi BtcUSD담보($)","$"),
 ("bifi_borrow_btcusd","대출 BtcUSD","$"),("bifi_borrow_usdc","대출 USDC","$"),("bifi_borrow_usdt","대출 USDT","$"),("bifi_borrow_dai","대출 DAI","$"),
 ("bifi_uw_debt","BiFi 미청산 부채($)","$"),("bifi_uw_count","BiFi 미청산 건수","n"),("bifi_borrowers","BiFi 차입자수","n"),
 ("exch_total","거래소 보유(BFC)","BFC"),("htx_bfc","HTX 운영지갑(BFC)","BFC"),("exch_pct","거래소 보유비중(%)","%"),("btcusd_supply","BtcUSD 발행","BFC"),("jpyc_supply","일본 JPYC","BFC"),
 ("stbfc_supply","유동스테이킹(stBFC)","BFC"),("val_total_stake","검증자 스테이크","BFC"),("nakamoto33","Nakamoto","n"),("treasury_bfc","Treasury","BFC"),("new_contracts","운용자 신규컨트랙트","n"),("shells_active","활성 껍데기","n"),
 ("defi_tvl_usd","DefiLlama TVL($)","$"),
]

def build_signals(rows):
    """신호칩 계산 — signal_board·verdict 공용(로직 단일화). 반환: [(라벨,색g/y/r,값텍스트)]"""
    cur=rows[-1]; prev=rows[-2] if len(rows)>1 else {}
    d=lambda k:(_num(cur.get(k))-_num(prev.get(k))) if _num(cur.get(k)) is not None and _num(prev.get(k)) is not None else None
    chips=[]
    a1=_num(cur.get("alert_p1")) or 0
    chips.append(("P1 경보","r" if a1 else "g", f"{a1:.0f}건" if a1 else "없음"))
    tf=d("treasury_bfc"); chips.append(("Treasury 유출","r" if (tf is not None and tf<0) else "g", "유출!" if (tf is not None and tf<0) else "미집행 유지"))
    nc=_num(cur.get("new_contracts"))
    if nc is not None: chips.append(("운용자 신규컨트랙트","r" if nc>0 else "g", f"{nc:.0f}건!" if nc>0 else "없음"))
    sh=_num(cur.get("shells_active")); chips.append(("빈지갑 자금유입","r" if (sh and sh>0) else "g", f"{sh:.0f}/11" if sh is not None else "0/11"))
    jp=_num(cur.get("jpysc_found")); chips.append(("JPYSC 출현","y" if (jp and jp>0) else "g", "발견!" if (jp and jp>0) else "미발견"))
    ef=_num(cur.get("exch_net_flow"));
    if ef is None: chips.append(("거래소 순흐름","g","—"))
    elif ef>5_000_000: chips.append(("거래소 순유입","r",f"+{_fmt(ef)} 매도압"))
    elif ef>0: chips.append(("거래소 순유입","y",f"+{_fmt(ef)}"))
    else: chips.append(("거래소 순흐름","g",f"{_fmt(ef)}"))
    u=_num(cur.get("util_pct"))
    if u is not None: chips.append(("BiFi 이용률","r" if u>90 else ("y" if u>75 else "g"),f"{u:.0f}%"))
    uw=_num(cur.get("bifi_uw_count")); uwd=_num(cur.get("bifi_uw_debt"))
    if uw is not None:
        c="r" if (uwd and uwd>2_000_000) else ("y" if uw>0 else "g")
        chips.append(("BiFi 미청산(UW)",c,(f"{uw:.0f}명 ${_fmt(uwd)}" if uw>0 else "없음")))
    pu=_num(cur.get("price_usd")); pp=_num(prev.get("price_usd"))
    if pu is not None and pp: ch=(pu-pp)/pp*100; chips.append(("BFC 가격 24h","y" if abs(ch)>=10 else "g",f"{ch:+.1f}%"))
    return chips

def verdict(rows):
    """상단 go/no-go 지시문 — 빨강/노랑 칩만 뽑아 '오늘 확인할 것'으로 요약."""
    chips=build_signals(rows)
    reds=[l for l,c,_ in chips if c=="r"]; yels=[l for l,c,_ in chips if c=="y"]
    if reds:   return ("r", f"⚠️ 오늘 확인 필요 — {', '.join(reds)}"+(f" · 주의: {', '.join(yels)}" if yels else ""))
    if yels:   return ("y", f"🟡 관찰 권장 — {', '.join(yels)} (긴급 아님)")
    return ("g", "✅ 이상 없음 — 특이신호 0. 오늘은 스킵 가능(가격/추세만 확인).")

def signal_board(rows):
    chips=build_signals(rows)
    col={"g":"#34d399","y":"#fbbf24","r":"#f87171"}; ico={"g":"🟢","y":"🟡","r":"🔴"}
    cells="".join(f'<div class="chip" style="border-color:{col[c]}"><div class="ci">{ico[c]} {lab}</div><div class="cv" style="color:{col[c]}">{val}</div></div>' for lab,c,val in chips)
    return f'<div class="sigboard">{cells}</div>'

def svg_chart(rows,cols,title,unit="",colors=None,h=190):
    colors=colors or ["#4da3ff","#fbbf24","#34d399","#f87171","#b794ff"]
    W,H=720,h; PADL,PADR,PADT,PADB=66,16,30,32
    series=[(lab,[(r["date"],_num(r.get(col))) for r in rows if _num(r.get(col)) is not None]) for col,lab in cols]
    series=[s for s in series if s[1]]
    if not series:
        return f'<div class="ch"><svg viewBox="0 0 {W} 70" width="100%" style="max-width:{W}px"><text x="12" y="22" fill="#e5e7eb" font-size="12" font-weight="700">{title}</text><text x="12" y="46" fill="#6b7280" font-size="11">데이터 누적 대기</text></svg></div>'
    npts=max(len(pts) for _,pts in series)
    allv=[v for _,pts in series for _,v in pts]; lo,hi=min(allv),max(allv)
    mid=(hi+lo)/2; nearflat=False
    if hi==lo:  # 평탄: 부호안전 패딩(음수축 방지)
        pad=abs(lo)*0.05 or 1; hi=lo+pad; lo=(lo-pad) if lo<0 else max(0,lo-pad)
    elif mid and (hi-lo)<abs(mid)*0.01:  # 변동 <1%: 전체높이 자동스케일=오해 → 축 넓혀 평탄히
        nearflat=(hi-lo)/abs(mid)*100; pad=abs(mid)*0.02
        lo=(mid-pad) if mid<0 else max(0,mid-pad); hi=mid+pad
    drawn=[(lab,(pts*2 if len(pts)==1 else pts)) for lab,pts in series]; n=max(len(pts) for _,pts in drawn)
    X=lambda i:PADL+(W-PADL-PADR)*(i/(n-1) if n>1 else 0.5); Y=lambda v:PADT+(H-PADT-PADB)*(1-(v-lo)/(hi-lo))
    g=[f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px;background:#0d1117;border:1px solid #1f2937;border-radius:8px" font-family="ui-sans-serif,system-ui">',
       f'<text x="12" y="18" fill="#e5e7eb" font-size="12" font-weight="700">{title}</text>']
    if nearflat: g.append(f'<text x="{W-PADR}" y="18" fill="#6b7280" font-size="9" text-anchor="end">변동 &lt;1% (≈보합)</text>')
    elif npts<3: g.append(f'<text x="{W-PADR}" y="18" fill="#6b7280" font-size="9" text-anchor="end">데이터 {npts}p·추세는 3회+</text>')
    for k in range(4):
        yv=lo+(hi-lo)*k/3; yy=Y(yv)
        g.append(f'<line x1="{PADL}" y1="{yy:.0f}" x2="{W-PADR}" y2="{yy:.0f}" stroke="#1b212b"/><text x="{PADL-6}" y="{yy+3:.0f}" fill="#6b7280" font-size="9" text-anchor="end">{_fmt(yv,unit)}</text>')
    fd,ld=drawn[0][1][0][0],drawn[0][1][-1][0]
    g.append(f'<text x="{PADL}" y="{H-6}" fill="#6b7280" font-size="9">{fd}</text><text x="{W-PADR}" y="{H-6}" fill="#6b7280" font-size="9" text-anchor="end">{ld}</text>')
    for si,(lab,pts) in enumerate(drawn):
        c=colors[si%len(colors)]; d=" ".join(f'{"M" if i==0 else "L"} {X(i):.0f} {Y(v):.0f}' for i,(_,v) in enumerate(pts))
        g.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2"/>')
        for i,(_,v) in enumerate(pts): g.append(f'<circle cx="{X(i):.0f}" cy="{Y(v):.0f}" r="2.5" fill="{c}"/>')
    if len(series)>1:
        lx=PADL
        for si,(lab,_) in enumerate(series):
            c=colors[si%len(colors)]; g.append(f'<rect x="{lx}" y="23" width="9" height="9" rx="2" fill="{c}"/><text x="{lx+12}" y="31" fill="#cbd5e1" font-size="10">{lab}</text>'); lx+=len(lab)*8+34
    g.append(f'<text x="{W-PADR}" y="{H-20}" fill="#9aa3b2" font-size="10" text-anchor="end">최신 {_fmt(series[0][1][-1][1],unit)}</text></svg>')
    return f'<div class="ch">{"".join(g)}</div>'

# 증가가 좋은지(good_up) valence 기반 화살표. thr 미만 변동은 회색(노이즈 억제)
def arrow(d,good_up=True,thr=0,unit=""):
    if d is None: return '<span class="flat">—</span>'
    if d==0 or (thr and abs(d)<thr): return f'<span class="flat">→ ~0</span>'
    good=(d>0)==good_up; cls="pos" if good else "neg"; sym="▲ +" if d>0 else "▼ "
    return f'<span class="{cls}">{sym}{_fmtc(abs(d) if d<0 else d,unit)}</span>'
def change_table(rows):
    cur=rows[-1]; prev=rows[-2] if len(rows)>1 else None; wk=rows[-8] if len(rows)>=8 else None
    # (키,라벨,단위,good_up,유의임계)
    M=[("price_usd","BFC 가격(USD)","$",True,0),("price_krw","BFC 가격(KRW)","원",True,0),("bifi_price_usd","BIFI 가격(USD)","$",True,0),
     ("exch_total","거래소 보유","",False,1_000_000),("exch_net_flow","거래소 순흐름","",False,1_000_000),("treasury_bfc","Treasury","",True,1),
     ("btcusd_supply","BtcUSD 발행","",True,200_000),("coll_total_usd","BiFi 예치($)","$",True,500_000),("bifi_borrow_dollar","BiFi 달러대출($)","$",True,100_000),
     ("util_pct","BiFi 이용률","%",True,3),("bifi_uw_debt","BiFi 미청산 부채($)","$",False,100_000),("jpyc_supply","JPYC","",True,200_000),("stbfc_supply","유동스테이킹","",True,1_000_000),
     ("val_total_stake","검증자 스테이크","",True,1_000_000),("nakamoto33","Nakamoto","",True,1),("defi_tvl_usd","TVL","$",True,300_000)]
    out=['<table><tr><th>지표</th><th class="r">현재</th><th class="r">전일Δ</th><th class="r">전주Δ</th></tr>']
    for col,lab,u,gu,thr in M:
        c=_num(cur.get(col))
        if c is None: continue
        dp=(c-_num(prev.get(col))) if prev and _num(prev.get(col)) is not None else None
        dw=(c-_num(wk.get(col))) if wk and _num(wk.get(col)) is not None else None
        hl=' class="hot"' if (dp is not None and abs(dp)>=thr and thr>0) else ''
        out.append(f'<tr{hl}><td>{lab}</td><td class="r">{_fmtc(c,u)}</td><td class="r">{arrow(dp,gu,thr,u)}</td><td class="r">{arrow(dw,gu,thr,u)}</td></tr>')
    return "".join(out)+"</table>"

def narrative(rows):
    if len(rows)<2: return "데이터 1포인트 — 내러티브·추세는 2회차부터."
    cur,prev=rows[-1],rows[-2]
    d=lambda c:(_num(cur.get(c))-_num(prev.get(c))) if _num(cur.get(c)) is not None and _num(prev.get(c)) is not None else None
    bits=[]; pf=d("price_usd")
    if pf is not None and _num(prev.get("price_usd")): bits.append(f"BFC {pf/_num(prev['price_usd'])*100:+.1f}%")
    for col,lab,thr in [("exch_total","거래소",1_000_000),("treasury_bfc","Treasury",1),("btcusd_supply","BtcUSD",200_000),
      ("bifi_borrow_dollar","달러대출",100_000),("coll_total_usd","예치($)",500_000),("jpyc_supply","JPYC",200_000)]:
        x=d(col)
        if x is not None and abs(x)>=thr: bits.append(f"{lab} {_fmt(x)}")
    a1=_num(cur.get("alert_p1")) or 0
    return (f"⚠️ P1 경보 {a1:.0f}건" if a1 else "✅ P1 경보 없음")+(" · "+", ".join(bits) if bits else " · 주요지표 변동 미미")

def recent_alerts(k=25):
    if not os.path.exists(LOG): return []
    try: lines=open(LOG).read().strip().split("\n")
    except: return []
    return [(p[0][:16].replace("T"," "),p[1],p[2]) for p in (ln.split("\t") for ln in lines[-k:][::-1]) if len(p)>=3]

def generate():
    if not os.path.exists(HIST): return
    rows=augment([r for r in csv.DictReader(open(HIST)) if r.get("date")])
    if not rows: return
    last=rows[-1]; prev=rows[-2] if len(rows)>1 else {}
    # 핵심 차트 = 미션 4대 감시(매도압·재단집행·렌딩청산·CDP부채)에 직결된 것만
    core=[
        svg_chart(rows,[("exch_total","거래소합"),("upbit_bfc","업비트"),("bithumb_bfc","빗썸"),("htx_bfc","HTX운영")],"① 거래소 보유 BFC (순유입=매도압)"),
        svg_chart(rows,[("treasury_bfc","Treasury")],"② 재단 Treasury (출금=P1 신호)"),
        svg_chart(rows,[("coll_total_usd","예치($)"),("bifi_borrow_dollar","대출($)")],"③ BiFi 예치 vs 대출 (달러)","$"),
        svg_chart(rows,[("util_pct","이용률%")],"④ BiFi 이용률 (대출/예치·청산근접도)","%"),
        svg_chart(rows,[("bifi_uw_debt","미청산부채$")],"⑤ BiFi 미청산(UNDERWATER) 부채 — 자동추적","$"),
        svg_chart(rows,[("btcusd_supply","BtcUSD")],"⑥ BtcUSD 발행 (=CDP 부채)"),
        svg_chart(rows,[("price_usd","BFC/USD")],"BFC 가격 (USD)","$"),
    ]
    etc=[
        svg_chart(rows,[("bfc_mcap_usd","BFC 시총")],"BFC 시가총액 (USD)","$"),
        svg_chart(rows,[("bifi_price_usd","BIFI/USD")],"BIFI 곡괭이토큰 (USD)","$"),
        svg_chart(rows,[("bifi_mcap_usd","BIFI 시총")],"BIFI 시가총액 (USD)","$"),
        svg_chart(rows,[("coll_bfc_usd","BFC담보"),("coll_wstbfc_usd","wstBFC담보"),("coll_btcusd_usd","BtcUSD담보")],"BiFi 담보 구성(달러환산)","$"),
        svg_chart(rows,[("bifi_borrow_btcusd","BtcUSD"),("bifi_borrow_usdc","USDC"),("bifi_borrow_usdt","USDT"),("bifi_borrow_dai","DAI")],"달러대출 구성(개별)","$"),
        svg_chart(rows,[("jpyc_supply","JPYC")],"일본 JPYC 공급"),
        svg_chart(rows,[("stbfc_supply","stBFC")],"Biquid 유동스테이킹"),
        svg_chart(rows,[("val_total_stake","총스테이크")],"검증자 총 스테이크"),
        svg_chart(rows,[("defi_tvl_usd","TVL")],"DefiLlama TVL","$"),
        svg_chart(rows,[("new_contracts","신규컨트랙트"),("shells_active","활성껍데기")],"운용자 신규 컨트랙트·활성 껍데기(물밑 신호)"),
        svg_chart(rows,[("alert_p1","P1"),("alert_p2","P2")],"일별 경보 건수"),
    ]
    dates=[r["date"] for r in rows]; series={key:[_num(r.get(key)) for r in rows] for key,_,_ in CATALOG}
    DATA=json.dumps({"dates":dates,"series":series,"cat":[{"k":k,"lab":lab,"u":u} for k,lab,u in CATALOG]})
    al=recent_alerts(); alopen=" open" if al else ""
    albox="".join(f'<tr><td class="small">{t}</td><td><span class="b-{ "bad" if p=="P1" else "warn"}">{p}</span></td><td class="wrap small">{m}</td></tr>' for t,p,m in al) or '<tr><td colspan="3" class="muted small">최근 기록된 경보 없음</td></tr>'
    # KPI 타일(값 + 전일Δ + valence색)
    def kpi(key,label,uf,unit="",good_up=True,thr=0):
        v=_num(last.get(key)); pv=_num(prev.get(key)); dd=(v-pv) if (v is not None and pv is not None) else None
        val=uf(v) if v is not None else "—"
        delta=""
        if dd is not None and dd!=0 and not (thr and abs(dd)<thr):
            good=(dd>0)==good_up; cls="pos" if good else "neg"; sym="▲" if dd>0 else "▼"
            delta=f'<span class="{cls}" style="font-size:11px"> {sym}{_fmtc(abs(dd),unit)}</span>'
        return f'<div class="kpi"><div class="v">{val}{delta}</div><div class="l">{label}</div></div>'
    bfcmc=_num(last.get("bfc_mcap_usd")); bifimc=_num(last.get("bifi_mcap_usd"))
    kpis="".join([
        kpi("price_usd","BFC 가격 · 시총 "+(f'${bfcmc/1e6:,.1f}M' if bfcmc else '—'),lambda v:f'${v:.5f}',"$",True),
        kpi("bifi_price_usd","BIFI 곡괭이 · 시총 "+(f'${bifimc/1e6:,.2f}M' if bifimc else '—'),lambda v:f'${v:.5f}',"$",True),
        kpi("exch_total","거래소 보유(BFC)",lambda v:f'{v/1e6:,.1f}M',"",False,1_000_000),
        kpi("btcusd_supply","BtcUSD 발행",lambda v:f'{v/1e6:,.2f}M',"",True,200_000),
        kpi("coll_total_usd","BiFi 예치(달러)",lambda v:f'${v/1e6:,.2f}M',"$",True,500_000),
        kpi("bifi_borrow_dollar","BiFi 달러대출",lambda v:f'${v/1e6:,.2f}M',"$",True,100_000),
        kpi("util_pct","BiFi 이용률",lambda v:f'{v:.1f}%',"%",False),
        kpi("nakamoto33","나카모토계수",lambda v:f'{v:.0f}',"",True),
    ])
    fx=f'<span class="muted small">· 원화: BFC {_num(last.get("price_krw")) or "—"}원 / BIFI {_num(last.get("bifi_price_krw")) or "—"}원</span>'
    vd=verdict(rows)
    head="""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bifrost(BFC) 데일리 추적 리포트</title><style>
body{margin:0;background:#0f1115;color:#e6e8ee;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic",sans-serif;line-height:1.55;font-size:14px;padding:20px 26px 80px;max-width:1180px;margin:0 auto}
h1{font-size:22px;margin:.2em 0} h2{font-size:16px;margin:22px 0 8px;border-top:1px solid #2a2f3a;padding-top:12px}
.lead{color:#9aa3b2;font-size:12.5px} .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));gap:10px;margin:10px 0}
.kpi{background:#1d212b;border:1px solid #2a2f3a;border-radius:10px;padding:10px 12px} .kpi .v{font-size:17px;font-weight:800} .kpi .l{font-size:11px;color:#9aa3b2}
.verdict{border-radius:10px;padding:14px 18px;margin:10px 0 6px;font-size:17px;font-weight:800;line-height:1.4}
.verdict.v-g{background:rgba(52,211,153,.12);border:1px solid #34d399;color:#6ee7b7} .verdict.v-y{background:rgba(251,191,36,.12);border:1px solid #fbbf24;color:#fcd34d} .verdict.v-r{background:rgba(248,113,113,.14);border:1px solid #f87171;color:#fca5a5}
.narr{background:#15212b;border:1px solid #234;border-left:4px solid #4da3ff;border-radius:8px;padding:10px 14px;margin:8px 0;font-size:13.5px}
.sigboard{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:10px 0}
.chip{background:#161b22;border:1px solid #333;border-left-width:4px;border-radius:8px;padding:8px 11px} .chip .ci{font-size:11px;color:#9aa3b2} .chip .cv{font-size:15px;font-weight:800;margin-top:2px}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:12px} @media(max-width:820px){.charts{grid-template-columns:1fr}}
.ch{background:#171a21;border:1px solid #2a2f3a;border-radius:10px;padding:6px}
table{border-collapse:collapse;width:100%;font-size:12.5px;margin:8px 0} th,td{border:1px solid #2a2f3a;padding:5px 8px;text-align:left} th{background:#1d212b} td.r,th.r{text-align:right}
tr.hot td{background:rgba(251,191,36,.10)} td.wrap{white-space:normal} .small{font-size:11.5px} .muted{color:#9aa3b2}
.b-bad{color:#f87171;font-weight:700} .b-warn{color:#fbbf24;font-weight:700} .pos{color:#34d399} .neg{color:#f87171} .flat{color:#6b7280}
details summary{cursor:pointer;font-size:14px;color:#cbd5e1;margin:8px 0} .builder{background:#171a21;border:1px solid #34d399;border-radius:10px;padding:12px}
.builder label{display:inline-block;font-size:11.5px;margin:2px 8px 2px 0;color:#cbd5e1;white-space:nowrap} .builder .btn{background:#1d2531;color:#cbd5e1;border:1px solid #4da3ff;border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer;margin:6px 6px 0 0}
</style></head><body>"""
    body=f"""<h1>Bifrost (BFC) 데일리 추적 리포트</h1>
<p class="lead">자동생성 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · 누적 {len(rows)}p · 데이터품질 {last.get('data_quality','—')} {fx}
 · <a href="bifrost-bfc-report.html" style="color:#4da3ff">📄 상세 리포트</a> · <a href="data/history.csv" style="color:#4da3ff">📊 전체 CSV</a></p>
<div class="verdict v-{vd[0]}">{vd[1]}</div>
<div class="narr"><b>오늘 한 줄:</b> {narrative(rows)}</div>
<h2>🚦 상태 보드 (한눈에)</h2>{signal_board(rows)}
<p class="muted small" style="margin:2px 0 0">🟢 정상 · 🟡 관찰 · 🔴 확인필요 &nbsp;|&nbsp; <b>색 방향</b>: 거래소 순유입·Treasury 유출·이용률 급등·미청산 증가 = 🔴 주의</p>
<h2>📌 핵심 지표 <span class="muted small">(값 + 전일Δ · 초록=우호적 방향, 빨강=주의 방향)</span></h2>
<div class="grid">{kpis}</div>
<h2>📈 핵심 차트 <span class="muted small">(미션 6대 감시 + 가격)</span></h2><div class="charts">{''.join(core)}</div>
<details><summary>📊 전일/전주 대비 변화 표 (정밀 수치 — 노란 배경=유의미 변동)</summary>{change_table(rows)}</details>
<details{alopen}><summary>🔻 기타 차트 (이용률·담보구성·대출구성·JPYC·스테이킹·검증자·TVL·경보)</summary><div class="charts">{''.join(etc)}</div></details>
<h2>🔔 최근 경보 (P1/P2)</h2><table><tr><th>시각</th><th>등급</th><th>내용</th></tr>{albox}</table>
<details><summary>🛠 커스텀 차트 빌더 (심화 — 원하는 지표 골라 겹쳐 비교)</summary>
<div class="builder"><div id="picks"></div>
 <div><button class="btn" onclick="draw()">그리기</button><button class="btn" onclick="preset('cmp')">예치vs대출($)</button><button class="btn" onclick="preset('price')">BFC/BIFI 가격</button>
  <label style="border-left:1px solid #333;padding-left:10px"><input type="checkbox" id="idx"> 지수화(첫값=100, 단위 다른 지표 비교)</label></div>
 <div id="bchart" style="margin-top:8px"></div></div></details>
<p class="lead" style="margin-top:16px">전체 시계열=<code>data/history.csv</code>(엑셀) · 경보원본=<code>data/monitor-events.log</code> · Δ색: 초록=우호적 방향, 빨강=주의 방향(예: 거래소 유입·Treasury 유출·이용률 상승=빨강).</p>"""
    script="""<script>
var D=__DATA__;var CL=["#4da3ff","#fbbf24","#34d399","#f87171","#b794ff","#f0883e","#56d4dd","#e879f9"];
function fmt(v){var a=Math.abs(v);if(a>=1e8)return (v/1e6).toFixed(0)+'M';if(a>=1e6)return(v/1e6).toFixed(2)+'M';if(a>=1e3)return(v/1e3).toFixed(0)+'K';if(a<1)return v.toFixed(5);return v.toFixed(1);}
(function(){var h='';D.cat.forEach(function(c){h+='<label><input type="checkbox" name="s" value="'+c.k+'"> '+c.lab+'</label>';});document.getElementById('picks').innerHTML=h;preset('cmp');})();
function preset(p){var on=p==='cmp'?['coll_total_usd','bifi_borrow_dollar']:['price_usd','bifi_price_usd'];
 document.querySelectorAll('input[name=s]').forEach(function(e){e.checked=on.indexOf(e.value)>=0;});document.getElementById('idx').checked=(p==='price');draw();}
function draw(){
 var keys=[];document.querySelectorAll('input[name=s]:checked').forEach(function(e){keys.push(e.value);});
 var idx=document.getElementById('idx').checked;var W=1080,H=360,PL=70,PR=150,PT=24,PB=34;
 var ser=keys.map(function(k){var lab=(D.cat.find(function(c){return c.k===k})||{}).lab||k;var pts=[];D.series[k].forEach(function(v,i){if(v!==null&&v!==undefined)pts.push([i,v]);});return {k:k,lab:lab,pts:pts};}).filter(function(s){return s.pts.length;});
 if(!ser.length){document.getElementById('bchart').innerHTML='<p class="muted small">지표를 선택하세요.</p>';return;}
 if(D.dates.length<3){document.getElementById('bchart').innerHTML='<p class="muted small">데이터 '+D.dates.length+'포인트 — 추세 비교는 3회차부터. 현재값: '+ser.map(function(s){return s.lab+' '+fmt(s.pts[s.pts.length-1][1]);}).join(' · ')+'</p>';return;}
 var norm=function(s){if(!idx)return s.pts;var f=s.pts[0][1]||1;return s.pts.map(function(p){return [p[0],p[1]/f*100];});};
 var all=[];ser.forEach(function(s){norm(s).forEach(function(p){all.push(p[1]);});});
 var lo=Math.min.apply(null,all),hi=Math.max.apply(null,all);if(hi===lo){var pad=Math.abs(lo)*0.05||1;hi=lo+pad;lo=lo<0?lo-pad:Math.max(0,lo-pad);}
 var n=D.dates.length;var X=function(i){return PL+(W-PL-PR)*(n>1?i/(n-1):0.5);};var Y=function(v){return PT+(H-PT-PB)*(1-(v-lo)/(hi-lo));};
 var g='<svg viewBox="0 0 '+W+' '+H+'" width="100%" style="background:#0d1117;border:1px solid #1f2937;border-radius:8px" font-family="ui-sans-serif,system-ui">';
 for(var k2=0;k2<5;k2++){var yv=lo+(hi-lo)*k2/4,yy=Y(yv);g+='<line x1="'+PL+'" y1="'+yy+'" x2="'+(W-PR)+'" y2="'+yy+'" stroke="#1b212b"/><text x="'+(PL-6)+'" y="'+(yy+3)+'" fill="#6b7280" font-size="10" text-anchor="end">'+(idx?yv.toFixed(0):fmt(yv))+'</text>';}
 g+='<text x="'+PL+'" y="'+(H-8)+'" fill="#6b7280" font-size="10">'+D.dates[0]+'</text><text x="'+(W-PR)+'" y="'+(H-8)+'" fill="#6b7280" font-size="10" text-anchor="end">'+D.dates[n-1]+'</text>';
 ser.forEach(function(s,si){var c=CL[si%CL.length];var p=norm(s);var pts=p.length===1?[p[0],p[0]]:p;
   var d=pts.map(function(pt,i){return (i?'L':'M')+' '+X(pt[0]).toFixed(0)+' '+Y(pt[1]).toFixed(0);}).join(' ');g+='<path d="'+d+'" fill="none" stroke="'+c+'" stroke-width="2"/>';
   pts.forEach(function(pt){g+='<circle cx="'+X(pt[0]).toFixed(0)+'" cy="'+Y(pt[1]).toFixed(0)+'" r="2.5" fill="'+c+'"/>';});
   var last=s.pts[s.pts.length-1];g+='<text x="'+(W-PR+6)+'" y="'+(28+si*18)+'" fill="'+c+'" font-size="11">■ '+s.lab+' '+fmt(last[1])+'</text>';});
 g+='</svg>';if(idx)g+='<p class="muted small" style="margin:4px 0 0">지수화: 각 지표 첫값=100 기준 상대변화.</p>';document.getElementById('bchart').innerHTML=g;}
</script></body></html>"""
    open(OUT,"w").write(head+body+script.replace("__DATA__",DATA)); return OUT

if __name__=="__main__":
    print("생성:",generate() or "history.csv 없음")
