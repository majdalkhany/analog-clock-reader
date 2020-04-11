import sys
import cv2 as cv
import globals
from alignClock import alignClock
from calculateTime import calculateTime
from detectClockHands import detectClockHands
from isolateClock import isolateClock
from orientClock import orientClock

# Passes image file into the function through the command line arguments
def detectClock(fileName):
    clockImg = cv.imread("images/" + fileName)
    alignedImg = alignClock(clockImg)
    orientedImg = orientClock(alignedImg)
    isolatedImg = isolateClock(orientedImg)
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
