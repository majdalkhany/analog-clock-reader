from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
import pytesseract


# TODO: Implement this (somehow)
def orientClock(clockImg):
    return clockImg


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
			if scoresData[y] < args["min_confidence"]:
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
