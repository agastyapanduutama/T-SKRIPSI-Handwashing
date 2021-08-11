######## Analisis Gerakan Evluasi Cuci Tangan #########
#
# Author: Agastya Pandu Satriya Utama, Dr. Esa Prakasa M.T.
# Deskripsi: 
# Program ini menggunakan Tensorflow lite untuk Mengklasifikasi gerakan Cuci Tangan Menggunakan Algoritma CNN
# untuk mengevaluasi hasil dari Gerakan Cuci Tangan, melalui Video
# 
# Saya memodifikasi dan mengembangkannya lebih lanjut

# Memasukan Library yang diperlukan
try:
    import numpy as np
    import tensorflow as tf
    import cv2
    import time
    from keras.preprocessing import image
    from tkinter import *
    from PIL import Image, ImageTk
    import os
except:
    print("beberapa lIbrary Tidak ditemukan")

os.system("clear")

# Path untuk model dan video
pathModel = "C:\\Users\\Pandu\\Documents\\python\\handwashing\\model\\handwashing.tflite"
pathVideo = "C:\\Users\\Pandu\\Documents\\python\\handwashing\\video\\s_cuci_tangan11.mp4"

# deklarasi variable tensorflow lite dan load model
interpreter = tf.lite.Interpreter(model_path=pathModel)
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Membaca video atau webcam # Untuk menggunakan webcam rubah parameter ke 0
# Referensi https://docs.opencv.org/4.5.2/dd/d43/tutorial_py_video_display.html
cap = cv2.VideoCapture(pathVideo)

# Membuat label yang akan di prediksi sesuai nilianya
labels = ['0', '1', '2', '3', '4', '5', '6', '7']

# Untuk menampilkan FPS
pTime = 0

gerakan = np.zeros(7, dtype=int)
totalFrames = 0

# Hasil Evaluasi Cuci Tangan
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
      text = ("Durasi Cuci Tangan: %3.2f  sec |  dilakukan dengan benar | Persentasi %3.2f %%" ) % (
          gerakanDurasiAcc, totalPresentasi)
  elif gerakanDurasiAcc < 40:
      textColour = "red"
      text = ("Durasi Cuci Tangan: %3.2f  sec |  dilakukan teralu Singkat Minimal 40 Detik \n") % (gerakanDurasiAcc)

  lb0 = Label(jendela, text=text, fg=textColour, font=("Helvetica", 12))
  yPost = 35 + yPost
  lb0.place(x=20, y=yPost)
  jendela.mainloop()

# Tampilan GUI
window = Tk()
window.title('Evaluasi Cuci Tangan')

# Kolom Kiri
leftFrame = Frame(window, width=200, height=200)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

# Put text in opencv
def textCv(nilai, gerakan):

    totalDurasiGerakan = 0
    secondPerFrame = 1/15

    for item in range(6):

        if nilai == item:
            color = 9,255,0
        else:
            color = 0,0,0
        
        durasiGerakan = gerakan[item]*secondPerFrame
        yPost = 20 + item*25
        durasi = round(durasiGerakan)
        cv2.putText(frame1, "gerakan ke: {}, Durasi : {}".format(item, durasi),(20, yPost), cv2.FONT_HERSHEY_PLAIN, 1, (color), 0)
        # cv2.putText(frame1, "sample",(20, yPost), cv2.FONT_HERSHEY_PLAIN, 1, (9,255,0), 0)
        totalDurasiGerakan = totalDurasiGerakan + durasiGerakan

    cv2.putText(frame1, "Total Durasi Gerakan: {}".format(totalDurasiGerakan),(20, 200), cv2.FONT_HERSHEY_PLAIN, 1, (color), 0)

# Kolom Kiri GUI
labelGerakan = Label(window, width=250, height=250)
labelGerakan.grid(row=0, column=0, padx=10, pady=2)

# Kolom kanan GUI
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
    hasil = np.array(list(str(nilai),), dtype=int)
    gerakan[hasil[0]] = gerakan[hasil[0]] + 1
    return nilai, gerakan
    # End Prediksi gambar #

# Jika tidak ada gerakan maka nilai akan bertambah dan akan menampilkan summary
noAction = 0

while True:
    try:
        # Membaca video
        ret, frame = cap.read()
        # Rotasikan gambar sesuai dengan rekomendasi dari kanan
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # Me resize image ke 224*224 kembali ke ukuran model
        inFrame = cv2.resize(frame, (150, 150))

        # Memasukan Video ke GUI Tkinter
        cv2image = cv2.cvtColor(inFrame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video.config(image=imgtk)

        # Prediksi Gerakan
        # Pisah warna pada video
        b, g, r = cv2.split(inFrame)
        # Meng treshold gambar atau merubah ke biner
        retR, tholdR = cv2.threshold(r, 50, 255, cv2.THRESH_BINARY)
        # Mengambil hasil treshold dan memasukannya ke array
        frameR = np.array(tholdR)
        # Merge channel Red
        channelRColor = cv2.merge([frameR, frameR, frameR])
        nilai, gerakan = classification(channelRColor)
        # End Prediksi Gerakan

        # Jika tidak ada gerakan
        if nilai == 6:
            noAction += 1
            if noAction == 30:
                break
        else:
            noAction = 0

        # Membuat Box Label Gerakan
        img = cv2.imread(
            "C:\\Users\\Pandu\\Documents\\python\\handwashing\\image\\abu.png", cv2.IMREAD_COLOR)
        frameNa = cv2.resize(img, (250, 250))
        frame1 = frameNa

        textCv(nilai, gerakan)

        cv2imageNa = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGBA)
        imgNa = Image.fromarray(cv2imageNa)
        imgtkNa = ImageTk.PhotoImage(image=imgNa)
        labelGerakan.config(image=imgtkNa)

        window.update()

        # Menampilkan FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        print("fps :" + str(fps))

        totalFrames += 1

    except cv2.error as e:
        break


cap.release()
cv2.destroyAllWindows()
window.destroy()
# Tampilkan Hasil Evaluasi
summariseTheResult(gerakan, totalFrames)
