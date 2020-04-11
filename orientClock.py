from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import pytesseract
import imutils


def orientClock(clockImg):
    fixedImageOrientation = fixClockOrientation(clockImg, clockImg, 0, 0)
    return fixedImageOrientation

#this function gets the clock image, the degrees to rotate the image
#and a degree counter. If it ends up rotating the image over 360 degrees
#then it cancels whatever it did and returns the original image it received
def fixClockOrientation(originalImage, image, degree, degreeCounter):
	degreeCounter = degreeCounter+degree
	if isOrientedCorrectly(image) == True:
		print("image is now in correct orientation: ", degreeCounter, "degrees")
		return image
	elif degreeCounter >=360:
		print("the image is kept in its original orientation:")
		return originalImage
	else:
		degreePlus = degree+2
		rotatedImage = rotateImage(image,degreePlus)
		fixClockOrientation(originalImage, rotatedImage, degreePlus, degreeCounter)

#rotate the specified image by the specified degrees
def rotateImage(image,degree):
	rotatedImg = imutils.rotate(image, degree)
	return rotatedImg

#pass the results array and check if it contains a number from 1 to 12
def isOrientedCorrectly(image):
	results = detectHours(image)
	detectedNumbers = 0
	res = [lis[1] for lis in results]
	for hour in np.arange(1, 12, 1):
		for x in res:
			if x == str(hour):
				detectedNumbers = detectedNumbers+1
	if detectedNumbers >= 2:
		return True
	else:
		return False


def calculateScores(scoreMap, geometryMap):
	#get the dimensions of scoreMap
	(nRows, nColumns) = scoreMap.shape[2:4]

    #initialize rects and confidences, which store the x and y coordinates for
    #the text region, and stores the corresponding probabilities associated with
    #rects, respectively
	rects = []
	confidences = []

	#loop over rows
	for x in range(0, nRows):
		scoresData = scoreMap[0, 0, x]
		xData0 = geometryMap[0, 0, x]
		xData1 = geometryMap[0, 1, x]
		xData2 = geometryMap[0, 2, x]
		xData3 = geometryMap[0, 3, x]
		anglesData = geometryMap[0, 4, x]
		# loop over columns
		for y in range(0, nColumns):
			# if our score does not have sufficient probability,
			# ignore it
			if scoresData[y] < 0.5:
				continue
			# compute the offset factor as our resulting feature
			# maps will be 4x smaller than the input image
			(offsetX, offsetY) = (y * 4.0, x * 4.0)
			# extract the rotation angle for the prediction and
			# then compute the sin and cosine
			angle = anglesData[y]
			cos = np.cos(angle)
			sin = np.sin(angle)
			# use the geometry volume to derive the width and height
			# of the bounding box
			h = xData0[y] + xData2[y]
			w = xData1[y] + xData3[y]
			# compute both the starting and ending (x, y)-coordinates
			# for the text prediction bounding box
			endX = int(offsetX + (cos * xData1[y]) + (sin * xData2[y]))
			endY = int(offsetY - (sin * xData1[y]) + (cos * xData2[y]))
			startX = int(endX - w)
			startY = int(endY - h)
			# add the bounding box coordinates and probability score
			# to our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[y])
	# return a tuple of the bounding boxes and associated confidences
	return (rects, confidences)





def detectHours(image):
    orig = image.copy()

    (origH, origW) = image.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    rW = origW / float(320)
    rH = origH / float(320)

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (320, 320))
    (H, W) = image.shape[:2]

    #Load the EAST text detector
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
    	(123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"])

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = calculateScores(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
    	# scale the bounding box coordinates based on the respective
    	# ratios
    	startX = int(startX * rW)
    	startY = int(startY * rH)
    	endX = int(endX * rW)
    	endY = int(endY * rH)

    	# in order to obtain a better OCR of the text we can potentially
    	# apply a bit of padding surrounding the bounding box -- here we
    	# are computing the deltas in both the x and y directions
    	dX = int((endX - startX) * 0.0)
    	dY = int((endY - startY) * 0.0)

    	# apply padding to each side of the bounding box, respectively
    	startX = max(0, startX - dX)
    	startY = max(0, startY - dY)
    	endX = min(origW, endX + (dX * 2))
    	endY = min(origH, endY + (dY * 2))

    	# extract the actual padded ROI
    	roi = orig[startY:endY, startX:endX]

        	# in order to apply Tesseract v4 to OCR text we must supply
    	# (1) a language, (2) an OEM flag of 4, indicating that the we
    	# wish to use the LSTM neural net model for OCR, and finally
    	# (3) an OEM value, in this case, 7 which implies that we are
    	# treating the ROI as a single line of text
    	config = ("-l eng --oem 1 --psm 7")
    	text = pytesseract.image_to_string(roi, config=config)

    	# add the bounding box coordinates and OCR'd text to the list
    	# of results
    	results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r:r[0][1])
    return results
