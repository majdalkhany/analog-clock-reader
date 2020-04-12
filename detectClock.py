import sys
import cv2 as cv
import globals
from utils import calculateAngle
from alignClock import alignClock
from calculateTime import calculateTime
from detectClockHands import detectClockHands
from isolateClock import isolateClock
from orientClock import orientClock

# The main algorithm function that calls all other functions
# 1. Imports image
# 2. alignClock: aligns clock (if it is skew)
# 3. orientClock: orients clock (if it is rotated)
# 4. isolateClock: isolates image to only contain the clock
# 5. detectClockHands: detects the clock's hands
# 6. calculateTime: uses angles of clock hands to calculate the time 

# Passes image file into the function through the command line arguments
def detectClock(fileName, skipOrientClock = False):
    clockImg = cv.imread("images/" + fileName)

    if (globals.isDemo):
        cv.imshow("Input image", clockImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    alignedImg = alignClock(clockImg)

    # orientClock is a bottleneck so we may want to suppress this step when running a test script
    if (not skipOrientClock): orientedImg = orientClock(alignedImg)

    isolatedImg = isolateClock(orientedImg if not skipOrientClock else alignedImg)
    clockHands = detectClockHands(isolatedImg)
    time = calculateTime(clockHands, isolatedImg)
    return time

if __name__ == "__main__":
    globals.isDemo = True
    time = detectClock(sys.argv[1])

    if (time == None):
        print ("Failed to detect clock")
    else:
        print("Time: " + time)
