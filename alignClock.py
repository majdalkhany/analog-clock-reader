import cv2 as cv
import numpy as np
import globals

cannyLowerThreshold = 50
cannyUpperThreshold = 200

# Aligns a clock if it is skew (ie. not circular)
# 1. Finds edges using Canny edge detector
# 2. Finds contours using these edges
# 3. Calculates boundingRect (of the skewed clock) and minEnclosingCircle (of the skewed/unskewed clock)
# 4. Calculates transformation matrix using boundingRect and minEnclosingCircle values
# 5. Warps perspective using the transformation matrix

# Aligns an angled clock so it is a circle rather than an oval
def alignClock(clockImg):
    # Finding boundingRect and minEnclosingCircle of clock
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)
    contours, hierarchy = cv.findContours(edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
    c, r = cv.minEnclosingCircle(contours[0])
    x, y, w, h = cv.boundingRect(contours[0])
    cx = int(c[0])
    cy = int(c[1])
    r = int(r)

    # If the boundingRect is roughly the same size as the minEnclosingCircle, alignment is unnecessary
    if (x + w + 10 > cx + r and y + h + 10 > cy + r):
        return clockImg

    # Also do not align if the boundingRect ratios are way off as this is probably a false positive
    if (w < h / 2 or h < w / 2):
        return clockImg

    # Display contours of skewed clock, min enclosing circle, and bounding rect
    if (globals.isDemo):
        print("Aligning image...")
        drawImg = np.zeros_like(clockImg)
        cv.drawContours(drawImg, contours, 0, (255, 255, 255), cv.FILLED, 8, hierarchy)
        cv.circle(drawImg, (cx, cy), r, (0, 255, 0), 2)
        cv.rectangle(drawImg, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow("Clock contour (white), bounding rectangle (red), circle to warp to (green)", drawImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Calculate transformation matrix and uses it to warp the image perspective for alignment
    srcPoints = np.array([(x, y), (x + w, y), (x, y + h), (x + w, y + h)], np.float32)
    dstPoints = np.array([(cx - r, cy - r), (cx + r, cy - r), (cx - r, cy + r), (cx + r, cy + r)], np.float32)
    transMatrix = cv.getPerspectiveTransform(srcPoints, dstPoints)
    warpedImg = cv.warpPerspective(clockImg, transMatrix, (clockImg.shape[1], clockImg.shape[0]))

    # Display result of warping perspective
    if (globals.isDemo):
        cv.imshow("Image after perspective transform", warpedImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return warpedImg
