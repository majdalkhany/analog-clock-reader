import math
import globals
from utils import calculateAngle

# Calculates time by determining the angles of the lines
# 1. Calculates angle of each hand (eg. 12 o'clock is 0 degrees, 3 is 90, 6 is 180, and 9 is 270)
# 2. Uses angle of each hand to calculate its time value
# 3. Formats time values and returns a single string

# clockHands[0] - hour hand
# clockHands[1] - minute hand
# clockHands[2] - second hand (optional)
# Each hand contains 4 values: [x1, y1, x2, y2], ie. the start and end points
def calculateTime(clockHands, clockImg):
    if (globals.isDemo): print("Calculating time...")
    if (len(clockHands) < 2): return None

    hasSeconds = len(clockHands) > 2

    # Calculate angles of hour, minute, and second hands
    angles = []
    angles.append(calculateAngle(clockHands[0][0], clockHands[0][1], clockHands[0][2], clockHands[0][3]))
    angles.append(calculateAngle(clockHands[1][0], clockHands[1][1], clockHands[1][2], clockHands[1][3]))
    angles.append(calculateAngle(clockHands[2][0], clockHands[2][1], clockHands[2][2], clockHands[2][3]) if hasSeconds else None)

    # If the hand is more on the left than right, the angle should be reversed
    # For example, otherwise 45 min will be calculated as 15 min
    for i in range(0, len(clockHands)):
        if (angles[i] == None): continue
        x1 = clockHands[i][0]
        x2 = clockHands[i][2]
        cx = clockImg.shape[0] // 2
        if (abs(cx - x1) > abs(cx - x2)):
            angles[i] = angles[i] + 180

    # Calculate time values using angles of each hand
    hourAngle, minuteAngle, secondAngle = angles
    hoursCalculated = round((hourAngle / 360) * 12)
    minutesCalculated = round((minuteAngle / 360) * 60)
    secondsCalculated = round((secondAngle / 360) * 60) if hasSeconds else None

    if (globals.isDemo):
        print("clockHands:", clockHands)
        print("Hour angle:", hourAngle)
        print("Minute angle:", minuteAngle)
        print("Second angle:", secondAngle)

    # Convert time to strings and format
    hoursFormatted = str(int(hoursCalculated))
    minutesFormatted = str(int(minutesCalculated)) if minutesCalculated > 9 else "0" + str(int(minutesCalculated))
    secondsFormatted = (str(int(secondsCalculated)) if secondsCalculated > 9 else "0" + str(int(secondsCalculated))) if hasSeconds else ""
    timeTotal = hoursFormatted + ":" + minutesFormatted + ":" + secondsFormatted if hasSeconds else hoursFormatted + ":" + minutesFormatted
    return timeTotal