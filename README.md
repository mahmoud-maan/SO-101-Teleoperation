# SO-101 Teleoperation

Python scripts for leader-follower teleoperation of the **SO-101** 6-DOF robot arm using Feetech STS/SMS series servos.

The leader arm (passive, hand-held) is detected automatically by its lower supply voltage (~5 V).  
The follower arm (powered, ~12 V) mirrors the leader's joint positions in real-time.

---

## Joint Map

| ID | Joint |
|----|-------|
| 1  | shoulder_pan |
| 2  | shoulder_lift |
| 3  | elbow_flex |
| 4  | wrist_flex |
| 5  | wrist_roll |
| 6  | gripper |

---

## Requirements

- Python 3.10+
- [vassar-feetech-servo-sdk](https://github.com/vassar-robotics/vassar-feetech-servo-sdk)
- Two USB-to-Serial adapters (one per arm)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Find Serial Ports

Plug in both arms and run:

```bash
python find_ports.py
```

Note the two port paths (e.g. `/dev/ttyACM0`, `/dev/ttyACM1`).

### 2. Calibrate

Calibrate each arm **once** before first use. This sets the current physical position as the servo neutral (raw value 2048).

```bash
# Leader arm
python calibrate.py --leader /dev/ttyACM0

# Follower arm
python calibrate.py --follower /dev/ttyACM1
```

Hold each arm in its desired home position before pressing Enter when prompted.

### 3. Teleoperate

Connect both arms and run:

```bash
python teleoperate.py
```

The script auto-detects which arm is the leader and which is the follower based on supply voltage.

**Options:**

```
--frequency HZ     Control loop frequency (default: 200 Hz)
--no-print         Suppress per-cycle position output
```

Example:

```bash
python teleoperate.py --frequency 100 --no-print
```

---

## Configuration

All shared constants (servo IDs, names, type, voltage threshold, default frequency) live in [`config.py`](config.py).

---

## Project Structure

```
SO-101-Teleoperation/
├── config.py          # Shared constants (servo IDs, names, thresholds)
├── teleoperate.py     # Main leader-follower teleoperation loop
├── calibrate.py       # One-time arm calibration utility
├── find_ports.py      # Scan and list connected servo ports
├── requirements.txt
└── README.md
```
