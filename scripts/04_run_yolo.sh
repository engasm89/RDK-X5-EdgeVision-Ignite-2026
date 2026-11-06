#!/usr/bin/env bash
# Run ONLY on a physical RDK X5, using D-Robotics published YOLO11m demo.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMERA_ID="${1:-0}"
if [[ ! "$CAMERA_ID" =~ ^[0-9]+$ ]]; then
  echo 'Usage: bash scripts/04_run_yolo.sh [nonnegative camera index]' >&2; exit 2
fi
if [[ ! -r /proc/device-tree/model ]]; then
  echo '[FAIL] Missing device tree board identity: cannot verify RDK X5. Run on the actual board.' >&2; exit 3
fi
BOARD_MODEL="$(tr -d '\000' < /proc/device-tree/model)"
if [[ ! "${BOARD_MODEL,,}" =~ (rdk.?x5|rdk.?x.?5|sunrise.?5|horizon.?x5) ]]; then
  echo "[FAIL] Board identity is not recognized as RDK X5: $BOARD_MODEL" >&2
  echo 'If this is an official X5 revision, verify the model string and report it before modifying this guard.' >&2
  exit 3
fi
ENTRY="$ROOT/vendor/yolo11m_demo/runtime/python/main.py"
if [[ ! -f "$ENTRY" ]]; then
  echo '[FAIL] Missing official YOLO11m sample; run bash scripts/03_setup_model.sh' >&2; exit 1
fi
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo '[FAIL] The official YOLO window requires HDMI desktop or working X11 forwarding.' >&2; exit 1
fi
printf '[RDK X5] %s\n' "$BOARD_MODEL"
printf '[CAMERA] index %s\n' "$CAMERA_ID"
cd "$(dirname "$ENTRY")"
exec python3 main.py --camera-id "$CAMERA_ID"
