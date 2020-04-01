import cv2 as cv
import numpy as np

cannyLowerThreshold = 100
cannyUpperThreshold = 200

def unwarpClock(clockImg):
    edges = cv.Canny(clockImg, cannyLowerThreshold, cannyUpperThreshold)
    contours, hierarchy = cv.findContours(edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
    center, radius = cv.minEnclosingCircle(contours[0])
    rect = cv.boundingRect(contours[0])

    # Draw original image outline, circle, and bounding rect for testing purposes
    drawImg = np.zeros_like(clockImg)
    cv.drawContours(drawImg, contours, 0, (255, 255, 255), cv.FILLED, 8, hierarchy)
    cv.circle(drawImg, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)
    cv.rectangle(drawImg, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 2)

    cv.imshow("Bounding rectangle (red), circle to warp to (green)", drawImg)
    cv.waitKey(0)
    cv.destroyAllWindows()