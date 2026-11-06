# Winter 2026 Stage 1 — actual submission checklist

## 0. Registration

- [ ] Join https://discord.gg/ydVxBpz3vP
- [ ] Submit https://forms.gle/ojG5pRmWXMsM27Vb9 if not already completed
- [ ] Activate https://developer.d-robotics.cc/en/rdkstudio
- [ ] Post self-introduction in challenge channel, create/identify **personal thread**

## 1. Board bring-up

- [ ] Flash a supported RDK X5 image (capture GUI or flashing completion evidence)
- [ ] Connect to a network and demonstrate shell on board via SSH
- [ ] Save actual screenshot at `evidence/01_flash_ssh.png`
- [ ] Create personal Discord Stage 1 check-in

## 2. Sensor (USB UVC camera)

- [ ] Plug camera in USB-A host port
- [ ] On-board run: `python3 scripts/02_camera_test.py --device 0 --output evidence/02_sensor_camera.png`
- [ ] Check that output image is a **real live frame**
- [ ] State interface: USB UVC / V4L2

## 3. Exactly one visible AI workload — YOLO11m

- [ ] On-board install official demo: `bash scripts/03_setup_model.sh`
- [ ] On board GUI/X11 run: `bash scripts/04_run_yolo.sh 0`
- [ ] Show person/object with boxes/class name in actual live demo
- [ ] Capture real screenshot with YOLO output and RDK terminal `evidence/03_yolo_on_rdk_x5.png`
- [ ] Record actual RDK X5 model and image version; no invented FPS/metrics

## 4. Deliverables and publishing

- [ ] Review repository for passwords, Wi-Fi details, tokens, private keys, device serials
- [ ] Create public PERSONAL GitHub repository and push **original** code+diagrams+README
- [ ] Intentionally add and commit sanitized REAL evidence screenshots (the evidence folder is gitignored by default; review before `git add -f`)
- [ ] Insert actual public repository/evidence URLs in showcase draft
- [ ] Post links in **personal Discord thread**, copy a **permalink**
- [ ] Follow [official PR guide](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter/blob/main/docs/github-pr-guide.md)
- [ ] Fork official repo and PR ONE showcase file at `projects/RDK-X5-EdgeVision-Ignite.md`
- [ ] Verify PR URLs accessible without authentication where expected

## Deadline

**Stage 1 ends Nov 10, 2026** according to the newsletter. Stage 2 opens Nov 11. Official program deadline Dec 15 should not be treated as an automatic extension of email's Stage 1 milestone.

**Current package status:** Not submitted, no hardware tests, no real screenshot, no Discord permalink, no GitHub PR.

## New verification tools

- `bash scripts/07_board_info.sh` — record non-sensitive board/kernel/camera metadata.
- Fill `submission/stage1_links.json` with actual verified links, board model, OS image version, and camera model.
- `python3 scripts/08_verify_submission.py` — validates expected PNG headers, dimensions, and link syntax only; it cannot verify genuineness or official acceptance.
- Video guide: `docs/VIDEO_REQUIREMENTS_AND_SHOTLIST_AR.md` — **Stage 1 video optional, Stage 3 video mandatory.**
