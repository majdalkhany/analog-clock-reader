import cv2 as cv
import numpy as np
import globals

cannyLowerThreshold = 50
cannyUpperThreshold = 200

# Aligns an angled clock so it is a circle rather than an oval
def alignClock(clockImg):
    # Finding bounding rect and circle to warp into
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)
    contours, hierarchy = cv.findContours(edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
    c, r = cv.minEnclosingCircle(contours[0])
    x, y, w, h = cv.boundingRect(contours[0])

    # Convert center point and radius to int
    cx = int(c[0])
    cy = int(c[1])
    r = int(r)

    # If the boundingRect is roughly the same size as the minEnclosingCircle, alignment is unnecessary
    if (x + w + 10 > cx + r and y + h + 10 > cy + r):
        return clockImg

    # Also do not align if the boundingRect ratios are way off as this is probably a false positive
    if (w < h / 2 or h < w / 2):
        return clockImg

    if (globals.isDemo): print("Aligning image...")

    # Draw original image outline, circle, and bounding rect
    if (globals.isDemo):
        drawImg = np.zeros_like(clockImg)
        cv.drawContours(drawImg, contours, 0, (255, 255, 255), cv.FILLED, 8, hierarchy)
        cv.circle(drawImg, (cx, cy), r, (0, 255, 0), 2)
        cv.rectangle(drawImg, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow("Clock contour (white), bounding rectangle (red), circle to warp to (green)", drawImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Apply perspective transform
    srcPoints = np.array([(x, y), (x + w, y), (x, y + h), (x + w, y + h)], np.float32)
    dstPoints = np.array([(cx - r, cy - r), (cx + r, cy - r), (cx - r, cy + r), (cx + r, cy + r)], np.float32)
    transMatrix = cv.getPerspectiveTransform(srcPoints, dstPoints)
    warpedImg = cv.warpPerspective(clockImg, transMatrix, (clockImg.shape[1], clockImg.shape[0]))

    if (globals.isDemo):
        cv.imshow("Image after perspective transform", warpedImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return warpedImg
