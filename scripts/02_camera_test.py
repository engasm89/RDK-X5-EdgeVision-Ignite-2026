#!/usr/bin/env python3
"""Capture one REAL UVC frame on the RDK X5; never synthesizes evidence."""
import argparse
from pathlib import Path
import sys
import time


def capture(device: int, output: Path, attempts: int = 40) -> tuple[int, int]:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError('cv2 unavailable; install board-supported OpenCV, not a random vendor runtime') from exc
    backend = getattr(cv2, 'CAP_V4L2', 0)
    cam = cv2.VideoCapture(device, backend)
    if not cam.isOpened():
        cam.release()
        raise RuntimeError(f'Cannot open camera index {device}; inspect v4l2-ctl --list-devices')
    try:
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for attempt in range(attempts):
            ok, frame = cam.read()
            if ok and frame is not None and getattr(frame, 'size', 0) > 0:
                output.parent.mkdir(parents=True, exist_ok=True)
                if not cv2.imwrite(str(output), frame):
                    raise RuntimeError('Failed to write actual camera frame')
                height, width = frame.shape[:2]
                return width, height
            time.sleep(0.10)
        raise RuntimeError(f'No valid frames after {attempts} attempts')
    finally:
        cam.release()


def main() -> int:
    parser = argparse.ArgumentParser(description='RDK X5 UVC camera sensor smoke test')
    parser.add_argument('--device', type=int, default=0, help='V4L2 /dev/videoN index')
    parser.add_argument('--output', type=Path, default=Path('evidence/02_sensor_camera.png'))
    args = parser.parse_args()
    if args.device < 0:
        parser.error('--device must be >= 0')
    try:
        width, height = capture(args.device, args.output)
    except Exception as exc:
        print(f'[FAIL] UVC camera: {exc}', file=sys.stderr)
        return 1
    print(f'[PASS] Real camera frame {width}x{height} saved to {args.output}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
