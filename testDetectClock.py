import math
from detectClock import detectClock

# Converts HH:MM:SS format to int value of seconds only
def calculateSeconds(time):
    times = time.split(":")
    if (len(times) > 2):
        h, m, s = times
        return (int(h) * 60 * 60) + (int(m) * 60) + int(s)
    else:
        h, m = times
        return (int(h) * 60 * 60) + (int(m) * 60)

def calculateDifference(time1, time2):
    return abs(calculateSeconds(time1) - calculateSeconds(time2))

# There are 43,200 possible times on a 12-hour clock (60 * 60 * 12)
# Return the value truncated to 2 decimal places (not rounded)
def calculateAccuracy(diff):
    percentage = 100 - ((diff / 43200) * 100)
    return math.floor(percentage * 10 ** 2) / 10 ** 2

# [0] is image, [1] is expected result
testCases = [
    ["clock1.jpg", "3:07:03"],
    ["clock1_skew.jpg", "3:07:03"],
    ["clock1_rotated.jpg", "3:07:03"],
    ["clock2.jpg", "10:10:25"],
    ["clock2_skew.jpg", "10:10:25"],
    ["clock3.jpg", "10:10:38"],
    ["clock4.jpg", "4:38:36"],
    ["clock5.jpg", "10:09"],
    ["clock6.jpg", "2:39:51"],
    ["clock7.jpg", "10:09"],
    ["clock7_rotated.jpg", "10:09"],
    ["watch1.jpg", "10:09:33"],
    ["watch2.jpg", "10:09:36"]
]

def testDetectClock():
    print('{:>5} {:>20} {:>16} {:>16} {:>16} {:>16}'.format("Test", "Image", "Expected", "Actual", "Difference (s)", "Accuracy (%)"))
    for i in range(0, len(testCases)):
        image = testCases[i][0]
        expected = testCases[i][1]

        # Only perform orientClock step of algorithm if image is rotated
        # The algorithm will work correctly if image is not rotated but doing so creates a bottleneck
        actual = detectClock(image, skipOrientClock=(not "rotated" in image))

        actualFormatted = actual if actual != None else "None"
        diff = calculateDifference(expected, actual) if actual != None else "-"
        accuracy = calculateAccuracy(diff) if actual != None else "0.00"
        print('{:>5} {:>20} {:>16} {:>16} {:>16} {:>16}'.format(i + 1, image, expected, actualFormatted, diff, accuracy))

if __name__ == "__main__":
    testDetectClock()
