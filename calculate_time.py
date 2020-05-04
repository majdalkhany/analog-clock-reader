import globals
from utils import calculate_angle


# Calculates time by determining the angles of the lines:
# 1. Calculates angle of each hand (eg. 12 o'clock is 0 degrees, 3 is 90, 6 is 180, and 9 is 270).
# 2. Uses angle of each hand to calculate its time value.
# 3. Formats time values and returns a single string.

# clockHands[0] - hour hand
# clockHands[1] - minute hand
# clockHands[2] - second hand (optional)
# Each hand contains 4 values: [x1, y1, x2, y2], ie. the start and end points.
def calculate_time(clock_hands, clock_img):
    if (globals.is_demo):
        print("Calculating time...")

    if (len(clock_hands) < 2):
        return None

    has_seconds = len(clock_hands) > 2

    # Calculate angles of hour, minute, and second hands.
    angles = []
    angles.append(calculate_angle(clock_hands[0][0], clock_hands[0][1], clock_hands[0][2], clock_hands[0][3]))
    angles.append(calculate_angle(clock_hands[1][0], clock_hands[1][1], clock_hands[1][2], clock_hands[1][3]))
    angles.append(calculate_angle(clock_hands[2][0], clock_hands[2][1], clock_hands[2][2], clock_hands[2][3]) if has_seconds else None)

    # If the hand is more on the left than right, the angle should be reversed.
    # For example, otherwise 45 min will be calculated as 15 min.
    for i in range(0, len(clock_hands)):
        if (angles[i] is None):
            continue

        x1 = clock_hands[i][0]
        x2 = clock_hands[i][2]
        cx = clock_img.shape[0] // 2
        if (abs(cx - x1) > abs(cx - x2)):
            angles[i] = angles[i] + 180

    # Calculate time values using angles of each hand.
    hour_angle, minute_angle, second_angle = angles
    hours_calculated = round((hour_angle / 360) * 12)
    minutes_calculated = round((minute_angle / 360) * 60)
    seconds_calculated = round((second_angle / 360) * 60) if has_seconds else None

    if (globals.is_demo):
        print("Clock hands:", clock_hands)
        print("Hour angle:", hour_angle)
        print("Minute angle:", minute_angle)
        print("Second angle:", second_angle)

    # Convert time to strings and format.
    hours_formatted = str(int(hours_calculated))
    minutes_formatted = str(int(minutes_calculated)) if minutes_calculated > 9 else "0" + str(int(minutes_calculated))
    seconds_formatted = (str(int(seconds_calculated)) if seconds_calculated > 9 else "0" + str(int(seconds_calculated))) if has_seconds else ""
    time_total = hours_formatted + ":" + minutes_formatted + ":" + seconds_formatted if has_seconds else hours_formatted + ":" + minutes_formatted
    return time_total
