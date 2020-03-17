import sys
import cv2 as cv
import numpy as np
import math

# A lot of these values are arbitary based on images that were tested
cannyLowerThreshold = 100
cannyUpperThreshold = 200

houghLinesThreshold = 90
houghLinesMinLineLength = 1
houghLinesMaxLineGap = 10

# This function is for detecting the clock's outer circumference using Hough Transform
# Recieves image as input and returns the same image cropped around the circle
def isolateClock(clockImg):
    # Convert the image to grayscale and blur
    gray = cv.cvtColor(clockImg, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(gray, 5)

    # Apply Hough Circle Transform
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 1000, param1=100, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))
    
    # Crop image around circle
    x = circles[0][0][0]
    y = circles[0][0][1]
    r = circles[0][0][2]
    return gray[(y-r):(y+r), (x-r):(x+r)]

def detectClockHands(clockImg):
    # TODO: FOR TESTING PURPOSES ONLY (ie. drawing lines in bright green)
    clockImg = cv.cvtColor(clockImg, cv.COLOR_GRAY2BGR)

    # Extract edges from image
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)

    h = clockImg.shape[0]
    w = clockImg.shape[1]
    c = (h // 2, w // 2)
    r = h // 30

    # Detect lines in image
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, houghLinesThreshold, None, houghLinesMinLineLength, houghLinesMaxLineGap)

    # Remove lines which do not pass through the center radius
    goodLines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        d = abs(((x2 - x1) * c[0]) + ((y1 - y2) * c[1]) + ((x1 - x2) * y1) + ((y2 - y1) * x1)) / math.sqrt(math.pow((x2 - x1), 2) + math.pow((y1 - y2), 2))
        if d <= r:
            goodLines.append(line)
            cv.line(clockImg, (x1, y1), (x2, y2), (0, 255, 0), 2)

    print(goodLines)
    return clockImg

# Calling the hough detection function
# Passes image file into the function through the command line arguments
# TODO: FOR TESTING PURPOSES ONLY, TO BE REMOVED LATER
clockImg = cv.imread("images/" + sys.argv[1])
isolatedImg = isolateClock(clockImg)
hands = detectClockHands(isolatedImg)

cv.imshow("Clock", hands)
cv.waitKey(0)
cv.destroyAllWindows()

