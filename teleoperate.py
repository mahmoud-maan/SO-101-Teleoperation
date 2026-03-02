#!/usr/bin/env python3
"""SO-101 teleoperation script.

Automatic leader/follower detection based on supply voltage:
  - Leader arm  (passive, hand-held): ~5 V  → voltage < VOLTAGE_THRESHOLD
  - Follower arm (powered):           ~12 V → voltage ≥ VOLTAGE_THRESHOLD

Usage
-----
    python teleoperate.py
    python teleoperate.py --frequency 100    # run at 100 Hz
    python teleoperate.py --no-print         # suppress position output
"""

import argparse
import logging
import time

from vassar_feetech_servo_sdk import ServoController, find_servo_port

from config import FREQUENCY, SERVO_IDS, SERVO_NAMES, SERVO_TYPE, VOLTAGE_THRESHOLD

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Teleoperate the SO-101 robot arm (leader → follower)."
    )
    parser.add_argument(
        "--frequency",
        type=int,
        default=FREQUENCY,
        metavar="HZ",
        help=f"Control loop frequency in Hz (default: {FREQUENCY})",
    )
    parser.add_argument(
        "--no-print",
        action="store_true",
        help="Suppress per-cycle position output",
    )
    return parser.parse_args()


def detect_leader_follower(
    ctrl1: ServoController,
    ctrl2: ServoController,
    port1: str,
    port2: str,
) -> tuple[ServoController, ServoController]:
    """Return (leader, follower) by reading the supply voltage on *ctrl1*."""
    voltage = ctrl1.read_voltage(SERVO_IDS[0])
    if voltage < VOLTAGE_THRESHOLD:
        log.info("%s → Leader  (%.1fV)", port1, voltage)
        log.info("%s → Follower", port2)
        return ctrl1, ctrl2
    else:
        log.info("%s → Follower (%.1fV)", port1, voltage)
        log.info("%s → Leader", port2)
        return ctrl2, ctrl1


def run_teleop(
    leader: ServoController,
    follower: ServoController,
    frequency: int,
    print_positions: bool,
) -> None:
    """Run the main teleoperation loop at *frequency* Hz."""
    loop_time = 1.0 / frequency
    log.info("Teleoperation running at %d Hz — press Ctrl+C to stop.", frequency)

    try:
        while True:
            start = time.perf_counter()

            positions = leader.read_positions()
            follower.write_position(positions)

            if print_positions:
                named = {SERVO_NAMES[k]: v for k, v in positions.items()}
                print("positions:", named)

            elapsed = time.perf_counter() - start
            if elapsed < loop_time:
                time.sleep(loop_time - elapsed)

    except KeyboardInterrupt:
        log.info("Teleoperation stopped.")


def main() -> None:
    args = parse_args()

    # Discover serial ports
    try:
        ports: list[str] = find_servo_port(return_all=True)
    except Exception as exc:
        log.error("Failed to scan serial ports: %s", exc)
        return

    if len(ports) < 2:
        log.error("Need 2 servo ports but found %d: %s", len(ports), ports)
        return

    log.info("Found ports: %s, %s", ports[0], ports[1])

    ctrl1 = ServoController(SERVO_IDS, SERVO_TYPE, ports[0])
    ctrl2 = ServoController(SERVO_IDS, SERVO_TYPE, ports[1])

    with ctrl1, ctrl2:
        leader, follower = detect_leader_follower(ctrl1, ctrl2, ports[0], ports[1])
        run_teleop(leader, follower, args.frequency, not args.no_print)


if __name__ == "__main__":
    main()
