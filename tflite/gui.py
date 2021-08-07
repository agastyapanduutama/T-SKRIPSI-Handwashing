import cv2
from tkinter import *
from PIL import Image, ImageTk
from random import randrange
window = Tk()

# Kolom Kiri
leftFrame = Frame(window, width=250, height=250)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

Instruct = Label(leftFrame, fg="black")
Instruct.grid(row=1, column=0, padx=10, pady=2)

# Kolom kanan
video = Label(window, width=250, height=250)
video.grid(row=0, column=1, padx=10, pady=2)

vid = cv2.VideoCapture(0)

while(True):
    ret, frame = vid.read()  # Reads the video
    frame = cv2.resize(frame, (224, 224))
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video.config(image=imgtk)
    nilai = randrange(6)
    if nilai == 1:
        color = "green"
    else:
        color = "black"
    for item in range(6):
        Instruct.config(text="Label : " + str(nilai), fg=color)
    window.update()

vid.release()
cv2.destroyAllWindows()
