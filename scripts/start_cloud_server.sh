#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/workspace/kpl-crawler}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-80}"
PUBLIC_IP="${PUBLIC_IP:-124.222.192.83}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$APP_DIR"

if [ ! -d "venv" ]; then
  echo "venv not found, creating: $APP_DIR/venv"
  "$PYTHON_BIN" -m venv venv
fi

# shellcheck disable=SC1091
source venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if command -v ss >/dev/null 2>&1; then
  EXISTING_PID="$(ss -lntp 2>/dev/null | awk -v port=":$PORT" '$4 ~ port {print $NF}' | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' | head -n 1)"
  if [ -n "${EXISTING_PID:-}" ]; then
    echo "stopping existing process on port $PORT: $EXISTING_PID"
    kill "$EXISTING_PID" || true
    sleep 1
  fi
fi

mkdir -p logs
nohup python generated/scenario_api_server.py --host "$HOST" --port "$PORT" > logs/server.out.log 2> logs/server.err.log &
PID="$!"

echo "started kpl-crawler"
echo "pid: $PID"
echo "local: http://127.0.0.1:$PORT"
echo "public: http://$PUBLIC_IP:$PORT"
echo "stdout: $APP_DIR/logs/server.out.log"
echo "stderr: $APP_DIR/logs/server.err.log"
