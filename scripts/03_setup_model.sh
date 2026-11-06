#!/usr/bin/env bash
# Download official RDK X5 YOLO11m example (vendor code is NOT redistributed).
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/vendor"
URL='https://archive.d-robotics.cc/downloads/rdk_demo/rdk_x5_demo/yolo11m_demo.tar.gz'
EXPECTED="$DEST/yolo11m_demo/runtime/python/main.py"
if [[ -s "$EXPECTED" ]]; then echo "[READY] $EXPECTED"; exit 0; fi
mkdir -p "$DEST"
TEMP_DIR="$(mktemp -d "$DEST/.extract.XXXXXX")"
cleanup(){ rm -rf -- "$TEMP_DIR"; }
trap cleanup EXIT
ARCHIVE="$TEMP_DIR/yolo11m_demo.tar.gz"
echo "Downloading vendor archive from: $URL"
if command -v curl >/dev/null 2>&1; then
  curl --fail --show-error --location --retry 3 --connect-timeout 20 --output "$ARCHIVE" "$URL"
elif command -v wget >/dev/null 2>&1; then
  wget --tries=3 --timeout=30 -O "$ARCHIVE" "$URL"
else
  echo '[FAIL] Requires curl or wget.' >&2; exit 1
fi
# Validate entries, reject unsafe links/devices and unexpectedly placed files.
python3 - "$ARCHIVE" <<'PYCODE'
import sys,tarfile
from pathlib import PurePosixPath
p=sys.argv[1]
with tarfile.open(p,'r:gz') as f:
    members=f.getmembers()
    if not members: raise SystemExit('Archive is empty')
    for m in members:
        path=PurePosixPath(m.name)
        if (path.is_absolute() or '..' in path.parts or not path.parts
                or path.parts[0] != 'yolo11m_demo'
                or not (m.isfile() or m.isdir())):
            raise SystemExit('Refusing unsafe tar archive entry: '+m.name)
        if m.size > 2_000_000_000:
            raise SystemExit('Refusing oversized single archive member: '+m.name)
print('Archive entries checked:',len(members))
PYCODE
tar -xzf "$ARCHIVE" --no-same-owner --no-same-permissions -C "$TEMP_DIR"
NEW_ENTRY="$TEMP_DIR/yolo11m_demo/runtime/python/main.py"
if [[ ! -s "$NEW_ENTRY" ]]; then
  echo '[FAIL] Official demo layout changed; main.py missing.' >&2; exit 2
fi
if [[ -e "$DEST/yolo11m_demo" ]]; then
  echo '[FAIL] Partial vendor directory exists. Inspect/move it manually to avoid overwriting.' >&2; exit 2
fi
mv "$TEMP_DIR/yolo11m_demo" "$DEST/yolo11m_demo"
echo '[READY] Official demo installed. Review vendor README/dependencies before execution.'
