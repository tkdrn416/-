#!/usr/bin/env python3
"""data/history.csv → bifrost-daily-report.html (SVG 시계열 그래프, 외부 의존 0).
monitor.py가 매 실행 끝에 report.generate()를 호출. 단독 실행도 가능: python3 report.py
"""
import os,csv,datetime
HERE=os.path.dirname(os.path.abspath(__file__))
HIST=os.path.join(HERE,"..","data","history.csv")
LOG=os.path.join(HERE,"..","data","monitor-events.log")
OUT=os.path.join(HERE,"..","bifrost-daily-report.html")

def _num(v):
    try: return float(v)
    except: return None

def svg_chart(rows,cols,title,unit="",colors=None,h=190):
    """cols: [(csv열, 범례라벨)]. 여러 열=멀티라인."""
    colors=colors or ["#4da3ff","#fbbf24","#34d399","#f87171","#b794ff"]
    W,H=720,h; PADL,PADR,PADT,PADB=64,16,28,34
    series=[]
    for col,lab in cols:
        pts=[(r["date"],_num(r.get(col))) for r in rows if _num(r.get(col)) is not None]
        if pts: series.append((lab,pts))
    if not series:
        return f'<div class="ch"><b>{title}</b><div class="muted small">데이터 없음</div></div>'
    allv=[v for _,pts in series for _,v in pts]
    lo,hi=min(allv),max(allv)
    if hi==lo: hi=lo+1
    n=max(len(pts) for _,pts in series)
    def X(i): return PADL+(W-PADL-PADR)*(i/(n-1) if n>1 else 0.5)
    def Y(v): return PADT+(H-PADT-PADB)*(1-(v-lo)/(hi-lo))
    g=[f'<svg viewBox="0 0 {W} {H}" width="100%" style="max-width:{W}px;background:#0d1117;border:1px solid #1f2937;border-radius:8px" font-family="ui-sans-serif,system-ui">']
    g.append(f'<text x="12" y="18" fill="#e5e7eb" font-size="12" font-weight="700">{title}</text>')
    # y-gridlines
    for k in range(4):
        yv=lo+(hi-lo)*k/3; yy=Y(yv)
        g.append(f'<line x1="{PADL}" y1="{yy:.0f}" x2="{W-PADR}" y2="{yy:.0f}" stroke="#1b212b"/>')
        g.append(f'<text x="{PADL-6}" y="{yy+3:.0f}" fill="#6b7280" font-size="9" text-anchor="end">{_fmt(yv,unit)}</text>')
    # x labels (first,last)
    fd,ld=series[0][1][0][0],series[0][1][-1][0]
    g.append(f'<text x="{PADL}" y="{H-8}" fill="#6b7280" font-size="9">{fd}</text>')
    g.append(f'<text x="{W-PADR}" y="{H-8}" fill="#6b7280" font-size="9" text-anchor="end">{ld}</text>')
    for si,(lab,pts) in enumerate(series):
        c=colors[si%len(colors)]
        d=" ".join(f'{"M" if i==0 else "L"} {X(i):.0f} {Y(v):.0f}' for i,(_,v) in enumerate(pts))
        g.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2"/>')
        for i,(_,v) in enumerate(pts): g.append(f'<circle cx="{X(i):.0f}" cy="{Y(v):.0f}" r="2.5" fill="{c}"/>')
        if len(series)>1:
            g.append(f'<rect x="{PADL+si*110}" y="{H-2}" width="0" height="0"/>')
            g.append(f'<text x="{12+si*120}" y="{H-20 if False else 18}" fill="{c}" font-size="10" text-anchor="end" transform="translate({W-PADR},0)"></text>')
    if len(series)>1:
        lx=PADL
        for si,(lab,_) in enumerate(series):
            c=colors[si%len(colors)]
            g.append(f'<rect x="{lx}" y="22" width="9" height="9" rx="2" fill="{c}"/><text x="{lx+13}" y="30" fill="#cbd5e1" font-size="10">{lab}</text>')
            lx+=len(lab)*7+34
    # latest value
    lab0,pts0=series[0]
    g.append(f'<text x="{W-PADR}" y="18" fill="#9aa3b2" font-size="10" text-anchor="end">최신 {_fmt(pts0[-1][1],unit)}</text>')
    g.append('</svg>')
    return f'<div class="ch">{"".join(g)}</div>'

def _fmt(v,unit):
    a=abs(v)
    if unit=="$": return f'${v:,.4f}' if a<1 else f'${v:,.2f}'
    if unit=="원": return f'{v:,.1f}'
    if a>=1e8: return f'{v/1e6:,.0f}M'
    if a>=1e6: return f'{v/1e6:,.2f}M'
    if a>=1e3: return f'{v/1e3:,.0f}K'
    return f'{v:,.0f}'

def recent_alerts(k=25):
    if not os.path.exists(LOG): return []
    try:
        with open(LOG) as f: lines=f.read().strip().split("\n")
    except: return []
    out=[]
    for ln in lines[-k:][::-1]:
        p=ln.split("\t")
        if len(p)>=3: out.append((p[0][:16].replace("T"," "),p[1],p[2]))
    return out

