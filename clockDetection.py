import sys
import cv2 as cv
import numpy as np
import math

cannyLowerThreshold = 100
cannyUpperThreshold = 200
houghLinesThreshold = 90

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
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)

    lines = cv.HoughLines(edges, 1, np.pi / 180, houghLinesThreshold)

    # Remove lines that do not pass through center (ie. are not clock hands)
    h = clockImg.shape[0]
    w = clockImg.shape[1]
    c = (h // 2, w // 2)

    # Center radius that clock hands should pass through
    # This size is relative to the size of the image
    r = h // 30

    # Source: https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
    goodLines = []
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + w * b * -1)
        y1 = int(y0 + h * a)
        x2 = int(x0 - w * b * -1)
        y2 = int(y0 - h * a)

        # Add line to goodLines if it falls within the center's radius
        # Source: https://math.stackexchange.com/questions/275529/check-if-line-intersects-with-circles-perimeter
        d = abs(((x2 - x1) * c[0]) + ((y1 - y2) * c[1]) + ((x1 - x2) * y1) + ((y2 - y1) * x1)) / math.sqrt(math.pow((x2 - x1), 2) + math.pow((y1 - y2), 2))
        if d <= r:
            goodLines.append(line)
            cv.line(clockImg, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return clockImg

# Calling the hough detection function
# Passes image file into the function through the command line arguments
# FOR TESTING PURPOSES ONLY, TO BE REMOVED LATER
clockImg = cv.imread("images/" + sys.argv[1])
isolatedImg = isolateClock(clockImg)
hands = detectClockHands(isolatedImg)

cv.imshow("Clock", hands)
cv.waitKey(0)
cv.destroyAllWindows()

