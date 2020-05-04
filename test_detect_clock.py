from detect_clock import detect_clock
from utils import calculate_difference
from utils import calculate_accuracy

# [0] is image, [1] is expected result
test_cases = [
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


# The main test function that goes through each test image and calculates the program's accuracy.
def test_detect_clock():
    print('{:>5} {:>20} {:>16} {:>16} {:>16} {:>16}'.format("Test", "Image", "Expected", "Actual", "Difference (s)", "Accuracy (%)"))
    for i in range(0, len(test_cases)):
        image = test_cases[i][0]
        expected = test_cases[i][1]

        # Only perform orient_clock step of algorithm if image is rotated.
        # The algorithm will work correctly if image is not rotated but doing so creates a bottleneck.
        actual = detect_clock(image, skip_orient_clock=("rotated" not in image))

        actualFormatted = actual if actual is not None else "None"
        diff = calculate_difference(expected, actual) if actual is not None else "-"
        accuracy = calculate_accuracy(diff) if actual is not None else "0.00"
        print('{:>5} {:>20} {:>16} {:>16} {:>16} {:>16}'.format(i + 1, image, expected, actualFormatted, diff, accuracy))


if __name__ == "__main__":
    test_detect_clock()