def generate():
    if not os.path.exists(HIST): return
    with open(HIST) as f: rows=list(csv.DictReader(f))
    if not rows: return
    last=rows[-1]
    charts=[
        svg_chart(rows,[("price_usd","BFC/USD")],"BFC 가격 (USD)",unit="$"),
        svg_chart(rows,[("exch_total","거래소합"),("upbit_bfc","업비트"),("bithumb_bfc","빗썸")],"거래소 보유 BFC"),
        svg_chart(rows,[("jpyc_supply","JPYC")],"일본 JPYC 공급(Bifrost)"),
        svg_chart(rows,[("btcusd_supply","BtcUSD")],"BtcUSD 발행량"),
        svg_chart(rows,[("stbfc_supply","stBFC")],"Biquid 유동스테이킹(=위임 대부분)"),
        svg_chart(rows,[("val_total_stake","총스테이크")],"검증자 총 스테이크"),
        svg_chart(rows,[("bifi_bfc_pool","BFC풀"),("bifi_wstbfc","wstBFC담보"),("bifi_btcusd","BtcUSD담보")],"BiFi 예치(담보) 물량"),
        svg_chart(rows,[("treasury_bfc","Treasury")],"재단 Treasury(축적·미집행)"),
    ]
    al=recent_alerts()
    albox="".join(f'<tr><td class="small">{t}</td><td><span class="b-{ "bad" if p=="P1" else "warn"}">{p}</span></td><td class="wrap small">{m}</td></tr>' for t,p,m in al) or '<tr><td colspan="3" class="muted small">기록된 경보 없음</td></tr>'
    def L(k,d=0,uf=None):
        v=_num(last.get(k));
        return (uf(v) if uf and v is not None else (f'{v:,.0f}' if v is not None else '—'))
    html=f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bifrost(BFC) 데일리 추적 리포트</title><style>
body{{margin:0;background:#0f1115;color:#e6e8ee;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic",sans-serif;line-height:1.55;font-size:14px;padding:20px 26px 80px;max-width:1180px;margin:0 auto}}
h1{{font-size:22px;margin:.2em 0}} h2{{font-size:16px;margin:26px 0 8px;border-top:1px solid #2a2f3a;padding-top:12px}}
.lead{{color:#9aa3b2;font-size:12.5px}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:10px 0}}
.kpi{{background:#1d212b;border:1px solid #2a2f3a;border-radius:10px;padding:10px 12px}} .kpi .v{{font-size:18px;font-weight:800}} .kpi .l{{font-size:11px;color:#9aa3b2}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:12px}} @media(max-width:820px){{.charts{{grid-template-columns:1fr}}}}
.ch{{background:#171a21;border:1px solid #2a2f3a;border-radius:10px;padding:6px}}
table{{border-collapse:collapse;width:100%;font-size:12.5px;margin:8px 0}} th,td{{border:1px solid #2a2f3a;padding:5px 8px;text-align:left}} th{{background:#1d212b}}
td.wrap{{white-space:normal}} .small{{font-size:11.5px}} .muted{{color:#9aa3b2}}
.b-bad{{color:#f87171;font-weight:700}} .b-warn{{color:#fbbf24;font-weight:700}}
</style></head><body>
<h1>Bifrost (BFC) 데일리 추적 리포트</h1>
<p class="lead">자동생성 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · 누적 {len(rows)}개 데이터포인트 · 소스 data/history.csv (매 monitor.py 실행 시 갱신)</p>
<div class="grid">
 <div class="kpi"><div class="v">${L('price_usd',uf=lambda v:f'{v:.5f}')}</div><div class="l">BFC 가격 (빗썸 {L('price_krw',uf=lambda v:f'{v:,.1f}')}원)</div></div>
 <div class="kpi"><div class="v">{L('exch_total',uf=lambda v:f'{v/1e6:,.1f}M')}</div><div class="l">거래소 보유(업비트+빗썸)</div></div>
 <div class="kpi"><div class="v">{L('btcusd_supply',uf=lambda v:f'{v/1e6:,.2f}M')}</div><div class="l">BtcUSD 발행 (홀더 {L('btcusd_holders')})</div></div>
 <div class="kpi"><div class="v">{L('jpyc_supply',uf=lambda v:f'{v/1e6:,.1f}M')}</div><div class="l">일본 JPYC(Bifrost)</div></div>
 <div class="kpi"><div class="v">{L('val_count')}</div><div class="l">검증자 · Nakamoto {L('nakamoto33')} · 스테이크 {L('val_total_stake',uf=lambda v:f'{v/1e6:,.0f}M')}</div></div>
 <div class="kpi"><div class="v">{L('stbfc_supply',uf=lambda v:f'{v/1e6:,.0f}M')}</div><div class="l">Biquid 유동스테이킹</div></div>
</div>
<h2>📈 시계열 그래프</h2>
<div class="charts">{''.join(charts)}</div>
<h2>🔔 최근 경보 (P1/P2)</h2>
<table><tr><th>시각</th><th>등급</th><th>내용</th></tr>{albox}</table>
<p class="lead">전체 시계열은 <code>data/history.csv</code>(엑셀), 경보 원본은 <code>data/monitor-events.log</code>.</p>
</body></html>"""
    with open(OUT,"w") as f: f.write(html)
    return OUT

if __name__=="__main__":
    p=generate(); print("생성:",p or "history.csv 없음")
