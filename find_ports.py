#!/usr/bin/env python3
"""Scan for connected Feetech servo controllers and print their serial ports.

Usage
-----
    python find_ports.py
"""

import logging

from vassar_feetech_servo_sdk import find_servo_port

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def main() -> None:
    """Print every serial port that has a Feetech servo controller attached."""
    try:
        ports: list[str] = find_servo_port(return_all=True)
    except Exception as exc:
        log.error("Failed to scan serial ports: %s", exc)
        return

    if not ports:
        log.warning("No servo ports found. Check USB connections and driver permissions.")
        return

    log.info("Found %d servo port(s):", len(ports))
    for i, port in enumerate(ports, start=1):
        print(f"  {i}. {port}")


if __name__ == "__main__":
    main()