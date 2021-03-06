import cv2 as cv
import numpy as np
import globals


# Isolates clock by cropping the image around the clock so the clock's center is the image center:
# 1. Convert image to greyscale and blur.
# 2. Apply HoughCircles to detect the clock's outer circumcerence.
# 3. Crop the image around this circumference.
def isolate_clock(clock_img):
    if (globals.is_demo):
        print("Isolating clock...")

    # Convert the image to grayscale and blur.
    gray = cv.cvtColor(clock_img, cv.COLOR_BGR2GRAY)
    img = cv.medianBlur(gray, 5)

    # Apply Hough Circle Transform.
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 1000, param1=100, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))

    # Crop image around circle.
    x = circles[0][0][0]
    y = circles[0][0][1]
    r = circles[0][0][2]
    isolated_img = gray[(y - r):(y + r), (x - r):(x + r)]

    # Display the isolated clock.
    if (globals.is_demo):
        cv.imshow("Isolated clock", isolated_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return isolated_img
