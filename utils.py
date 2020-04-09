import math

# Determines angle given four points (x1, y1, x2, y2) using math.atan2
# Returns the value in radians, so the result needs to be converted to degrees
def calculateAngle(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

# Calculates distance between two points
def calculateDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x2)**2 + (y2 - y1)**2)