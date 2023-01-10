import cv2
import numpy as np
import math

def region(image):
    height, width = image.shape

    """triangle = np.array([
                       [(0, height), (int(width * 1 / 10), int(height / 2)), (int(width * 9 / 10), int(height / 2)), (width, height)]
                       ])"""

    triangle = np.array([
                       [(0, height), (0, int(height / 2)), (width, int(height / 2)), (width, height)]
                       ])

    mask = np.zeros_like(image)

    mask = cv2.fillPoly(mask, triangle, 255)

    #cv2.imshow("Mask", mask)

    mask = cv2.bitwise_and(image, mask)
    return mask

def drawHoughLines(image, lines):
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    return image

def drawHoughLinesP(image, lines):
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv2.line(image, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    return image

def getCorrectLines(lines):
    if lines is None:
        return None

    correctLines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)

        if slope > 0:
            correctLines.append(line)
        #print(f"x1: {x1} y1: {y1} x2: {x2} y2: {y2} Slope: {slope}")

    return correctLines


class LaneDetector:
    def detect(self, frame):
        open_cv_image = np.array(frame)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        img = open_cv_image.copy()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_white = np.array([20,60,100],np.uint8)
        upper_white = np.array([80,255,255],np.uint8)
        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        res = cv2.bitwise_and(img, img, mask=white_mask)

        res2 = cv2.bitwise_xor(img, res)

        cv2.imshow('res', res)
        cv2.imshow('res2',res2)

        gray = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

        cv2.imshow("thresh", thresh)

        blur = cv2.GaussianBlur(thresh, (5, 5), 0)

        edges = cv2.Canny(blur, 0, 255, L2gradient = True)

        region_image = region(edges)

        canny1 = cv2.bitwise_or(gray, edges)

        #lines = cv2.HoughLines(region_image, 1, np.pi / 180, 150, None, 0, 0)
        linesP = cv2.HoughLinesP(region_image, rho=1, theta=np.pi/180, threshold=50, minLineLength=1, maxLineGap=100)

        linesP = getCorrectLines(linesP)

        imgCopy = img.copy()

        #img = drawHoughLines(img, lines)
        imgCopy = drawHoughLinesP(imgCopy, linesP)

        #cv2.imshow("Hough Lane Detection", img)

        cv2.imshow("Hough Probabilistic Lane Detection", imgCopy)

        cv2.waitKey(1)
