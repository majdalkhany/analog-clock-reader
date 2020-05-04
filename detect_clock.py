import sys
import cv2 as cv
import globals
from align_clock import align_clock
from calculate_time import calculate_time
from detect_clock_hands import detect_clock_hands
from isolate_clock import isolate_clock
from orient_clock import orient_clock


# The main algorithm function that calls all other functions:
# 1. Imports image.
# 2. alignClock: aligns clock (if it is skew).
# 3. orientClock: orients clock (if it is rotated).
# 4. isolateClock: isolates image to only contain the clock.
# 5. detectClockHands: detects the clock's hands.
# 6. calculateTime: uses angles of clock hands to calculate the time.

# Passes image file into the function through the command line arguments.
def detect_clock(file_name, skip_orient_clock=False):
    clock_img = cv.imread("images/" + file_name)

    if (globals.is_demo):
        cv.imshow("Input image", clock_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    aligned_img = align_clock(clock_img)

    # orient_clock is a bottleneck so we may want to suppress this step when running a test script.
    if (not skip_orient_clock):
        oriented_img = orient_clock(aligned_img)

    isolated_img = isolate_clock(oriented_img if not skip_orient_clock else aligned_img)
    clock_hands = detect_clock_hands(isolated_img)
    time = calculate_time(clock_hands, isolated_img)
    return time


if __name__ == "__main__":
    globals.is_demo = True
    time = detect_clock(sys.argv[1])

    if (time is None):
        print("Failed to detect clock")
    else:
        print("Time: " + time)
