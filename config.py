"""Shared configuration for the SO-101 teleoperation project."""

# Servo IDs present on both arms
SERVO_IDS: list[int] = [1, 2, 3, 4, 5, 6]

# Human-readable names for each servo
SERVO_NAMES: dict[int, str] = {
    1: "shoulder_pan",
    2: "shoulder_lift",
    3: "elbow_flex",
    4: "wrist_flex",
    5: "wrist_roll",
    6: "gripper",
}

# Servo protocol type: "sts" (STS/SMS series) or "hls" (HLS series)
SERVO_TYPE: str = "sts"

# Voltage threshold (V) used to distinguish leader from follower.
# Leader arm (passive, hand-held): ~5 V
# Follower arm (powered):          ~12 V
VOLTAGE_THRESHOLD: float = 9.0

# Teleoperation control loop frequency (Hz)
FREQUENCY: int = 200
