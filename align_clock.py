import cv2 as cv
import numpy as np
import globals

CANNY_LOWER_THRESHOLD = 50
CANNY_UPPER_THRESHOLD = 200


# Aligns a clock if it is skew (ie. not circular):
# 1. Finds edges using Canny edge detector.
# 2. Finds contours using these edges.
# 3. Calculates boundingRect (of the skewed clock) and minEnclosingCircle (of skewed/unskewed clock).
# 4. Calculates transformation matrix using boundingRect and minEnclosingCircle values.
# 5. Warps perspective using the transformation matrix.
def align_clock(clock_img):
    # Finding boundingRect and minEnclosingCircle of clock.
    edges = cv.Canny(clock_img, CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD)
    contours, hierarchy = cv.findContours(edges, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
    c, r = cv.minEnclosingCircle(contours[0])
    x, y, w, h = cv.boundingRect(contours[0])
    cx = int(c[0])
    cy = int(c[1])
    r = int(r)

    # If the boundingRect is roughly the same size as the minEnclosingCircle, alignment is unnecessary.
    if (x + w + 10 > cx + r and y + h + 10 > cy + r):
        return clock_img

    # Also do not align if the boundingRect ratios are way off as this is probably a false positive.
    if (w < h / 2 or h < w / 2):
        return clock_img

    # Display contours of skewed clock, min enclosing circle, and bounding rect.
    if (globals.is_demo):
        print("Aligning image...")
        draw_img = np.zeros_like(clock_img)
        cv.drawContours(draw_img, contours, 0, (255, 255, 255), cv.FILLED, 8, hierarchy)
        cv.circle(draw_img, (cx, cy), r, (0, 255, 0), 2)
        cv.rectangle(draw_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow("Clock contour (white), bounding rectangle (red), circle to warp to (green)", draw_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Calculate transformation matrix and uses it to warp the image perspective for alignment.
    src_points = np.array([(x, y), (x + w, y), (x, y + h), (x + w, y + h)], np.float32)
    dst_points = np.array([(cx - r, cy - r), (cx + r, cy - r), (cx - r, cy + r), (cx + r, cy + r)], np.float32)
    trans_matrix = cv.getPerspectiveTransform(src_points, dst_points)
    warped_img = cv.warpPerspective(clock_img, trans_matrix, (clock_img.shape[1], clock_img.shape[0]))

    # Display result of warping perspective.
    if (globals.is_demo):
        cv.imshow("Image after perspective transform", warped_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return warped_img
