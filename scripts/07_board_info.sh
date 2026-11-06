#!/usr/bin/env bash
# Collect NON-SENSITIVE metadata only: do not print MAC, IP, wireless config or serials.
set -Eeuo pipefail
printf '%s\n' 'RDK X5 SYSTEM INFORMATION (recorded on-device)'
printf 'UTC date: '; date -u +'%Y-%m-%d %H:%M:%S'
printf 'Architecture: '; uname -m
printf 'Kernel: '; uname -sr
printf 'Board model: '
if [[ -r /proc/device-tree/model ]]; then tr -d '\000' < /proc/device-tree/model; echo; else echo 'Unavailable'; fi
printf 'OS: '; if [[ -f /etc/os-release ]]; then grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2- | tr -d '"'; else echo 'Unknown'; fi
printf 'OpenCV: '; python3 - <<'PYC'
try:
 import cv2
 print(cv2.__version__)
except Exception as e: print('unavailable:',type(e).__name__)
PYC
printf 'Camera nodes: '; compgen -G '/dev/video*' | paste -sd ' ' - || true
printf '\nNOTE: This report alone does not prove YOLO or camera operation.\n'
