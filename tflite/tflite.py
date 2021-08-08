# Memasukan Library yang diperlukan
import numpy as np
import tensorflow as tf
import cv2
import time
from keras.preprocessing import image
from tkinter import *
from PIL import Image, ImageTk
import os

os.system("cls")
# Path untuk model dan video
pathModel = "/home/pandu/Documents/handwashing/model/tflite/handwashing.tflite"
pathVideo = "/home/pandu/Documents/handwashing/video/s_cuci_tangan11.mp4"

# deklarasi variable tensorflow lite dan load model
interpreter = tf.lite.Interpreter(model_path=pathModel)
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Untuk menampilkan FPS
pTime = 0

# Membuat label yang akan di prediksi sesuai nilianya
labels = ['0', '1', '2', '3', '4', '5', '6', '7']

# Membaca video atau webcam
# Untuk menggunakan webcam rubah parameter ke 0
cap = cv2.VideoCapture(pathVideo)


# Tampilan GUI
window = Tk()
window.title('Evaluasi Cuci Tangan')

# Kolom Kiri
leftFrame = Frame(window, width=200, height=200)
leftFrame.grid(row=0, column=0, padx=10, pady=2)


def text(nilai):
    for item in range(6):
        if nilai == item:
            color = "green"
        else:
            color = "black"

        item += 1
        Instruct = Label(leftFrame, fg=color, text="gerakan : " + str(item))
        Instruct.grid(row=item, column=0, padx=10, pady=2)


# Kolom kanan
video = Label(window, width=200, height=200)
video.grid(row=0, column=1, padx=10, pady=2)
# End GUI


def classification(channelRColor):
    # Start Prediksi Gambar #
    # interpreter.resize_tensor_input(input_details[0]['index'],[len(test_image), 224, 224, 3])
    interpreter.allocate_tensors()
    test_image = image.img_to_array(channelRColor)
    test_image = np.expand_dims(test_image, axis=0)

    input_data = np.array(test_image, dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Menampilkan Output dari hasil prediksi / klasifikasi
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print("Tingkat Akurasi : " + str(np.max(np.unique(output_data))))
    print("Label Terdeteksi :" + str(labels[np.argmax(output_data)]))
    nilai = (np.argmax(output_data))
    text(nilai)
    # End Prediksi gambar #


while True:
    # Membaca video
    ret, frame = cap.read()
    # Rotasikan gambar sesuai dengan rekomendasi dari kanan
    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    # Me resize image ke 224*224 kembali ke ukuran model
    inFrame = cv2.resize(frame, (150, 150))
    # inFrame = frame
    # cv2.imshow("frame", frame)

    cv2image = cv2.cvtColor(inFrame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video.config(image=imgtk)

    # Split warna pada video
    b, g, r = cv2.split(inFrame)
    # Meng treshold gambar atau merubah ke biner
    retR, tholdR = cv2.threshold(r, 50, 255, cv2.THRESH_BINARY)
    # Mengambil hasil treshold dan memasukannya ke array
    frameR = np.array(tholdR)

    # Mengambil channel Red
    channelRColor = cv2.merge([frameR, frameR, frameR])

    classification(channelRColor)
    window.update()

    # Menampilkan FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    print("fps :" + str(fps))

    if cv2.waitKey(25) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
