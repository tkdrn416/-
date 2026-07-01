#!/usr/bin/env bash
# Bifrost(BFC) 일일 모니터 루프 — 원커맨드 실행기
#   1) 최신 데이터 pull(누적 시계열 보존)  2) monitor.py 실행(점검·경보·CSV·리포트)
#   3) 변경된 데이터/리포트 commit + push (에페메럴 컨테이너라 반드시 push 해야 시계열이 쌓임)
# 사용: bash tools/run-loop.sh
set -uo pipefail
cd "$(dirname "$0")/.."                       # repo/bifrost-bfc
ROOT="$(git rev-parse --show-toplevel)"
BRANCH="$(git branch --show-current)"
echo "== Bifrost 루프 시작 · branch=$BRANCH · $(date -u +%FT%TZ) =="

# 1) 최신 상태 반영(다른 곳에서 push된 누적분이 있으면 가져옴; 충돌나도 진행)
git -C "$ROOT" pull --rebase --autostash origin "$BRANCH" || echo "[pull 건너뜀]"

# 2) 모니터 실행(점검+경보요약+history.csv 1행+baseline+데일리 리포트 갱신)
python3 tools/monitor.py
RC=$?
if [ $RC -ne 0 ]; then echo "[monitor.py 비정상 종료 rc=$RC — 커밋 생략]"; exit $RC; fi

# 3) 데이터·리포트만 커밋(코드 변경은 손대지 않음). ROOT로 이동해 경로 모호성 제거
cd "$ROOT"
# 존재하는 파일만 add(monitor-events.log는 경보 발생 시에만 생성 → 없으면 git add가 전체 실패)
FILES="bifrost-bfc/data/history.csv bifrost-bfc/data/monitor-baseline.json bifrost-bfc/bifrost-daily-report.html"
[ -f bifrost-bfc/data/monitor-events.log ] && FILES="$FILES bifrost-bfc/data/monitor-events.log"
git add -- $FILES

if git diff --cached --quiet; then
  echo "[변경 없음 — 커밋/푸시 생략]"; exit 0
fi
git commit -q -m "loop: 일일 모니터 $(date -u +%F)"
# 네트워크 실패 시 4회 지수백오프 재시도
for delay in 2 4 8 16; do
  if git push origin "$BRANCH"; then echo "[push 완료]"; exit 0; fi
  echo "[push 실패 — ${delay}s 후 재시도]"; sleep "$delay"
done
echo "[push 최종 실패 — 다음 실행에서 재시도됨]"; exit 1
