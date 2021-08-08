import cv2
from tkinter import *
from PIL import Image, ImageTk
from random import randrange
import time
import os
import numpy as np

os.system("cls")
window = Tk()
window.title('Evaluasi Cuci Tangan')

label = Label(window, text="Label gerakan : ")
label.place(anchor='nw')

# Kolom Kiri
leftFrame = Frame(window, width=200, height=200)
leftFrame.grid(row=0, column=0, padx=10, pady=2)


def text(nilai):
    for item in range(6):
        item += 1

        if nilai == item:
            color = "green"
        else:
            color = "black"
        Instruct = Label(leftFrame, fg=color, text="gerakan : " + str(item))
        Instruct.grid(row=item, column=0, padx=10, pady=0)


# Kolom kanan
video = Label(window, width=200, height=200)
video.grid(row=0, column=1, padx=10, pady=2)

# label = Label(window, text="gerakan : ")
# label.place(relx = 0.5,rely=0.1,anchor = 'center')
# label.grid(row=0, column=1, padx=10, pady=0)

gerakan = np.zeros(7, dtype=int)
# print(gerakan)

vid = cv2.VideoCapture("/home/pandu/Documents/handwashing/video/s_cuci_tangan11.mp4")

while(True):
    ret, frame = vid.read()  # Reads the video
    frame = cv2.resize(frame, (224, 224))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video.config(image=imgtk)
    nilai = randrange(7)
    text(nilai)

    # gerakan += 1
    # print(gerakan)

    # gerakan[nilai[0]] = gerakan[nilai[0]] + 1

    hasil = np.array(list(str(nilai),), dtype=int)
    print(hasil)
    gerakan[hasil[0]] = gerakan[hasil[0]] + 1
    print(gerakan)

    # y = gerakan[poseIdx[0]]
    # gerakan[poseIdx[0]] + 1
    # print(gerakan)

    # print(gerakan)

    window.update()

vid.release()
cv2.destroyAllWindows()
