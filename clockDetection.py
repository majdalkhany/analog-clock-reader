import sys
import cv2 as cv
import numpy as np
import math

# A lot of these values are arbitary based on images that were tested
cannyLowerThreshold = 100
cannyUpperThreshold = 200

houghLinesThreshold = 90
houghLinesMinLineLength = 5
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

    # Merge nearby lines together so there is not 2 lines for each hand
    # They will be turned into one line, located at the midpoint between the two lines
    # TODO: Probably need to track the thickness of the hand since the length of hour and minute hands are often similar
    mergedLines = []
    d = h // 30
    for i in range(0, len(goodLines)):
        for j in range(i + 1, len(goodLines)):
            ix1, iy1, ix2, iy2 = goodLines[i][0]
            jx1, jy1, jx2, jy2 = goodLines[j][0]
            if (abs(ix1 - jx1) < d and abs(iy1 - jy1) < d and abs(ix2 - jx2) < d and abs(iy2 - jy2) < d):
                mergedLines.append([(ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2]) 

    # TODO: DISPLAY FOR TESTING PURPOSES
    for line in mergedLines:
        x1, y1, x2, y2 = line
        cv.line(clockImg, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return clockImg

# Passes image file into the function through the command line arguments
clockImg = cv.imread("images/" + sys.argv[1])
isolatedImg = isolateClock(clockImg)
hands = detectClockHands(isolatedImg)

cv.imshow("Clock", hands)
cv.waitKey(0)
cv.destroyAllWindows()

