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

# Returns three lines representing the hour, minute, and second hands (ie. [hour, minute, second])
# TODO: Support not having a second hand
def detectClockHands(clockImg):
    # Convert image to colour so coloured lines can be displayed
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
    # mergedLines are of the form (x1, y1, x2, y2, t) where t is the thickness of the line
    mergedLines = []
    d = h // 30
    for i in range(0, len(goodLines)):
        for j in range(i + 1, len(goodLines)):
            ix1, iy1, ix2, iy2 = goodLines[i][0]
            jx1, jy1, jx2, jy2 = goodLines[j][0]
            if (abs(ix1 - jx1) < d and abs(iy1 - jy1) < d and abs(ix2 - jx2) < d and abs(iy2 - jy2) < d):
                t = math.sqrt((jx1 - ix1)**2 + (jy1 - iy1)**2)
                mergedLines.append([(ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2, t])
    
    # Sort mergedLines by thickness
    mergedLines.sort(key=lambda x:x[4], reverse=True)
    print("mergedLines: ", mergedLines)
    print("NOTE: This list should only ever have 2 or 3 values")

    # Remove the thickness value for each, don't need it at this point
    for line in mergedLines:
        line.pop()

    # The two thickest lines are the hour and minute hand, the shorter of which is the hour hand
    # The remaining line is therefore the second hand
    clockHands = []
    line1Length = math.sqrt((mergedLines[0][2] - mergedLines[0][0])**2 + (mergedLines[0][3] - mergedLines[0][1])**2)
    line2Length = math.sqrt((mergedLines[1][2] - mergedLines[1][0])**2 + (mergedLines[1][3] - mergedLines[1][1])**2)

    if (line1Length < line2Length):
        clockHands.append(mergedLines[0])
        clockHands.append(mergedLines[1])
    else:
        clockHands.append(mergedLines[1])
        clockHands.append(mergedLines[0])
    
    clockHands.append(mergedLines[2])

    # DISPLAY FOR TESTING PURPOSES
    # Print hour in red, minute in blue, second in green
    cv.line(clockImg, (clockHands[0][0], clockHands[0][1]), (clockHands[0][2], clockHands[0][3]), (0, 0, 255), 2)
    cv.line(clockImg, (clockHands[1][0], clockHands[1][1]), (clockHands[1][2], clockHands[1][3]), (255, 0, 0), 2)
    cv.line(clockImg, (clockHands[2][0], clockHands[2][1]), (clockHands[2][2], clockHands[2][3]), (0, 255, 0), 2)

    return clockImg

# Passes image file into the function through the command line arguments
clockImg = cv.imread("images/" + sys.argv[1])
isolatedImg = isolateClock(clockImg)
hands = detectClockHands(isolatedImg)

cv.imshow("Clock", hands)
cv.waitKey(0)
cv.destroyAllWindows()

