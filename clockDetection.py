import cv2
import numpy as np
import sys


#This function is for detecting the clock's outer circumference
#using Hough Transform
#Recieves the name of the image file as argument
def clockHoughDetection(imageName):
    clockimg = cv2.imread(imageName)
    #convert the image to grayscale first
    gray = cv2.cvtColor(clockimg, cv2.COLOR_BGR2GRAY)
    #make a copy of the grayscale image
    gray_copy = gray.copy()

    img = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 1000, param1=100, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        print(i)
        # outer circle
        cv2.circle(clockimg, (i[0], i[1]), i[2], (0,255,0), 1)
        #Center of the circle
        cv2.circle(clockimg, (i[0], i[1]), 2, (0,255,0), 3)

    #FOR TESTING PURPOSES ONLY, TO BE REMOVED LATER
    cv2.imshow("Circle Detection", clockimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




#Calling the hough detection function
#passes image file into the function through the command line arguments
#FOR TESTING PURPOSES ONLY, TO BE REMOVED LATER
clockHoughDetection(sys.argv[1])
