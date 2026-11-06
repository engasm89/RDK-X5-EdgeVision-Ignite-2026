# Release Notes — v2 review (2026-11-06)

## Improvements

- Rechecked official **Winter 2026** rules (not Summer): Stage 1 does **not** require a video; Stage 3 does (3–7 min, 30s continuous AI).
- Added Arabic and English production shot lists and explicit Stage 1 screenshot checklist.
- Hardened official YOLO11m downloader with staging directory and strict archive entry validation; install failure leaves no partially extracted vendor demo.
- Added board-model guard to YOLO runner so the script refuses unsupported desktop/host execution instead of claiming physical proof.
- Added standalone sanitised board metadata collector, link/evidence registry and evidence auditing (PNG signature, dimensions and minimum bytes).
- Corrected documentation around GUI-required demonstration and verified GPIO BOARD pin 15 against D-Robotics documentation.
- All vendor inference code remains external and is downloaded on the actual board only.

## Verified locally vs still unknown

HOST ONLY: static tests, mocked-camera tests, shell parse and Python compile, PNG files and package integrity.

NOT VERIFIED: camera compatibility, complete vendor tar downloaded/executed on target board, flash result, physical board-model text (model string may require guard adjustment after inspection), GPIO output electrically, final public URLs, registration, competition acceptance.

A project cannot be *100% competition-ready* without real screenshots, working board, GitHub public URL, Discord permalink and official PR.
