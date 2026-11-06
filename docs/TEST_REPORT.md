# QA and release verification — 2026-11-06 (v2)

## Automated local verification (not physical board)

- **Python unit tests: 11 PASSED, 0 FAILED.** Camera capture (mock), GPIO cleanup (mock), PNG evidence parsing, submission gate, CLI argument validation, host board guard, vendor archive safe install and path-traversal rejection.
- Python compile check: PASS.
- Bash syntax (`bash -n`) check: PASS.
- Vendor archive installer tested with a **local fixture** only; real download and runtime are not verified.
- Source package SHA-256 manifest and ZIP integrity test: PASS.
- Wiring diagrams PNG/SVG are documentation, **not** photographs of real RDK X5.
- `08_verify_submission.py`: **EXPECTED FAIL**, pending 3 genuine PNG screenshots, 3 real public links and 3 actual hardware metadata values.

## Not yet verified

Physical board flash and SSH; specific OS image; camera frame on board; official YOLO11m runtime + BPU inference; GUI availability; LED voltage/pinmux on user's revision; raw evidence validity; registration; public GitHub and Discord URL access; official showcase PR; organizer acceptance.

## Release decision

**STATUS: SOFTWARE PACKAGE QA PASS / PHYSICAL SUBMISSION NOT READY.**

Do not mark the contest completed or claim 100% readiness until device evidence and external submission are verified.
