import cv2 as cv
import numpy as np
import globals

# Detects the clock's outer circumference using Hough Transform
# Returns the image cropped around the circle representing the clock's face
# The center of the clock will be the center of the image
def isolateClock(clockImg):
    if (globals.isDemo): print("Isolating clock...")

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
    isolatedImg = gray[(y-r):(y+r), (x-r):(x+r)]

    if (globals.isDemo):
        cv.imshow("Isolated clock", isolatedImg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return isolatedImg