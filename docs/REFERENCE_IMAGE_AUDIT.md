# Visual cross-check & image authenticity — 2026-11-06

## Authoritative design references

- RDK X5 official hardware introduction, including connector-function map, USB-A camera support, USB-C 5 V / 5 A dedicated power: https://developer.d-robotics.cc/rdk_doc/en/Quick_start/hardware_introduction/rdk_x5/
- Official D-Robotics USB camera + YOLO11m runtime instructions: https://developer.d-robotics.cc/x5_cases_doc/en/basic/detect
- Official Stage 1 required evidence: https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter/blob/main/stages/stage1-ignite.md
- A published photograph of the actual RDK X5 board (for visual comparison; respect publisher image copyright): https://cdn.shopify.com/s/files/1/0514/0719/2262/files/2025-06-16_11.57.16.png?v=1752042449

## Verified topology (not a verified physical assembly)

1. Board: D-Robotics **RDK X5** (not RDK X3 or RDK X5 Module). The genuine board has 40-pin GPIO, four USB 3.0 Type-A sockets, RJ45 Ethernet, dedicated USB-C power, HDMI, MIPI CSI camera connectors.
2. Sensor: **any specifically tested UVC-compatible USB webcam** in one of the USB-A host receptacles; the camera manufacturer/model has NOT been specified by the owner.
3. PSU: **5 V / 5 A**, into the dedicated power USB-C input, not the QuickLink connector or a laptop port.
4. Ethernet from RDK X5 RJ45 to a LAN router, or use Wi-Fi. SSH is from laptop over LAN, not a camera/USB-cable connection to the board.
5. Optional LED circuit is separately documented and is NOT model inference output. Power off before jumper wiring.

## Generated concept visual (assets/CONCEPT_ONLY_NOT_EVIDENCE.png)

Status: **illustrative ONLY; NOT electrically/physically certified and NOT 100% component-identical**. The product style broadly resembles the official RDK X5, but the camera model is arbitrary, some cable/port geometry in the generative image is unreliable, and the rendering is not an actual user's setup. Do **not** use this visual to decide the power or USB port, solder/wire anything, or claim challenge completion. Use only hardware/rdk_x5_wiring.svg and the official board port map for wiring.

### Explicitly rejected synthetic renders

The alternate collages included fabricated shell output, fabricated YOLO results and inconsistent GPIO wiring. They have been **excluded** from the published package. None are valid performance or Stage 1 proof. All evidence must come from the actual board and actual sensor.

## Remaining identity checks required for 100% match

- [ ] Photo of the user's *actual* RDK X5 and visible revision/connector positions.
- [ ] Webcam label, model, USB Vendor ID/Product ID, or USB camera actual photo.
- [ ] Verify port locations against the printed official board layout.
- [ ] Verify supply, microSD image version, boot and SSH on actual board.
- [ ] Verify `/dev/video*`, real camera frame, and real AI inference screenshot.

**Conclusion:** Verified *conceptual connection topology* from official documentation; not verified a 100%-identical depiction of the actual assembly or successful run.
