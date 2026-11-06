#!/usr/bin/env python3
"""Conservative Stage 1 evidence audit. Never substitutes for real board verification."""
import json
from pathlib import Path
import re
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
    'flash and SSH':ROOT/'evidence/01_flash_ssh.png',
    'USB camera sensor':ROOT/'evidence/02_sensor_camera.png',
    'YOLO on physical RDK X5':ROOT/'evidence/03_yolo_on_rdk_x5.png',
}
LINKS=ROOT/'submission/stage1_links.json'


def png_dimensions(path):
    with path.open('rb') as f:
        header=f.read(24)
    if len(header)!=24 or header[:8]!=b'\x89PNG\r\n\x1a\n' or header[12:16]!=b'IHDR':
        raise ValueError('not a valid PNG signature/IHDR')
    width,height=struct.unpack('>II',header[16:24])
    if not 320<=width<=20000 or not 240<=height<=20000:
        raise ValueError('unreasonable PNG dimensions')
    return width,height


def examine(root=ROOT, links_path=LINKS):
    failures=[]
    for label,path in REQUIRED.items():
        try:
            if not path.exists() or path.stat().st_size < 2048:
                raise ValueError('missing or too small')
            width,height=png_dimensions(path)
            print(f'[FILE] {label}: {width} x {height} PNG, {path.stat().st_size} bytes')
        except (ValueError, OSError) as e:
            print(f'[MISSING] {label}: {e}')
            failures.append(label)
    try:
        links=json.loads(links_path.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:
        print(f'[MISSING] links metadata: {e}')
        failures.append('links metadata')
        links={}
    expected=['personal_github_repo','discord_stage1_permalink','official_showcase_pr']
    for key in expected:
        val=links.get(key,'')
        if not isinstance(val,str) or not re.match(r'^https://[^ ]{8,}$',val):
            print(f'[MISSING] Verified public link: {key}')
            failures.append(key)
        else:
            print(f'[LINK] {key}: {val} (reachability NOT checked)')
    for key in ('board_model','os_image_version','camera_model'):
        val=links.get(key,'')
        if not isinstance(val,str) or not val.strip() or 'TO_FILL' in val:
            print(f'[MISSING] Actual hardware metadata: {key}')
            failures.append(key)
    return failures


def main():
    failures=examine()
    print('\nNOTE: This script does not verify screenshot authenticity, physical run, public visibility, registration or official judging.')
    if failures:
        print(f'NOT READY FOR SUBMISSION: {len(failures)} requirement(s) still unresolved.')
        return 1
    print('LOCAL FILE/LINK FORMAT CHECK PASSED — manual board and official acceptance checks still required.')
    return 0

if __name__=='__main__':
    sys.exit(main())
