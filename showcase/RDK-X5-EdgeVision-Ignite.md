# RDK X5 EdgeVision Ignite — USB Camera + On-Device YOLO11m

**Participant:** Ashraf Al-Madhoun / Educational Engineering Team  
**Challenge:** Robotics Dream Keeper Challenge — Winter 2026, Stage 1 (Ignite)  
**Status:** DRAFT — DO NOT SUBMIT UNTIL PHYSICAL BOARD EVIDENCE IS CAPTURED

## Overview

A reproducible RDK X5 Stage 1 demo that brings up the board, uses a UVC USB webcam as the live sensor, and executes YOLO11m object detection **on the RDK X5** using D-Robotics' official model runtime sample. A GPIO LED blink circuit is a separate optional interface exercise.

## System and components

- **Compute**: RDK X5
- **Sensor**: USB UVC webcam via USB-A HOST (V4L2)
- **AI task**: YOLO11m object detection (one on-device workload)
- **Display**: HDMI desktop or X11-forwarded GUI
- **Optional I/O**: 470Ω + red LED at GPIO physical BOARD15 and GND BOARD14
- **Network/remote**: Ethernet or Wi-Fi, SSH

## Reproducible run commands

```bash
bash scripts/01_preflight.sh
python3 scripts/02_camera_test.py --device 0 --output evidence/02_sensor_camera.png
bash scripts/03_setup_model.sh
bash scripts/04_run_yolo.sh 0
# Optional only:
sudo python3 scripts/05_led_test.py --pin 15 --seconds 10
```

## Hardware verification (fill with factual observations)

- Board image + version: [TO_FILL: REAL_BOARD_IMAGE_VERSION]
- Camera model and device ID/path: [TO_FILL: CAMERA_MODEL_AND_VIDEO_DEVICE]
- Flash and live SSH evidence: [TO_FILL: PUBLIC_EVIDENCE_LINK_01]
- Sensor/actuator proof: [TO_FILL: PUBLIC_EVIDENCE_LINK_02]
- On-board AI visualization: [TO_FILL: PUBLIC_EVIDENCE_LINK_03]
- Personal public GitHub repository: [TO_FILL: PERSONAL_PUBLIC_GITHUB_URL]
- Stage 1 Discord post permalink: [TO_FILL: DISCORD_POST_PERMALINK]

## What was learned and how to reproduce

- Official image flashing, first boot, SSH and basic Linux diagnostics.
- USB UVC camera interface and V4L2 validation.
- Real YOLO11m demo using vendor-supplied inference runtime on X5.
- Electrical safety and optional GPIO LED operation with current limiting.

## Known limitations

This is the Stage 1 baseline, not a full robotics product. The LED is a heartbeat, not model-driven alarm control. Frame rate, latency, power draw, thermal performance, and stable 24/7 operation have **not** been measured; do not assert them without actual testing. If all code works, screenshots/links must still be supplied.

## Acknowledgements

The YOLO11m example and vendor models are D-Robotics-provided; they are downloaded on the board from the official documented distribution. This showcase is a separate project wrapper, wiring plan and test suite.

Official stage guide: https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter/blob/main/stages/stage1-ignite.md
