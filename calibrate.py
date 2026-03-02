#!/usr/bin/env python3
"""Calibrate a single SO-101 arm (leader or follower).

Sets the current physical position of every servo as the neutral
midpoint (raw value 2048), which is required before teleoperation.

Usage
-----
    python calibrate.py --leader   /dev/ttyACM0
    python calibrate.py --follower /dev/ttyACM1
"""

import argparse
import logging
import sys

from vassar_feetech_servo_sdk import ServoController

from config import SERVO_IDS, SERVO_TYPE

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate an SO-101 robot arm (sets current position as neutral 2048)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--leader", action="store_true", help="Calibrate the leader arm")
    group.add_argument("--follower", action="store_true", help="Calibrate the follower arm")
    parser.add_argument(
        "port",
        type=str,
        help="Serial port the arm is connected to (e.g. /dev/ttyACM0)",
    )
    return parser.parse_args()


def calibrate(role: str, port: str) -> None:
    """Connect to *port*, hold the arm in position, then zero all servos."""
    log.info("Starting calibration for %s arm on %s", role.upper(), port)

    controller = ServoController(servo_ids=SERVO_IDS, servo_type=SERVO_TYPE, port=port)

    try:
        controller.connect()

        input(
            "\nMove the arm to its desired neutral (home) position, "
            "then press [Enter] to calibrate …"
        )

        success = controller.set_middle_position()

        if success:
            log.info("%s arm calibrated — all servos set to 2048.", role.upper())
            final_positions = controller.read_all_positions()
            log.info("Final positions: %s", final_positions)
        else:
            log.error(
                "Calibration failed. Check that the servos are powered "
                "and that the servo IDs are correct."
            )
            sys.exit(1)

    except Exception as exc:
        log.error("Unexpected error: %s", exc)
        sys.exit(1)
    finally:
        controller.disconnect()
        log.info("Disconnected from %s.", port)


def main() -> None:
    args = parse_args()
    role = "leader" if args.leader else "follower"
    calibrate(role, args.port)


if __name__ == "__main__":
    main()