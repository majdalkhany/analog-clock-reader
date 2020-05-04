# Analog Clock Reader
COMP 4102 Final Project (Winter 2020)

Majd Al Khany - 100977501

Layne Koftinow-Mikan - 101013563

## Requirements to run
- OpenCV
- Tesseract and PyTesseract

## How to run
- Launch command: python detect_clock.py <image.jpg> (images must be in the images folder)
- Test framework launch command: python test_detect_clock.py

## How the algorithm works
Input: clock image
1. Align clock if it is sufficiently skewed (align_clock.py)
    1. Detect edges using Canny edge detector
    2. Use edges to detect clock contour using Suzuki contour detection
    3. Calculate the boundingRect and minEnclosingCircle of the contour
    4. Calculate the transformation matrix using boundingRect and minEnclosingCircle values
    5. Warp perspective using the transformation matrix
2. Orient clock if numbers cannot be detected (orient_clock.py)
    1. Detect text (numbers on the clock) in the input image using the EAST DNN text detector
    2. Place bounding boxes around the detected text in the image (for the OCR engine to be able to find the text and interpret it)
    3. Pass the image and data computed in the previous step by the EAST text detector to the PyTesseract OCR engine (in order to read the text on the image)
    4. If PyTesseract was able to successfully read the numbers on the clock image, then the image is in the correct orientation, return the image in its current state; otherwise,
        1. Use imutils.rotate to rotate the image by an interval of 10 degrees, and repeat the steps above until the image is in the correct orientation, at which point the image will be returned in the corrected orientation
        2. If the image gets rotated 360 degrees or more and PyTesseract still cannot read the text/numbers correctly, then all rotations are discarded and the image is returned in the same orientation that it was originally passed
3. Center the clock by cropping the image (isolate_clock.py)
    1. Convert image to greyscale and apply medianBlur
    2. Apply Hough transform to detect the clock’s outer circumference
    3. Crop the image around this circumference
4. Detect the clock's hands (detect_clock_hands.py)
    1. Detect edges using Canny edge detector
    2. Detect lines using probabilistic Hough transform on these edges
    3. Remove lines that cannot represent clock hands (ie. do not pass near center)
    4. Merge similar lines together into one line (since most hands will have more than one line corresponding to them)
    5. Estimate which lines represent hour, minute, and second hands using their length and thickness, resulting in a list of 2-3 lines (seconds hand is optional)
5. Calculate the time using the clock's hands (calculate_time.py)
    1. Calculate angle of each hand (eg. 12 o’clock is 0 degrees, 3 o’clock is 90 degrees, etc.)
    2. Use angles of each hand to calculate time value
    3. Format time values and return a single string
Output: string representing the time on the clock (hh:mm:ss)

## Example
Step | Screenshot
------------ | -------------
Input clock | ![Input image](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img1.png)
Isolated clock | ![Isolated image](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img2.png)
Edge detection | ![Edge detection](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img3.png)
Line detection | ![Line detection](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img4.png)
Hand estimates | ![Hand estimates](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img5.png)
Program output | ![Program output](https://github.com/majdalkhany/analog-clock-reader/blob/master/README_images/img6.png)
