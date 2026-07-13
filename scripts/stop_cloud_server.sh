#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/workspace/kpl-crawler}"
PORT="${PORT:-8765}"

cd "$APP_DIR"

PIDS=""
if command -v ss >/dev/null 2>&1; then
  PIDS="$(ss -lntp 2>/dev/null | awk -v port=":$PORT" '$4 ~ port {print $NF}' | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' | sort -u)"
fi

if [ -z "$PIDS" ] && command -v pgrep >/dev/null 2>&1; then
  PIDS="$(pgrep -f "generated/scenario_api_server.py.*--port $PORT" || true)"
fi

if [ -z "$PIDS" ]; then
  echo "kpl-crawler is not running on port $PORT"
  exit 0
fi

echo "$PIDS" | while read -r PID; do
  [ -z "$PID" ] && continue
  echo "stopping kpl-crawler pid=$PID port=$PORT"
  kill "$PID" || true
done

sleep 1

REMAINING=""
if command -v ss >/dev/null 2>&1; then
  REMAINING="$(ss -lntp 2>/dev/null | awk -v port=":$PORT" '$4 ~ port {print $NF}' | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' | sort -u)"
fi

if [ -n "$REMAINING" ]; then
  echo "$REMAINING" | while read -r PID; do
    [ -z "$PID" ] && continue
    echo "force stopping pid=$PID"
    kill -9 "$PID" || true
  done
fi

echo "stopped kpl-crawler on port $PORT"
