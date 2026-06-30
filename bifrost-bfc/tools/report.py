#!/usr/bin/env python3
"""data/history.csv → bifrost-daily-report.html (SVG 시계열 + 전일/전주 Δ표 + 자동 내러티브).
외부 의존 0. monitor.py가 매 실행 끝에 report.generate() 호출. 단독: python3 report.py
"""
import os,csv,datetime
HERE=os.path.dirname(os.path.abspath(__file__))
HIST=os.path.join(HERE,"..","data","history.csv")
LOG=os.path.join(HERE,"..","data","monitor-events.log")
OUT=os.path.join(HERE,"..","bifrost-daily-report.html")

def _num(v):
    try: return float(v)
    except: return None

def _fmt(v,unit=""):
    if v is None: return "—"
    a=abs(v)
    if unit=="$": return f'${v:,.5f}' if a<1 else f'${v:,.2f}'
    if unit=="원": return f'{v:,.1f}원'
    if unit=="%": return f'{v:,.1f}%'
    if a>=1e8: return f'{v/1e6:,.0f}M'
    if a>=1e6: return f'{v/1e6:,.2f}M'
    if a>=1e3: return f'{v/1e3:,.0f}K'
    return f'{v:,.0f}'

def svg_chart(rows,cols,title,unit="",colors=None,h=190):
    colors=colors or ["#4da3ff","#fbbf24","#34d399","#f87171","#b794ff"]
    W,H=720,h; PADL,PADR,PADT,PADB=66,16,30,32
    series=[]
    for col,lab in cols:
        pts=[(r["date"],_num(r.get(col))) for r in rows if _num(r.get(col)) is not None]
        if pts: series.append((lab,pts))
    if not series:
        return f'<div class="ch"><svg viewBox="0 0 {W} 70" width="100%" style="max-width:{W}px"><text x="12" y="22" fill="#e5e7eb" font-size="12" font-weight="700">{title}</text><text x="12" y="46" fill="#6b7280" font-size="11">데이터 누적 대기</text></svg></div>'
    allv=[v for _,pts in series for _,v in pts]; lo,hi=min(allv),max(allv)
    if hi==lo: hi=lo*1.001+1; lo=lo*0.999-1  # 평탄 시 약간의 폭
    drawn=[(lab,(pts*2 if len(pts)==1 else pts)) for lab,pts in series]  # N=1이면 평탄선
    n=max(len(pts) for _,pts in drawn)
    def X(i): return PADL+(W-PADL-PADR)*(i/(n-1) if n>1 else 0.5)
    def Y(v): return PADT+(H-PADT-PADB)*(1-(v-lo)/(hi-lo))
    g=[f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px;background:#0d1117;border:1px solid #1f2937;border-radius:8px" font-family="ui-sans-serif,system-ui">']
    g.append(f'<text x="12" y="18" fill="#e5e7eb" font-size="12" font-weight="700">{title}</text>')
    for k in range(4):
        yv=lo+(hi-lo)*k/3; yy=Y(yv)
        g.append(f'<line x1="{PADL}" y1="{yy:.0f}" x2="{W-PADR}" y2="{yy:.0f}" stroke="#1b212b"/>')
        g.append(f'<text x="{PADL-6}" y="{yy+3:.0f}" fill="#6b7280" font-size="9" text-anchor="end">{_fmt(yv,unit)}</text>')
    fd,ld=drawn[0][1][0][0],drawn[0][1][-1][0]
    g.append(f'<text x="{PADL}" y="{H-6}" fill="#6b7280" font-size="9">{fd}</text>')
    g.append(f'<text x="{W-PADR}" y="{H-6}" fill="#6b7280" font-size="9" text-anchor="end">{ld}{" (단일점)" if n==2 and fd==ld else ""}</text>')
    for si,(lab,pts) in enumerate(drawn):
        c=colors[si%len(colors)]
        d=" ".join(f'{"M" if i==0 else "L"} {X(i):.0f} {Y(v):.0f}' for i,(_,v) in enumerate(pts))
        g.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2"/>')
        for i,(_,v) in enumerate(pts): g.append(f'<circle cx="{X(i):.0f}" cy="{Y(v):.0f}" r="2.5" fill="{c}"/>')
    if len(series)>1:
        lx=PADL
        for si,(lab,_) in enumerate(series):
            c=colors[si%len(colors)]
            g.append(f'<rect x="{lx}" y="23" width="9" height="9" rx="2" fill="{c}"/><text x="{lx+12}" y="31" fill="#cbd5e1" font-size="10">{lab}</text>')
            lx+=len(lab)*8+34
    g.append(f'<text x="{W-PADR}" y="18" fill="#9aa3b2" font-size="10" text-anchor="end">최신 {_fmt(series[0][1][-1][1],unit)}</text>')
    g.append('</svg>')
    return f'<div class="ch">{"".join(g)}</div>'

def arrow(d):
    if d is None or d==0: return '<span class="flat">→ 0</span>'
    return f'<span class="up">▲ +{_fmt(d)}</span>' if d>0 else f'<span class="dn">▼ {_fmt(d)}</span>'

def change_table(rows):
    cur=rows[-1]; prev=rows[-2] if len(rows)>1 else None; wk=rows[-8] if len(rows)>=8 else None
    metrics=[("price_usd","BFC 가격","$"),("exch_total","거래소 보유",""),("exch_net_flow","거래소 순흐름",""),
     ("treasury_bfc","Treasury",""),("btcusd_supply","BtcUSD 발행",""),("btcusd_vault_share","BtcUSD 볼트점유","%"),
     ("jpyc_supply","JPYC",""),("stbfc_supply","유동스테이킹",""),("val_total_stake","검증자 스테이크",""),
     ("nakamoto33","Nakamoto",""),("val_top5_pct","상위5 집중","%"),("staking_ratio_pct","스테이킹비율","%"),
     ("bifi_bfc_pool","BiFi BFC풀",""),("defi_tvl_usd","TVL","$")]
    out=['<table><tr><th>지표</th><th class="r">현재</th><th class="r">전일Δ</th><th class="r">전주Δ</th></tr>']
    for col,lab,u in metrics:
        c=_num(cur.get(col))
        if c is None: continue
        dp=(c-_num(prev.get(col))) if prev and _num(prev.get(col)) is not None else None
        dw=(c-_num(wk.get(col))) if wk and _num(wk.get(col)) is not None else None
        out.append(f'<tr><td>{lab}</td><td class="r">{_fmt(c,u)}</td><td class="r">{arrow(dp)}</td><td class="r">{arrow(dw)}</td></tr>')
    out.append('</table>')
    return "".join(out)

def narrative(rows):
    if len(rows)<2: return "데이터 1포인트 — 내러티브는 2회차부터(전일 대비 변화 자동요약)."
    cur,prev=rows[-1],rows[-2]; bits=[]
    def d(col):
        a,b=_num(cur.get(col)),_num(prev.get(col)); return (a-b) if a is not None and b is not None else None
    pf=d("price_usd")
    if pf is not None and _num(prev.get("price_usd")): bits.append(f"가격 {pf/_num(prev['price_usd'])*100:+.1f}%")
    for col,lab,thr in [("exch_total","거래소",1_000_000),("treasury_bfc","Treasury",1),("btcusd_supply","BtcUSD",200_000),
                        ("jpyc_supply","JPYC",200_000),("val_total_stake","검증자스테이크",1_000_000),("stbfc_supply","유동스테이킹",1_000_000)]:
        x=d(col)
        if x is not None and abs(x)>=thr: bits.append(f"{lab} {_fmt(x)}")
    nk=d("nakamoto33")
    if nk: bits.append(f"Nakamoto {_num(prev.get('nakamoto33')):.0f}→{_num(cur.get('nakamoto33')):.0f}")
    a1=_num(cur.get("alert_p1")) or 0
    head=f"⚠️ P1 경보 {a1:.0f}건" if a1 else "✅ P1 경보 없음"
    return head+(" · "+", ".join(bits) if bits else " · 주요지표 변동 미미")

def recent_alerts(k=25):
    if not os.path.exists(LOG): return []
    try: lines=open(LOG).read().strip().split("\n")
    except: return []
    out=[]
    for ln in lines[-k:][::-1]:
        p=ln.split("\t")
        if len(p)>=3: out.append((p[0][:16].replace("T"," "),p[1],p[2]))
    return out

def generate():
    if not os.path.exists(HIST): return
    rows=[r for r in csv.DictReader(open(HIST)) if r.get("date")]
    if not rows: return
    last=rows[-1]
    charts=[
        svg_chart(rows,[("price_usd","BFC/USD")],"BFC 가격 (USD)","$"),
        svg_chart(rows,[("exch_total","거래소합"),("upbit_bfc","업비트"),("bithumb_bfc","빗썸")],"거래소 보유 BFC"),
        svg_chart(rows,[("btcusd_supply","BtcUSD")],"BtcUSD 발행량"),
        svg_chart(rows,[("btcusd_vault_share","볼트점유%")],"BtcUSD 브릿지볼트 점유율","%"),
        svg_chart(rows,[("jpyc_supply","JPYC")],"일본 JPYC 공급(Bifrost)"),
        svg_chart(rows,[("stbfc_supply","stBFC")],"Biquid 유동스테이킹(=위임 대부분)"),
        svg_chart(rows,[("val_total_stake","총스테이크")],"검증자 총 스테이크"),
        svg_chart(rows,[("val_top5_pct","상위5%"),("val_top10_pct","상위10%")],"검증자 집중도(탈중앙성 추세)","%"),
        svg_chart(rows,[("bifi_bfc_pool","BFC풀"),("bifi_wstbfc","wstBFC담보"),("bifi_btcusd","BtcUSD담보")],"BiFi 예치(담보) 물량"),
        svg_chart(rows,[("defi_tvl_usd","TVL")],"DefiLlama 체인 TVL","$"),
        svg_chart(rows,[("treasury_bfc","Treasury")],"재단 Treasury(축적·미집행)"),
        svg_chart(rows,[("alert_p1","P1"),("alert_p2","P2")],"일별 경보 건수"),
    ]
    al=recent_alerts()
    albox="".join(f'<tr><td class="small">{t}</td><td><span class="b-{ "bad" if p=="P1" else "warn"}">{p}</span></td><td class="wrap small">{m}</td></tr>' for t,p,m in al) or '<tr><td colspan="3" class="muted small">기록된 경보 없음</td></tr>'
    def L(k,uf=None):
        v=_num(last.get(k)); return (uf(v) if uf and v is not None else (f'{v:,.0f}' if v is not None else '—'))
    html=f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bifrost(BFC) 데일리 추적 리포트</title><style>
body{{margin:0;background:#0f1115;color:#e6e8ee;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic",sans-serif;line-height:1.55;font-size:14px;padding:20px 26px 80px;max-width:1180px;margin:0 auto}}
h1{{font-size:22px;margin:.2em 0}} h2{{font-size:16px;margin:24px 0 8px;border-top:1px solid #2a2f3a;padding-top:12px}}
.lead{{color:#9aa3b2;font-size:12.5px}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:10px;margin:10px 0}}
.kpi{{background:#1d212b;border:1px solid #2a2f3a;border-radius:10px;padding:10px 12px}} .kpi .v{{font-size:17px;font-weight:800}} .kpi .l{{font-size:11px;color:#9aa3b2}}
.narr{{background:#15212b;border:1px solid #234;border-left:4px solid #4da3ff;border-radius:8px;padding:10px 14px;margin:8px 0;font-size:13px}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:12px}} @media(max-width:820px){{.charts{{grid-template-columns:1fr}}}}
.ch{{background:#171a21;border:1px solid #2a2f3a;border-radius:10px;padding:6px}}
table{{border-collapse:collapse;width:100%;font-size:12.5px;margin:8px 0}} th,td{{border:1px solid #2a2f3a;padding:5px 8px;text-align:left}} th{{background:#1d212b}} td.r,th.r{{text-align:right}}
td.wrap{{white-space:normal}} .small{{font-size:11.5px}} .muted{{color:#9aa3b2}}
.b-bad{{color:#f87171;font-weight:700}} .b-warn{{color:#fbbf24;font-weight:700}}
.up{{color:#f87171}} .dn{{color:#34d399}} .flat{{color:#6b7280}}
</style></head><body>
<h1>Bifrost (BFC) 데일리 추적 리포트</h1>
<p class="lead">자동생성 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · 누적 {len(rows)}개 데이터포인트 · 데이터품질 {last.get('data_quality','—')} · 소스 data/history.csv</p>
<div class="narr"><b>오늘 한 줄:</b> {narrative(rows)}</div>
<div class="grid">
 <div class="kpi"><div class="v">${L('price_usd',lambda v:f'{v:.5f}')}</div><div class="l">BFC 가격 (빗썸 {L('price_krw',lambda v:f'{v:,.1f}')}원)</div></div>
 <div class="kpi"><div class="v">{L('exch_total',lambda v:f'{v/1e6:,.1f}M')}</div><div class="l">거래소 보유(업비트+빗썸)</div></div>
 <div class="kpi"><div class="v">{L('btcusd_supply',lambda v:f'{v/1e6:,.2f}M')}</div><div class="l">BtcUSD (홀더 {L('btcusd_holders')} · 볼트 {L('btcusd_vault_share',lambda v:f'{v:.0f}')}%)</div></div>
 <div class="kpi"><div class="v">{L('jpyc_supply',lambda v:f'{v/1e6:,.1f}M')}</div><div class="l">일본 JPYC(Bifrost)</div></div>
 <div class="kpi"><div class="v">{L('val_count')}·N{L('nakamoto33')}</div><div class="l">검증자 · 상위5 {L('val_top5_pct',lambda v:f'{v:.0f}')}% · 스테이킹 {L('staking_ratio_pct',lambda v:f'{v:.0f}')}%</div></div>
 <div class="kpi"><div class="v">${L('defi_tvl_usd',lambda v:f'{v/1e6:,.1f}M')}</div><div class="l">DefiLlama TVL</div></div>
</div>
<h2>📊 전일/전주 대비 변화</h2>
{change_table(rows)}
<h2>📈 시계열 그래프</h2>
<div class="charts">{''.join(charts)}</div>
<h2>🔔 최근 경보 (P1/P2)</h2>
<table><tr><th>시각</th><th>등급</th><th>내용</th></tr>{albox}</table>
<p class="lead">전체 시계열=<code>data/history.csv</code>(엑셀) · 경보원본=<code>data/monitor-events.log</code> · ▲=증가 ▼=감소(녹색=유출/감소가 호재인 거래소 기준 색반전).</p>
</body></html>"""
    open(OUT,"w").write(html); return OUT

if __name__=="__main__":
    print("생성:",generate() or "history.csv 없음")
