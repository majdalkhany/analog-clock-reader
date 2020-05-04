from imutils.object_detection import non_max_suppression
import numpy as np
import cv2 as cv
import pytesseract
import imutils
import globals

# This object is for the detection and correction of a clock image's orientation.
# An image is passed into orient_clock, and it checks for the image's orientation
# by using character recognition. EAST text detection is used to detect text,
# and pytesseract is used to figure out what the text actually is.
# Since OCR doesn't work unless the text is in the correct orientation,
# orient_clock will be rotating the image and applying OCR until it can detect
# the numbers on the clock, which would indicate that its correctly oriented.
# In this case that the clock image is already in the correct orientation,
# no work would be done and the image would be kept as-is.


# orient_clock main function, which recieves the clock image and returns it in the
# corrent orientation, if it needs to be re-oriented at all.
def orient_clock(clock_img):
    if (globals.is_demo):
        print("Orienting clock...")

    oriented_clock = fix_clock_orientation(clock_img, clock_img, 0)

    if (globals.is_demo):
        cv.imshow("Oriented image", oriented_clock)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return oriented_clock


# This function gets the original clock image (which it maintains without
# modifying at all), the rotated clock image, and the degrees to rotate the
# image. If it ends up rotating the image over 360 degrees then it cancels
# whatever it did and returns the original image it received.
def fix_clock_orientation(original_img, img, degree):
    # Tf the image is in the correct orientation, don't do anything and return
    # the original image received.
    if is_oriented_correctly(img):
        if (globals.is_demo):
            if (degree == 0):
                print("Clock is kept in its original orientation.")
            else:
                print("Clock is now in correct orientation: ", degree, "degrees")
        return img

    # If the image has been rotated 360 degrees or more, then the number detection
    # has failed for whatever reason and the original image will be returned.
    elif degree >= 360:
        if (globals.is_demo):
            print("Failed to orient clock. Clock is kept in its original orientation.")
        return original_img

    # In the case that the image is not oriented correctly and hasn't been rotated
    # >=360 degrees, rotate it by an interval of 10 degrees and recursively
    # check if it is now in the correct orientation.
    else:
        degree_plus = degree + 10
        if (globals.is_demo):
            print("Rotating", degree_plus, "degrees...")
        rotated_img = rotate_image(original_img, degree_plus)
        return fix_clock_orientation(original_img, rotated_img, degree_plus)


# Rotate the specified image by the specified degrees.
def rotate_image(original_img, degree):
    return imutils.rotate(original_img, degree)


# Pass the clock image and check if it contains numbers from 1 to 12.
# Numbers 6 and 9 are ignored because they are the usually interchangeable when
# either are flipped, which could cause some problems.
def is_oriented_correctly(img):
    # Get the list of detected numbers from the image.
    results = detect_hours(img)

    # Count how many elements are in that list, if they are more than 2 then
    # the clock is in the correct orientation, otherwise its still rotated.
    detected_numbers = 0
    res = [lis[1] for lis in results]
    for hour in [1, 2, 3, 4, 5, 7, 8, 10, 11, 12]:
        for x in res:
            if (x == str(hour)) or (x == (str(hour) + "-")):
                detected_numbers = detected_numbers + 1
    return detected_numbers > 2


def calculate_scores(score_map, geometry_map):
    # Get the dimensions of score_map.
    (rows, cols) = score_map.shape[2:4]

    # Initialize rects and confidences, which store the x and y coordinates for
    # the text region, and stores the corresponding probabilities associated with
    # rects, respectively.
    rects = []
    confidences = []

    # Loop over rows.
    for x in range(0, rows):
        score_data = score_map[0, 0, x]
        x_data0 = geometry_map[0, 0, x]
        x_data1 = geometry_map[0, 1, x]
        x_data2 = geometry_map[0, 2, x]
        x_data3 = geometry_map[0, 3, x]
        angles_data = geometry_map[0, 4, x]

        # Loop over columns.
        for y in range(0, cols):
            # If our score does not have sufficient probability, ignore it.
            if score_data[y] < 0.5:
                continue

            # Compute the offset factor as our resulting feature maps will be 4x smaller than the input image.
            (offset_x, offset_y) = (y * 4.0, x * 4.0)

            # Extract the rotation angle for the prediction and then compute the sin and cosine.
            angle = angles_data[y]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # Use the geometry volume to derive the width and height of the bounding box.
            h = x_data0[y] + x_data2[y]
            w = x_data1[y] + x_data3[y]

            # Compute both the starting and ending (x, y)-coordinates for the text prediction bounding box.
            end_x = int(offset_x + (cos * x_data1[y]) + (sin * x_data2[y]))
            end_y = int(offset_y - (sin * x_data1[y]) + (cos * x_data2[y]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)

            # Add the bounding box coordinates and probability score to our respective lists.
            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(score_data[y])

    # Return a tuple of the bounding boxes and associated confidences.
    return (rects, confidences)


# This is a function for applying the pytesseract OCR in order to detect
# the numbers (hours) on the clock image. This will only read numbers that
# are in the correct orientation, numbers that are upside down will
# not be detected.
def detect_hours(img):
    orig = img.copy()
    (orig_h, orig_w) = img.shape[:2]

    # Set the new width and height and then determine the ratio in change for both the width and height.
    rw = orig_w / float(320)
    rh = orig_h / float(320)

    # resize the image and grab the new image dimensions.
    img = cv.resize(img, (320, 320))
    (h, w) = img.shape[:2]

    # Load the EAST text detector.
    net = cv.dnn.readNet("frozen_east_text_detection.pb")

    # Construct a blob from the image and then perform a forward pass of the model to obtain the two output layer sets.
    blob = cv.dnn.blobFromImage(img, 1.0, (w, h), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

    # Decode the predictions, then  apply non-maxima suppression to suppress weak, overlapping bounding boxes.
    (rects, confidences) = calculate_scores(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # Initialize the list of results.
    results = []

    # Loop over the bounding boxes.
    for (start_x, start_y, end_x, end_y) in boxes:
        # Scale the bounding box coordinates based on the respective ratios.
        start_x = int(start_x * rw)
        start_y = int(start_y * rh)
        end_x = int(end_x * rw)
        end_y = int(end_y * rh)

        # In order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions.
        dx = int((end_x - start_x) * 0.0)
        dy = int((end_y - start_y) * 0.0)

        # Apply padding to each side of the bounding box, respectively.
        start_x = max(0, start_x - dx)
        start_y = max(0, start_y - dy)
        end_x = min(orig_w, end_x + (dx * 2))
        end_y = min(orig_h, end_y + (dy * 2))

        # Extract the actual padded ROI.
        roi = orig[start_y:end_y, start_x:end_x]

        # In order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text.
        config = ("-l eng --oem 1 --psm 7")
        text = pytesseract.image_to_string(roi, config=config)

        # Add the bounding box coordinates and OCR'd text to the list of results.
        results.append(((start_x, start_y, end_x, end_y), text))

    # Sort the results bounding box coordinates from top to bottom.
    return sorted(results, key=lambda r: r[0][1])
