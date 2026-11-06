# RDK X5 wiring and electrical safety (verified design assumptions)

## Core setup: no custom GPIO electronics required

| Source | Destination | Interface | Notes |
| --- | --- | --- | --- |
| Dedicated 5V/5A power supply | RDK X5 POWER USB-C input | Power | Never source from a laptop USB port |
| UVC USB camera | RDK X5 USB-A HOST | USB 2/3 + UVC | Meets sensor requirement; check actual V4L2 index |
| Ethernet router | RDK X5 Ethernet RJ45 | 1Gb Ethernet | Wi-Fi is also acceptable |
| HDMI monitor | RDK X5 HDMI OUT | HDMI | Useful for GUI YOLO11m demo; X11 forwarding alternative |
| Development PC | Network router -> RDK X5 | SSH/TCP | Screenshot live SSH commands |

## Optional LED expansion circuit — physical BOARD numbering

```
RDK X5 40-pin HEADER   470-ohm resistor       Red LED
GPIO BOARD pin 15  ----/\/\/\/\/-----------|>|------  GND BOARD pin 14
                                         anode   cathode
```

- Pin 15 is documented as a possible LED **OUTPUT** in Hobot.GPIO examples.
- Pin 14 is ground in the Raspberry-Pi-compatible 40-pin header. Confirm silk-screen location/board revision before wiring.
- Current (approx at 3.3V): `(3.3 - 2.0) / 470 = 2.8mA`, assuming ~2.0V red-LED forward drop. This is an approximate design calculation, not a measured current or board drive-capability guarantee.
- The RDK X5 digital IO level is 3.3V; on configurable carrier/module boards the IO voltage jumper must match; **never apply 5V to GPIO**.
- Disconnect RDK X5 power before adding/removing jumper leads.
- Check pin multiplexing via `sudo srpi-config` only if necessary. Pin function availability may vary by image/board revision.
- The LED script is a standalone test of the GPIO interface; it is **not linked** to YOLO detections.

## Sources

- https://developer.d-robotics.cc/rdk_doc/en/Quick_start/hardware_introduction/rdk_x5/
- https://developer.d-robotics.cc/rdk_doc/en/Basic_Application/01_40pin_user_sample/40pin_define/
- https://d-robotics.github.io/rdk_doc/en/Basic_Application/01_40pin_user_sample/gpio/
