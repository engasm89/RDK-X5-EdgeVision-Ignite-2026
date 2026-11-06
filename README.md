# RDK X5 EdgeVision Ignite — Stage 1 | Winter 2026

> **Status: code and wiring prepared; untested on physical RDK X5; challenge evidence NOT yet captured.**
> This project uses D-Robotics' official *YOLO11m* on-device example, plus original bring-up, USB camera, optional GPIO LED, and submission utilities. No benchmark or board run is claimed.

## Objective

Meet the RDK Challenge Winter **Stage 1 — Ignite** requirements with an RDK X5 and a USB UVC camera:
1. Boot an official image, network and SSH.
2. Demonstrate the USB camera as one sensor.
3. Run **one on-board AI task**: YOLO11m object detection.
4. Collect real screenshots, publish a personal repository, post a Discord permalink, and submit one showcase PR into `projects/` of the official challenge repo.

**Stage 1 target deadline:** November 10, 2026 (Stage 2 opens November 11). The program repo describes flexible milestones, but use the email's Nov 10 instruction.

## Hardware — essential vs optional

| Part | Required? | Connection |
| --- | --- | --- |
| D-Robotics RDK X5 | Yes | Host board |
| Officially recommended USB-C 5V/5A power supply | Yes | Dedicated POWER USB-C port, **not computer USB** |
| microSD with supported RDK X5 image | Usually | Flash with RDK Studio / official method |
| UVC-compatible USB camera | Yes for this pathway | USB-A host port on RDK X5 |
| Network (Ethernet recommended) | Yes | Ethernet to router, or Wi-Fi |
| HDMI display/keyboard/mouse **or X11 forwarding** | Required for GUI demo | HDMI screen or X11-enabled remote session |
| Red LED + 470 Ω resistor + jumper wires | Optional | BOARD GPIO15 -> resistor -> LED anode, LED cathode -> BOARD GND14 |

**Safety:** GPIO15 is a 3.3V-level GPIO on supported RDK X5 configurations; verify board revision/IO voltage before wiring. Power **off** to connect jumpers; never place LED directly across a GPIO without a resistor. LED is only a heartbeat/IO demonstration, **not a YOLO alert output**.

## Quick start (run these on the real RDK X5, not on your laptop)

### Step A — Flash + SSH

