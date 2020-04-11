import cv2 as cv
import numpy as np
import math
import globals
from utils import calculateAngle

# Most of these values were fine tuned based on testing images
cannyLowerThreshold = 100
cannyUpperThreshold = 200
houghLinesThreshold = 90
houghLinesMinLineLength = 5
houghLinesMaxLineGap = 25

# Returns three lines representing the hour, minute, and second hands (ie. [hour, minute, second])
def detectClockHands(clockImg):
    if (globals.isDemo): print("Detecting clock hands...")

    # Convert image to colour so coloured lines can be displayed
    clockImg = cv.cvtColor(clockImg, cv.COLOR_GRAY2BGR)

    # Extract edges from image
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)

    h = clockImg.shape[0]
    w = clockImg.shape[1]
    c = (h // 2, w // 2)
    r = h // 4

    if (globals.isDemo):
        cv.imshow("Canny edge detection", edges)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Detect lines in image
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, houghLinesThreshold, None, houghLinesMinLineLength, houghLinesMaxLineGap)
    if (lines is None):
        if (globals.isDemo): print("detectClockHands.py - No lines detected")
        return []

    # Append goodLines with lines that pass through a radius around the center specified by r
    # This ensures lines which do not represent clock hands are ignored
    goodLines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        d = abs(((x2 - x1) * c[0]) + ((y1 - y2) * c[1]) + ((x1 - x2) * y1) + ((y2 - y1) * x1)) / math.sqrt(math.pow((x2 - x1), 2) + math.pow((y1 - y2), 2))
        if d <= r:
            goodLines.append(line)

    if (globals.isDemo):
        clockImgCopy = clockImg.copy()
        for line in goodLines:
            for x1, y1, x2, y2 in line:
                cv.line(clockImgCopy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.imshow("Filtered lines", clockImgCopy)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Merge nearby lines together, otherwise each clock hand will have two lines (one on each edge)
    # The new merged line will be located at the midpoint between the two lines
    # mergedLines are of the form (x1, y1, x2, y2, t, a) where t is the thickness of the line and a is its angle
    mergedLines = []
    hasBeenMerged = []
    maxThetaDiff = 3
    for i in range(0, len(goodLines)):
        for j in range(i + 1, len(goodLines)):
            ix1, iy1, ix2, iy2 = goodLines[i][0]
            jx1, jy1, jx2, jy2 = goodLines[j][0]

            # Merge lines together if their angles are similar
            iTheta = calculateAngle(ix1, iy1, ix2, iy2)
            jTheta = calculateAngle(jx1, jy1, jx2, jy2)

            if (abs(iTheta - jTheta) <= maxThetaDiff):
                # To determine thickness, calculate distance from midpoint of one line to the closest point on the other line
                # Cannot just compare the endpoints since they may not line up
                midx = (ix2 + ix1) // 2
                midy = (iy2 + iy1) // 2
                p1 = np.array([jx1, jy1])
                p2 = np.array([jx2, jy2])
                p3 = np.array([midx, midy])
                t = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
                a = calculateAngle((ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2)

                # Exclude this line if its angle is too similar to an existing line
                addLine = True
                for line in mergedLines:
                    if abs(a - line[5]) < maxThetaDiff:
                        addLine = False
                        break

                if (addLine):
                    mergedLines.append([(ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2, t, a])

    # Sort mergedLines by thickness
    mergedLines.sort(key=lambda x:x[4], reverse=True)

    hasSeconds = len(mergedLines) > 2

    # Remove the thickness and angle value for each, don't need it at this point
    for line in mergedLines:
        line.pop()
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

    # Add second hand only if it exists
    if (hasSeconds):
        clockHands.append(mergedLines[2])

    # DISPLAY FOR TESTING PURPOSES
    # Print hour in red, minute in blue, second in green
    if (globals.isDemo):
        cv.line(clockImg, (clockHands[0][0], clockHands[0][1]), (clockHands[0][2], clockHands[0][3]), (0, 0, 255), 2)
        cv.line(clockImg, (clockHands[1][0], clockHands[1][1]), (clockHands[1][2], clockHands[1][3]), (255, 0, 0), 2)

        # Display second hand only if it exists
        if (hasSeconds):
            cv.line(clockImg, (clockHands[2][0], clockHands[2][1]), (clockHands[2][2], clockHands[2][3]), (0, 255, 0), 2)

        cv.imshow("Hour (red), minute (blue), second (green)", clockImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return clockHands