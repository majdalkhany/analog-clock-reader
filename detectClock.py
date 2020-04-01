import sys
import cv2 as cv
from calculateAngle import calculateAngle
from calculateTime import calculateTime
from detectClockHands import detectClockHands
from isolateClock import isolateClock

# Passes image file into the function through the command line arguments
clockImg = cv.imread("images/" + sys.argv[1])
isolatedImg = isolateClock(clockImg)
clockHands = detectClockHands(isolatedImg)
time = calculateTime(clockHands)
print(time)