1. Install [RDK Studio](https://developer.d-robotics.cc/en/rdkstudio) or use the documented official flash process for a supported **RDK X5** image.
2. Power from 5V/5A supply and connect network. Verify actual IP on the board with `hostname -I` (or use serial-console/network settings).
3. From computer: `ssh <YOUR_USER>@<BOARD_IP>` — use the credentials provided by the chosen image. **Do not assume an IP or username.**
4. Capture real evidence: screenshot of successful flashing and active SSH terminal. Save privately as `evidence/01_flash_ssh.png`.

### Step B — On board: validate and capture camera sensor

Transfer this directory to board (`scp -r` or `git clone` after pushing your own repo), then:

```bash
cd RDK-X5-EdgeVision-Ignite-2026
bash scripts/01_preflight.sh
python3 scripts/02_camera_test.py --device 0 --output evidence/02_sensor_camera.png
```

A valid live frame saves actual sensor evidence. If `cv2` is unavailable, install the **board-image-compatible** OpenCV package via the official board guidance. Do not indiscriminately upgrade the D-Robotics Python runtime with `pip install -U`.

### Step C — On board: fetch and run the *official* YOLO11m demo

```bash
bash scripts/03_setup_model.sh
# Launch from the board's graphical desktop terminal or X11-forwarded SSH:
bash scripts/04_run_yolo.sh 0
```

This invokes `vendor/yolo11m_demo/runtime/python/main.py --camera-id 0` on the **RDK X5**, following the [official case](https://developer.d-robotics.cc/x5_cases_doc/en/basic/detect). It uses the accelerator/runtime provided in the official demo; *the sample model and its dependencies are downloaded separately*, not bundled in this repository. Use your desktop screenshot tool to record the live detection window and an RDK X5 terminal together: `evidence/03_yolo_on_rdk_x5.png`. Do not substitute a PC YOLO run or a mockup.

If camera index is not 0, inspect `v4l2-ctl --list-devices` or `ls -l /dev/video*`, retest `--device N`, and run `04_run_yolo.sh N`.

**GUI is required:** plain SSH without X11 / an HDMI desktop normally cannot display the YOLO demo window. Mac users can configure XQuartz; Windows users can use an X11-capable SSH client or run on HDMI. `echo $DISPLAY` should show a display identifier in that session.

### Step D — Optional circuit: LED test (separate terminal)

1. **Power off**, connect GPIO BOARD15 -> 470Ω -> LED long lead (anode), LED short lead (cathode) -> GND BOARD14.
2. Verify pin numbering and IO voltage; boot the board.
3. Run: `sudo python3 scripts/05_led_test.py --pin 15 --seconds 10`
4. Film genuine LED blinking if desired. A camera by itself is enough for the one-sensor requirement.

### Step E — Submission

Read [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md), edit the draft showcase [showcase/RDK-X5-EdgeVision-Ignite.md](showcase/RDK-X5-EdgeVision-Ignite.md), and run:

```bash
python3 scripts/06_verify_submission.py
```

That check is a *local checklist*; it cannot confirm Discord, GitHub permission, image validity, or official acceptance. Only post real evidence after board testing.

## Diagrams

- [Full hookup diagram (PNG)](hardware/rdk_x5_wiring.png)
- [Vector hookup diagram (SVG)](hardware/rdk_x5_wiring.svg)
- [Optional LED electrical schematic (PNG)](hardware/optional_led_schematic.png)
- [Optional LED schematic (SVG)](hardware/optional_led_schematic.svg)

## System architecture

`USB UVC Camera -> USB-A host -> RDK X5 (video frames) -> official YOLO11m demo / BPU runtime -> object detection window -> actual evidence screenshot`

The optional `BOARD15 -> resistor -> LED -> GND` circuit is an independent GPIO test, not a model confidence or detection indicator.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No SSH | Confirm image boot, board IP, network route, SSH service, and credentials supplied by image |
| RDK X5 repeatedly restarts | Use correct **5V/5A** supply at the dedicated POWER port |
| `python3: No module named cv2` | Use image-supported OpenCV package; check `python3 -c 'import cv2'` |
| No camera frame | UVC compatibility, USB-A host port, `v4l2-ctl --list-devices`, permissions, competing applications, and device index |
| No AI window / `DISPLAY` empty | Use board Ubuntu desktop or X11-forwarded SSH; check GUI before running |
| YOLO example not present | Run `03_setup_model.sh` on board with Internet and verify official archive URL remains available |
| Runtime/model version warning | Prefer matching vendor firmware/demo versions; refer to official docs, do not claim inference is correct when incompatible |
| LED does not light | LED polarity, **470Ω**, BOARD pin mapping, 3.3V domain, pinmux (`sudo srpi-config`), then `Hobot.GPIO` access |

## Sources & attribution

- [Official Winter Stage 1 rules](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter/blob/main/stages/stage1-ignite.md)
- [Official RDK X5 YOLO11m USB camera case](https://developer.d-robotics.cc/x5_cases_doc/en/basic/detect)
- [Official board interfaces, power, USB](https://developer.d-robotics.cc/rdk_doc/en/Quick_start/hardware_introduction/rdk_x5/)
- [Hobot.GPIO usage and BOARD 15 LED example](https://d-robotics.github.io/rdk_doc/en/Basic_Application/01_40pin_user_sample/gpio/)
- [GPIO electrical precautions & pinmux](https://developer.d-robotics.cc/rdk_doc/en/Basic_Application/01_40pin_user_sample/40pin_define/)
- [Official Winter challenge repository](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter)

**License:** MIT for original scripts, diagrams, and documentation in this package. The third-party YOLO11m demo, model, and downloaded assets are NOT redistributed and retain their respective original licenses. Check third-party licensing before public redistribution.

## Video and final evidence QA (2026-11-06 update)

**Winter Stage 1 does not require a video**; keep the three genuine screenshots plus GitHub, Discord and showcase PR. **Winter Stage 3 requires** a 3–7 minute public video, preferably 1080p, including 30 continuous seconds of AI. See [Arabic shot list](docs/VIDEO_REQUIREMENTS_AND_SHOTLIST_AR.md) and [English guide](docs/VIDEO_REQUIREMENTS_EN.md).

After real board run: `bash scripts/07_board_info.sh`, fill [actual URLs and board metadata](submission/stage1_links.json), and `python3 scripts/08_verify_submission.py`. Even a passing local check is not official acceptance.

**Note on board identification**: the YOLO runner now refuses to run on generic non-RDK machines. Confirm `/proc/device-tree/model` before use; if an official revised board identifies itself differently, verify the actual identity before editing the guarded regex.

[Quality review/release notes](docs/RELEASE_NOTES_V2.md).

## Public visual references vs. evidence

The included [`assets/CONCEPT_ONLY_NOT_EVIDENCE.png`](assets/CONCEPT_ONLY_NOT_EVIDENCE.png) is an **AI-generated concept visualization**, not a photo of a verified physical build. Do not use it as a wiring specification or contest proof. See [`docs/REFERENCE_IMAGE_AUDIT.md`](docs/REFERENCE_IMAGE_AUDIT.md) for official product links and the unresolved hardware-identification checks. A GitHub publication guide and honest Discord progress/completion drafts are under `docs/` and `submission/`.
