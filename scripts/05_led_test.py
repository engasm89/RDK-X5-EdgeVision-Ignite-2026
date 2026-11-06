#!/usr/bin/env python3
"""Optional BOARD GPIO LED blink; independent of object-detection results."""
import argparse
import sys
import time


def blink(pin: int, seconds: float, period: float) -> None:
    try:
        import Hobot.GPIO as gpio
    except ImportError as exc:
        raise RuntimeError('Hobot.GPIO not available (run on compatible RDK X5 system)') from exc
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    try:
        gpio.setup(pin, gpio.OUT, initial=gpio.LOW)
        stop = time.monotonic() + seconds
        while time.monotonic() < stop:
            gpio.output(pin, gpio.HIGH)
            time.sleep(period / 2)
            gpio.output(pin, gpio.LOW)
            time.sleep(period / 2)
    finally:
        try:
            gpio.output(pin, gpio.LOW)
        finally:
            gpio.cleanup()


def main() -> int:
    ap = argparse.ArgumentParser(description='Optional RDK X5 GPIO LED blink test')
    ap.add_argument('--pin', type=int, default=15, help='Physical 40-pin header number in BOARD mode')
    ap.add_argument('--seconds', type=float, default=10.0)
    ap.add_argument('--period', type=float, default=1.0)
    args = ap.parse_args()
    if args.pin != 15:
        ap.error('This documented wiring uses BOARD pin 15 only; revise and verify schematic before other pins')
    if not 0 < args.seconds <= 600 or not 0.1 <= args.period <= 20:
        ap.error('Require seconds in (0,600] and period in [0.1,20]')
    print('GPIO15 heartbeat only: NO inference-driven LED behavior is implemented')
    print('Confirm physical pin numbers, 3.3V domain, 470Ω series resistor, and power-off wiring')
    try:
        blink(args.pin, args.seconds, args.period)
    except Exception as exc:
        print(f'[FAIL] LED test: {exc}', file=sys.stderr)
        return 1
    print('[PASS] GPIO commands completed; physically observe LED before claiming success')
    return 0


if __name__ == '__main__':
    sys.exit(main())
