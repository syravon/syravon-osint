#!/bin/bash

cd "$(dirname "$0")"
PIDFILE=".syravon-web.pid"

case "${1:-start}" in
  start)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "SYRAVON OSINT is already running."
      exit 0
    fi

    source .venv/bin/activate
    nohup python -m syravon_osint.web > web.log 2>&1 &
    echo $! > "$PIDFILE"
    echo "SYRAVON OSINT starting at http://127.0.0.1:5000"
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      kill "$(cat "$PIDFILE")" 2>/dev/null
      rm -f "$PIDFILE"
      echo "Stop signal sent."
    else
      echo "No PID file found."
    fi
    ;;
  status)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "SYRAVON OSINT is running."
    else
      echo "SYRAVON OSINT is not running."
    fi
    ;;
  *)
    echo "Usage: ./run-web.sh {start|stop|status}"
    exit 1
    ;;
esac
