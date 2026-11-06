# Optional Stage 2 concept after Stage 1 succeeds

**Concept**: EdgeVision workbench safety-monitor *prototype*, evolving the USB camera → on-device YOLO11m pipeline into a configurable object-presence alerting system.

Do not claim it meets safety-critical monitoring requirements: detection alone is not an interlock, and current Stage 1 LED demo is **not** connected to detections.

- Replace official GUI-only example with a tested output API for per-frame detections and event state.
- Decide target object classes, confidence threshold, and debounce based on board testing.
- Add optional GPIO indicators via a verified, electrically isolated actuator interface if controlling external loads.
- Stage 2 document CPU/BPU allocation, ROS 2 nodes and messages, bandwidth, hardware constraints, risk analysis, and fallback behavior.
- Stage 3 evaluate real latency/FPS and produce genuine end-to-end demo with test logs.
