import cv2 as cv
import numpy as np
import math
import globals
from utils import calculate_angle

CANNY_LOWER_THRESHOLD = 100
CANNY_UPPER_THRESHOLD = 200
HOUGH_LINES_THRESHOLD = 90
HOUGH_LINES_MIN_LINE_LENGTH = 5
HOUGH_LINES_MAX_LINE_GAP = 25


# Detects the hands of the clock:
# 1. Detects edges using Canny edge detector.
# 2. Detects lines using Hough transform on the edges.
# 3. Removes lines that cannot represent clock hands (ie. they do not pass near the center).
# 4. Merges similar lines together into one line (since most hands will have >1 lines corresponding to them).
# 5. Uses line length and thickness to estimate which lines represent the hour, minute, and second hands.
# Note: the second hand is considered optional as not all clocks have this.
# Returns three vectors representing the hour, minute, and second hands (ie. [[hour], [minute], [second]]).
def detect_clock_hands(clock_img):
    if (globals.is_demo):
        print("Detecting clock hands...")

    # Extract edges from image
    edges = cv.Canny(clock_img, CANNY_LOWER_THRESHOLD, CANNY_UPPER_THRESHOLD)

    h = clock_img.shape[0]
    w = clock_img.shape[1]
    c = (h // 2, w // 2)
    r = h // 4

    # Display result of Canndy edge detection
    if (globals.is_demo):
        cv.imshow("Canny edge detection for Hough", edges)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Detect lines in image
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, HOUGH_LINES_THRESHOLD, None, HOUGH_LINES_MIN_LINE_LENGTH, HOUGH_LINES_MAX_LINE_GAP)
    if (lines is None):
        if (globals.is_demo):
            print("detectClockHands.py - No lines detected")
        return []

    # Display all detected lines
    if (globals.is_demo):
        clock_img_copy = cv.cvtColor(clock_img.copy(), cv.COLOR_GRAY2BGR)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(clock_img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.imshow("Hough line detection", clock_img_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Append goodLines with lines that pass through a radius around the center specified by r
    # This ensures lines which do not represent clock hands are ignored
    good_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        d = abs(((x2 - x1) * c[0]) + ((y1 - y2) * c[1]) + ((x1 - x2) * y1) + ((y2 - y1) * x1)) / math.sqrt(math.pow((x2 - x1), 2) + math.pow((y1 - y2), 2))
        if d <= r:
            good_lines.append(line)

    # Display all good lines
    if (globals.is_demo):
        clock_img_copy = cv.cvtColor(clock_img.copy(), cv.COLOR_GRAY2BGR)
        for line in good_lines:
            for x1, y1, x2, y2 in line:
                cv.line(clock_img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.imshow("Filtered lines", clock_img_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Merge nearby lines together, otherwise each clock hand will have two lines (one on each edge)
    # The new merged line will be located at the midpoint between the two lines
    # mergedLines are of the form (x1, y1, x2, y2, t, a) where t is the thickness of the line and a is its angle
    merged_lines = []
    max_theta_diff = 3
    for i in range(0, len(good_lines)):
        for j in range(i + 1, len(good_lines)):
            ix1, iy1, ix2, iy2 = good_lines[i][0]
            jx1, jy1, jx2, jy2 = good_lines[j][0]

            # Merge lines together only if their angles are similar
            i_theta = calculate_angle(ix1, iy1, ix2, iy2)
            j_theta = calculate_angle(jx1, jy1, jx2, jy2)

            if (abs(i_theta - j_theta) <= max_theta_diff):
                # To determine thickness, calculate distance from midpoint of one line to the closest point on the other line
                # Cannot just compare the endpoints since they may not line up
                midx = (ix2 + ix1) // 2
                midy = (iy2 + iy1) // 2
                p1 = np.array([jx1, jy1])
                p2 = np.array([jx2, jy2])
                p3 = np.array([midx, midy])
                t = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
                a = calculate_angle((ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2)

                # Exclude this line if its angle is too similar to an existing line
                add_line = True
                for line in merged_lines:
                    if abs(a - line[5]) < max_theta_diff:
                        add_line = False
                        break

                # Merge the lines and append them to the list
                if (add_line):
                    merged_lines.append([(ix1 + jx1) // 2, (iy1 + jy1) // 2, (ix2 + jx2) // 2, (iy2 + jy2) // 2, t, a])

    # Sort mergedLines by thickness
    merged_lines.sort(key=lambda x: x[4], reverse=True)

    has_seconds = len(merged_lines) > 2

    # Remove the thickness and angle value for each, don't need it at this point
    for line in merged_lines:
        line.pop()
        line.pop()

    # The two thickest lines are the hour and minute hand, the shorter of which is the hour hand
    # The remaining line is therefore the second hand
    clock_hands = []
    line1_length = math.sqrt((merged_lines[0][2] - merged_lines[0][0])**2 + (merged_lines[0][3] - merged_lines[0][1])**2)
    line2_length = math.sqrt((merged_lines[1][2] - merged_lines[1][0])**2 + (merged_lines[1][3] - merged_lines[1][1])**2)

    if (line1_length < line2_length):
        clock_hands.append(merged_lines[0])
        clock_hands.append(merged_lines[1])
    else:
        clock_hands.append(merged_lines[1])
        clock_hands.append(merged_lines[0])

    # Add second hand only if it exists
    if (has_seconds):
        clock_hands.append(merged_lines[2])

    # Display hour hand in red, minute hand in blue, and second hand in green
    if (globals.is_demo):
        clock_img_copy = cv.cvtColor(clock_img.copy(), cv.COLOR_GRAY2BGR)
        cv.line(clock_img_copy, (clock_hands[0][0], clock_hands[0][1]), (clock_hands[0][2], clock_hands[0][3]), (0, 0, 255), 2)
        cv.line(clock_img_copy, (clock_hands[1][0], clock_hands[1][1]), (clock_hands[1][2], clock_hands[1][3]), (255, 0, 0), 2)

        # Display second hand only if it exists
        if (has_seconds):
            cv.line(clock_img_copy, (clock_hands[2][0], clock_hands[2][1]), (clock_hands[2][2], clock_hands[2][3]), (0, 255, 0), 2)

        cv.imshow("Hour (red), minute (blue), second (green)", clock_img_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return clock_hands
