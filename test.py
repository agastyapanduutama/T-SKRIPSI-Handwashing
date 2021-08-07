import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

from keras.models import load_model
from keras.preprocessing import image

import time
import screeninfo
from tkinter import *
window = Tk()


def summariseTheResult(poseCount, totalFrames):
  window.title('Hasil Evaluasi Cuci Tangan')
  window.geometry("600x300+300+300")

  secondPerFrame = 1/30
  posePctAcc = 0
  poseDurationAcc = 0

  for idx in range(6):
    poseDuration = poseCount[idx]*secondPerFrame
    posePct = (poseCount[idx]/totalFrames)*100
    # print(posePct)

    idxStr = "{:2d}".format(idx)

    # if poseCount[idx] >= 10:
    if poseDuration >= 5:
      textColour = "black"
    else:
      textColour = "red"

    # print(idxStr)
    # if idxStr >= 6:
    #       print("he")
        

    text = ("Gerakan %s: Dilakukan selama : %3.2f detik | Persentasi : %3.2f %% \n") % (idxStr, poseDuration, posePct)
    lb0 = Label(window, text=text, fg=textColour, font=("Helvetica", 12))
    yPost = 20 + idx*25
    lb0.place(x=20, y=yPost)

    poseDurationAcc = poseDurationAcc + poseDuration
    posePctAcc = posePctAcc + posePct

  posePctAcc = round(posePctAcc)

  if poseDurationAcc >= 40:
      textColour = "black"
        # text = ("Durasi Cuci Tangan: %3.2f  sec | Persentasi : %3.2f %% \n dilakukan dengan benar") % (poseDurationAcc, posePctAcc)
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan dengan benar") % (poseDurationAcc)
  elif poseDurationAcc < 40:
      textColour = "red"
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan teralu Singkat Minimal 40 Detik \n dan setiap gerakan dilakukan minimal 8 Detik ") % (poseDurationAcc)
  

  lb0 = Label(window, text=text, fg=textColour, font=("Helvetica", 12))
  yPost = 35 + yPost
  lb0.place(x=20, y=yPost)


# saveVideo = False
model = load_model("/home/pandu/Documents/eksperimen/model/16jun21.h5")
# model.summary()
os.system("clear")
 
## Video Part
videoPath = "/home/pandu/Documents/eksperimen/video/"
videoFile = "barujon.mp4"

cap = cv2.VideoCapture(videoPath+videoFile)
# url = "http://192.168.1.3:4747/video?640x480"
# cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture(url)


totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(totalFrames)
totalFrames = 0

frameVideo = cap.get(cv2.CAP_PROP_FRAME_COUNT)


frameIdx = 0
ratio = 0.5
pTime = 0

ret, frame0 = cap.read()

M = frame0.shape[0]
N = frame0.shape[1]

M = int(ratio*M)
N = int(ratio*N)

screen = screeninfo.get_monitors()[0]

noAction = 0
labels = ['1', '2', '3', '4' ,'5', '6', 'Tidak ada gerakan']

poseCount = np.zeros(7, dtype=int)

while True:
# while(True) and (frameIdx < (frameVideo-1)):
    ret, frame0 = cap.read()
    # time.sleep(00.09)
    # pct = (frameIdx/totalFrames)*100
    pct = frameIdx
    frame0 = cv2.rotate(frame0, cv2.ROTATE_180)
    # frame0 = cv2.rotate(frame0, cv2.ROTATE_90_CLOCKWISE)
    # frame0 = cv2.rotate(frame0, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame0 = frame0

    M = frame0.shape[0]
    N = frame0.shape[1]

    mR = 96
    nR = 96

    frame = cv2.resize(frame0, (int(ratio*N), int(ratio*M)))

    #out.write(frame)

    inFrame = cv2.resize(frame0, (nR, mR))

    # RGB Color
    b, g, r = cv2.split(inFrame)
    retR, tholdR = cv2.threshold(r, 50, 255, cv2.THRESH_BINARY)
    frameR = np.array(tholdR)
    cv2.imshow('Treshold Channel R color', frameR)


    # HSV Color
    hsvImg = cv2.cvtColor(inFrame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsvImg)
    retHSV, tholdHSV = cv2.threshold(h, 50, 255, cv2.THRESH_BINARY)
    frameHSV = np.array(tholdHSV)
    # Convert Color
    convertHSV = (255-frameHSV)
    # cv2.imshow('Treshold Channel H Color', convertHSV)


    # RGB
    rgbFrame = cv2.merge([frameR, frameR, frameR])

    # HSV
    hsvFrame = cv2.merge([convertHSV, convertHSV, convertHSV])

    test_image = image.img_to_array(rgbFrame)
    test_image = np.expand_dims(test_image, axis=0)

    result = model.predict(test_image)

    label = labels[np.argmax(result)]
    if label == "Tidak ada gerakan":
        print(noAction)
        noAction += 1
        if noAction > 50:
              break
    else :
        noAction = 0
            
    poseIdx = np.argmax(result, axis=1)
    print("Gerakan terdeteksi gerakan :" + str(labels[np.argmax(result)]))
    poseCount[poseIdx[0]] = poseCount[poseIdx[0]] + 1

    frameIdxDisp = frameIdx + 10000
    frameIdxDispStr = str(frameIdxDisp)[1:]

    infoStr = "%2.2f" % (pct)
    infoStr = "Frame Ke: "+frameIdxDispStr +" Gerakan Ke: "+str(poseIdx[0])
    # print(infoStr)

    cv2.putText(frame0, infoStr, (10, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0, 0), 2)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame0, f'FPS: {int(fps)}', (120, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    # cv2.namedWindow("RGB Video", cv2.WND_PROP_FULLSCREEN)
    # cv2.moveWindow("RGB Video", screen.x - 1, screen.y - 1)
    # cv2.setWindowProperty("RGB Video", cv2.WND_PROP_FULLSCREEN,
    #                       cv2.WINDOW_FULLSCREEN)
    cv2.imshow("RGB Video", frame0)

    # if saveVideo == True:
    #   out.write(frame)

    totalFrames += 1

    frameIdx += 1

    if frameVideo > 200:
      if frameIdx+1  == frameVideo:
          break
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

summariseTheResult(poseCount, totalFrames)


window.mainloop()
cv2.destroyAllWindows()
