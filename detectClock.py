import sys
import cv2 as cv
from alignClock import alignClock
from calculateAngle import calculateAngle
from calculateTime import calculateTime
from detectClockHands import detectClockHands
from isolateClock import isolateClock

# Passes image file into the function through the command line arguments
clockImg = cv.imread("images/" + sys.argv[1])
unwarpedImg = alignClock(clockImg)
isolatedImg = isolateClock(unwarpedImg)
clockHands = detectClockHands(isolatedImg)
time = calculateTime(clockHands)
print(time)
