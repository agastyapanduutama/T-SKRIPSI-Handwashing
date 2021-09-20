import cv2
import os
import numpy as np


os.system("cls")

cap0 = cv2.VideoCapture(0)

M = 100
N = 200


def invImage(grayImage):
    M = grayImage.shape[0]
    N = grayImage.shape[1]
    for i in range(M):
        for j in range(N):
            grayImage[i, j] = abs(255-grayImage[i, j])

    return grayImage


def checkBackGround(grayImage):
    M = grayImage.shape[0]
    N = grayImage.shape[1]


invThr = 150

if (cap0.isOpened()):
    while(True):
        ret, frame0 = cap0.read()
        frame0 = cv2.resize(frame0, (N, M), interpolation=cv2.INTER_AREA)
        frame0 = cv2.GaussianBlur(frame0, (5, 5), 0)

        red = frame0[:, :, 2]
        gre = frame0[:, :, 1]
        blu = frame0[:, :, 0]

        hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)
        hue = hsv[:, :, 0]
        sat = hsv[:, :, 1]
        vvv = hsv[:, :, 2]

        lab = cv2.cvtColor(frame0, cv2.COLOR_BGR2LAB)
        lComp = lab[:, :, 0]
        aComp = lab[:, :, 1]
        bComp = lab[:, :, 2]

        rgbImg = np.hstack((red, gre, blu))
        hsvImg = np.hstack((hue, sat, vvv))
        labImg = np.hstack((lComp, aComp, bComp))

        imgGrid = np.vstack((rgbImg, hsvImg, labImg))

        ret, redTh = cv2.threshold(red, 0, 255, cv2.THRESH_OTSU)
        if (redTh[10, (M-1)] >= invThr):
            redTh = invImage(redTh)
        ret, greTh = cv2.threshold(gre, 0, 255, cv2.THRESH_OTSU)
        if (greTh[10, (M-1)] >= invThr):
            greTh = invImage(greTh)
        ret, bluTh = cv2.threshold(blu, 0, 255, cv2.THRESH_OTSU)
        if (bluTh[10, (M-1)] >= invThr):
            bluTh = invImage(bluTh)

        ret, hueTh = cv2.threshold(hue, 0, 255, cv2.THRESH_OTSU)
        if (hueTh[10, (M-1)] >= invThr):
            hueTh = invImage(hueTh)
        ret, satTh = cv2.threshold(sat, 0, 255, cv2.THRESH_OTSU)
        if (satTh[10, (M-1)] >= invThr):
            satTh = invImage(satTh)
        ret, vvvTh = cv2.threshold(vvv, 0, 255, cv2.THRESH_OTSU)
        if (vvvTh[10, (M-1)] >= invThr):
            vvvTh = invImage(vvvTh)

        ret, lCompTh = cv2.threshold(lComp, 0, 255, cv2.THRESH_OTSU)
        if (lCompTh[10, (M-1)] >= invThr):
            lCompTh = invImage(lCompTh)
        ret, aCompTh = cv2.threshold(aComp, 0, 255, cv2.THRESH_OTSU)
        if (aCompTh[10, (M-1)] >= invThr):
            aCompTh = invImage(aCompTh)
        ret, bCompTh = cv2.threshold(bComp, 0, 255, cv2.THRESH_OTSU)
        if (bCompTh[10, (M-1)] >= invThr):
            bCompTh = invImage(bCompTh)
        
        rgbBWImg = np.hstack((redTh, greTh, bluTh))
        hsvBWImg = np.hstack((hueTh, satTh, vvvTh))
        labBWImg = np.hstack((lCompTh, aCompTh, bCompTh))

        imgBWGrid = np.vstack((rgbBWImg, hsvBWImg, labBWImg))

        cv2.imshow("Original image", frame0)
        cv2.imshow("Colour channels", imgGrid)
        cv2.imshow("Binary of colour channels", imgBWGrid)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap0.release()
            cv2.destroyAllWindows()
            break
