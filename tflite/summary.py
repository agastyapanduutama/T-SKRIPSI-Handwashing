from tkinter import *
import numpy as np


def summariseTheResult(poseCount, totalFrames):
  jendela = Tk()
  jendela.title('Hasil Evaluasi Cuci Tangan')
  jendela.geometry("600x300+300+300")

  detikPerFrame = 1/15
  gerakanPctAcc = 0
  gerakanDurasiAcc = 0
  totalPresentasi = 0

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
    totalPresentasi = totalPresentasi + posePct

  gerakanPctAcc = round(gerakanPctAcc)

  if gerakanDurasiAcc >= 40:
      textColour = "black"
      # text = ("Durasi Cuci Tangan: %3.2f  sec | Persentasi : %3.2f %% \n dilakukan dengan benar") % (gerakanDurasiAcc, gerakanPctAcc)
      text = ("Durasi Cuci Tangan: %3.2f  sec |  dilakukan dengan benar | Persentasi %3.2f %%") % (
          gerakanDurasiAcc, totalPresentasi)
  elif gerakanDurasiAcc < 40:
      textColour = "red"
      text = ("Durasi Cuci Tangan: %3.2f  sec |  dilakukan teralu Singkat Minimal 40 Detik \n") % (
          gerakanDurasiAcc)

  lb0 = Label(jendela, text=text, fg=textColour, font=("Helvetica", 12))
  yPost = 35 + yPost
  lb0.place(x=20, y=yPost)
  jendela.mainloop()
