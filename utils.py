import math


# Determines angle given four points (x1, y1, x2, y2) using math.atan2
# Returns the value in radians, so the result needs to be converted to degrees
def calculate_angle(x1, y1, x2, y2):
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90
    return angle if angle > 0 else 360 - abs(angle)


# Converts HH:MM:SS format to int value of seconds only.
def calculate_seconds(time):
    times = time.split(":")
    if (len(times) > 2):
        h, m, s = times
        return (int(h) * 60 * 60) + (int(m) * 60) + int(s)
    else:
        h, m = times
        return (int(h) * 60 * 60) + (int(m) * 60)


# Calculates the difference between two times (in seconds).
def calculate_difference(time1, time2):
    return abs(calculate_seconds(time1) - calculate_seconds(time2))


# Calculate how accurate a time difference is compared to all possible times.
# Note: there are 43,200 possible times on a 12-hour clock (60 * 60 * 12).
def calculate_accuracy(diff):
    percentage = 100 - ((diff / 43200) * 100)
    return math.floor(percentage * 10 ** 2) / 10 ** 2
