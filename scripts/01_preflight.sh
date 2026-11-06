#!/usr/bin/env bash
set -Eeuo pipefail
printf '\n=== RDK X5 Stage 1 Preflight (diagnostic only) ===\n'
printf 'Date (UTC): '; date -u +'%Y-%m-%dT%H:%M:%SZ'
printf 'Machine architecture: '; uname -m
printf 'Kernel: '; uname -sr
printf 'Board model: '
if [[ -r /proc/device-tree/model ]]; then tr -d '\000' < /proc/device-tree/model; printf '\n'; else echo 'unknown (not a conclusive failure)'; fi
printf 'Python: '; python3 --version
printf 'DISPLAY: %s\n' "${DISPLAY:-not set (GUI demo will need a desktop or X11)}"
printf '\nVideo devices:\n'
found=0
for d in /dev/video*; do
  if [[ -e "$d" ]]; then printf '  %s\n' "$d"; found=1; fi
done
if [[ "$found" == 0 ]]; then echo '  none (plug UVC webcam into USB-A and check udev)'; fi
if command -v v4l2-ctl >/dev/null; then
  printf '\nV4L2 devices (may include non-camera devices):\n'
  v4l2-ctl --list-devices || true
else
  echo 'v4l2-ctl absent (optional: install v4l-utils if supported)'
fi
printf '\nPython imports:\n'
python3 - <<'PYCODE'
for name in ('cv2','Hobot.GPIO'):
    try:
        __import__(name)
        print('  OK ', name)
    except Exception as exc:
        print('  NOT READY', name, type(exc).__name__, str(exc)[:160])
PYCODE
printf '\nNetwork interface summary (keep private if sensitive):\n'
if command -v ip >/dev/null; then ip -brief link || true; fi
printf '\nOfficial demo directory: '
if [[ -f /app/pydev_demo/07_usb_camera_sample/usb_camera_yolov5x.py ]]; then echo 'legacy YOLOv5 demo present'; else echo 'optional legacy demo not found'; fi
printf '\nNote: a passing diagnostic is not physical camera/AI success.\n'
