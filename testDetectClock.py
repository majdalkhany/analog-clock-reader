import math
from detectClock import detectClock

# Converts HH:MM:SS format to int value of seconds only
def calculateSeconds(time):
    h, m, s = time.split(":")
    return (int(h) * 60 * 60) + (int(m) * 60) + int(s)

def calculateDifference(time1, time2):
    return abs(calculateSeconds(time1) - calculateSeconds(time2))

# There are 43,200 possible times on a 12-hour clock (60 * 60 * 12)
# Return the value truncated to 2 decimal places (not rounded)
def calculateAccuracy(diff):
    percentage = 100 - (diff / 43200)
    return math.floor(percentage * 10 ** 2) / 10 ** 2

# [0] is image, [1] is expected result
testCases = [
    ["clock1.jpg", "3:07:03"],
    ["clock1_skew.jpg", "3:07:03"],
    ["clock2.jpg", "10:09:25"]
    # ["clock3.jpg", "5:59:22"],
    # ["clock4.jpg", "10:09:38"],
    # ["watch1.jpg", "10:10:34"]
]

def testDetectClock():
    print('{:>5} {:>16} {:>16} {:>16} {:>16} {:>16}'.format("Test", "Image", "Expected", "Actual", "Difference (s)", "Accuracy (%)"))
    for i in range(0, len(testCases)):
        image = testCases[i][0]
        expected = testCases[i][1]
        actual = detectClock(image)
        diff = calculateDifference(expected, actual)
        accuracy = calculateAccuracy(diff)
        print('{:>5} {:>16} {:>16} {:>16} {:>16} {:>16}'.format(i + 1, image, expected, actual, diff, accuracy))

if __name__ == "__main__":
    testDetectClock()