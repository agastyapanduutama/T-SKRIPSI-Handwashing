import koneksi
from tkinter import *
from tkinter import messagebox
import numpy as np
window = Tk()
import sys
import os


def restartProgram():
    messagebox.showinfo("Informasi", "Memuat ulang Aplikasi")
    # os.system("python3 /home/pandu/Documents/eksperimen/eksperimenClasify/testAnotherFile/client.py")
    sys.exit()

def summariseTheResult(poseCount, totalFrames):
  window.title('Hasil Evaluasi Cuci Tangan')
  window.geometry("600x300+300+300")
  # window.attributes('-fullscreen', True)

  secondPerFrame = 1/30
  posePctAcc = 0
  poseDurationAcc = 0

  for idx in range(6):
    # print(int(poseCount[idx])+109)
    poseDuration = int(poseCount[idx])*secondPerFrame
    posePct = (int(poseCount[idx])/totalFrames)*100

    idxStr = "{:2d}".format(idx)

    # if poseCount[idx] >= 10:
    if poseDuration >= 5:
      textColour = "black"
    else:
      textColour = "red"

    # print(idxStr)
    # if idxStr >= 6:
    #       print("he")

    text = ("Gerakan %s: Dilakukan selama : %3.2f detik | Persentasi : %3.2f %% \n") % (
        idxStr, poseDuration, posePct)
    lb0 = Label(window, text=text, fg=textColour, font=("Helvetica", 12))
    yPost = 20 + idx*25
    lb0.place(x=20, y=yPost)

    poseDurationAcc = poseDurationAcc + poseDuration
    posePctAcc = posePctAcc + posePct

  posePctAcc = round(posePctAcc)

  if poseDurationAcc >= 40:
      textColour = "black"
      # text = ("Durasi Cuci Tangan: %3.2f  sec | Persentasi : %3.2f %% \n dilakukan dengan benar") % (poseDurationAcc, posePctAcc)
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan dengan benar") % (
          poseDurationAcc)
  elif poseDurationAcc < 40:
      textColour = "red"
      text = ("Durasi Cuci Tangan: %3.2f  sec |  \n dilakukan teralu Singkat Minimal 40 Detik \n dan setiap gerakan dilakukan minimal 8 Detik ") % (poseDurationAcc)

  lb0 = Label(window, text=text, fg=textColour, font=("Helvetica", 12))
  b = Button(window, text="Lakukan ulang", command=restartProgram, height=2, width=10)
  b.pack(side=BOTTOM)
  yPost = 35 + yPost
  lb0.place(x=20, y=yPost)
  window.mainloop()


def data():

  sql = 'SELECT poseCount, totalFrames FROM `t_summary` ORDER BY id DESC LIMIT 1'
  koneksi.cursor.execute(sql)
  result = koneksi.cursor.fetchall()
  if koneksi.cursor.rowcount > 0:
        for data in result:
          pose = data[0]
          total = data[1]

  else:
        print("Terjadi kesalahan")

  poseCount = pose
  totalFrames = int(total)
  kata = poseCount
  remove_characters = ["[", "]"]
  for item in remove_characters:
        kata = kata.replace(item, "")
  x = kata.split()
  
  summariseTheResult(x, totalFrames)

# print(data())

# isi = [192 197 181 206 235 263   0]


# poseCount = ['192','197','181','206','235','263','0']
# totalFrames = 875

# summariseTheResult(poseCount, totalFrames)

