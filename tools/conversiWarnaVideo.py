# Library
import numpy as np
import cv2
import os
import time

os.system("clear")

# Path file 
pathVideo = "C:\\Users\\Pandu\\Documents\\python\\video\\gerakan1.mp4"

# Read Image
cap = cv2.VideoCapture(pathVideo)


# If using Background Subtraction
backSub = cv2.createBackgroundSubtractorMOG2()
# backSub = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    # Rotate Image
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Resize Image

    frame = cv2.resize(frame, (200, 200))

    # Konversi Video Ke LAB
    labImg = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Konversi Video ke HSV
    hsvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Split warna RGB
    b, g, r = cv2.split(frame)
    
    # Split warna LAB
    l, a, b = cv2.split(labImgOri)
    
    
    # Split warna HSV
    h, s, v = cv2.split(hsvImgOri)

    # Gabungkan Gambar
    # oriMerge = np.hstack((frame, frame, frame))
    rgbMerge = np.hstack((R, G, Blue))
    labMerge = np.hstack((L, A, B))
    hsvMerge = np.hstack((H, S, V))

    # Merge Gambar RGB, LAB, HSV
    finMerge = np.vstack((rgbMerge, labMerge, hsvMerge))

    # Tampilkan Hasil Konversi Warna
    cv2.imshow("all", finMerge)

    # Konversi Warna ke Treshold
    retR, tholdR = cv2.threshold(finMerge, 50, 255, cv2.THRESH_BINARY)
    frameR = np.array(tholdR)
    cv2.imshow('Treshold Channel R color', frameR)

    # # Jika Menggunakan Background Subtraction 
    # fgMask = backSub.apply(finMerge)
    # cv2.imshow('backsub', fgMask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
