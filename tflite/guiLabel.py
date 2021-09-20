# Only label

import cv2
from tkinter import *
from PIL import Image, ImageTk
from random import randrange
import time
import os
import numpy as np

os.system("clear")

window = Tk()
window.title('Evaluasi Cuci Tangan')

# FPS Yang didapat pada Perangkat
pTime = 0

# Hasil Evaluasi Cuci Tangan
def summariseTheResult(poseCount, totalFrames):
  jendela = Tk()
  jendela.title('Hasil Evaluasi Cuci Tangan')
  jendela.geometry("600x300+300+300")

  detikPerFrame = 1/15
  gerakanPctAcc = 0
  gerakanDurasiAcc = 0

  for idx in range(6):
    poseDuration = poseCount[idx]*detikPerFrame
    posePct = (poseCount[idx]/totalFrames)*100

    idxStr = "{:2d}".format(idx)

    # Jika gerakan lebih dari 5 detik maka gerakan dianggap bagus
    if poseDuration >= 5:
      textColour = "black"
    else:
      textColour = "red"

    text = ("Gerakan %s: Dilakukan selama : %3.2f detik | Persentasi : %3.2f %% \n") % (
        idxStr, poseDuration, posePct)
    lb0 = Label(jendela, text=text, fg=textColour, font=("Helvetica", 12))
    yPost = 20 + idx*25
    lb0.place(x=20, y=yPost)

    gerakanDurasiAcc = gerakanDurasiAcc + poseDuration
    gerakanPctAcc = gerakanPctAcc + posePct

  gerakanPctAcc = round(gerakanPctAcc)

  if gerakanDurasiAcc >= 40:
      textColour = "black"
      # text = ("Durasi Cuci Tangan: %3.2f  sec | Persentasi : %3.2f %% \n dilakukan dengan benar") % (gerakanDurasiAcc, gerakanPctAcc)
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan dengan benar") % (
          gerakanDurasiAcc)
  elif gerakanDurasiAcc < 40:
      textColour = "red"
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan teralu Singkat Minimal 40 Detik \n") % (gerakanDurasiAcc)

  lb0 = Label(jendela, text=text, fg=textColour, font=("Helvetica", 12))
  yPost = 35 + yPost
  lb0.place(x=20, y=yPost)
  jendela.mainloop()

# Put text in opencv
def textCv(nilai, gerakan):
    totalDurasiGerakan = 0
    secondPerFrame = 1/15

    for item in range(6):
        item += 1

        if nilai == item:
            color = 9,255,0
        else:
            color = 0,0,0

        durasiGerakan = gerakan[item]*secondPerFrame
        yPost = 20 + item*25
        durasi = round(durasiGerakan)
        cv2.putText(frame1, "gerakan ke: {}, Durasi : {}".format(item, durasi),(20, yPost), cv2.FONT_HERSHEY_PLAIN, 1, (color), 0)
    
        totalDurasiGerakan = totalDurasiGerakan + durasiGerakan

    cv2.putText(frame1, "Total Durasi Gerakan: {}".format(totalDurasiGerakan),(20, 200), cv2.FONT_HERSHEY_PLAIN, 1, (color), 0)

# Kolom kanan
# video = Label(window, width=250, height=250)
# video.grid(row=0, column=1, padx=10, pady=2)
totalFrames = 0

labelGerakan = Label(window, width=250, height=250)
labelGerakan.grid(row=0, column=0, padx=10, pady=2)

gerakan = np.zeros(7, dtype=int)
frameIdx = 0

# Path Video
vid = cv2.VideoCapture("C:\\Users\\Pandu\\Documents\\python\\video\\gerakan1.mp4")
frameVideo = vid.get(cv2.CAP_PROP_FRAME_COUNT)
print(frameVideo)

# while(True):
while(True) and (frameIdx < (frameVideo-1)):
    ret, frame = vid.read()  # Reads the video
    frame = cv2.resize(frame, (224, 224))
    
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    img = cv2.imread(
        "C:\\Users\\Pandu\\Documents\\python\\T-SKRIPSI-Handwashing\\assets\\abu.png", cv2.IMREAD_COLOR)
    frameNa = cv2.resize(img, (250,250))
    frame1 = frameNa

    nilai = randrange(7)
    nilai = 1
    hasil = np.array(list(str(nilai),), dtype=int)
    gerakan[hasil[0]] = gerakan[hasil[0]] + 1

    textCv(nilai, gerakan)

    # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # img = Image.fromarray(cv2image)
    # imgtk = ImageTk.PhotoImage(image=img)
    # video.config(image=imgtk)
    
    cv2imageNa = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGBA)
    imgNa = Image.fromarray(cv2imageNa)
    imgtkNa = ImageTk.PhotoImage(image=imgNa)
    labelGerakan.config(image=imgtkNa)

    totalFrames += 1

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    print("fps :" + str(round(fps)))

    frameIdx +=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    window.update()

vid.release()
cv2.destroyAllWindows()
window.destroy()


# summariseTheResult(gerakan, totalFrames)
# window.mainloop()
