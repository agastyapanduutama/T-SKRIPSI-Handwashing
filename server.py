import socket
import sys
import cv2
import pickle
import numpy as np
import struct  # new
import zlib
import os
import time
from keras.models import load_model
from keras.preprocessing import image
# Another File Python
import summary
from summary import summariseTheResult
import koneksi

koneksi.savelog

# Load Model
model = load_model("/home/pandu/Documents/eksperimen/model/16jun21.h5")
os.system("clear")

# Set Connection
HOST = 'localhost'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
# End Set connection


totalFrames = 0
noAction = 0
labels = ['1', '2', '3', '4', '5', '6', 'Tidak ada gerakan']

poseCount = np.zeros(7, dtype=int)

notResponse = 0

def showJson(poseCount, totalFrames):
    hasil = {
        "NumPose": poseCount,
        "NumFrame": totalFrames
    }
    # print(poseCount)
    koneksi.saveHistory(poseCount, totalFrames)
    print("Berhasil memasukan ke database")
    print('close')
   

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        
        # If not receive data
        if len(data) < payload_size:
            notResponse += 1
            print(notResponse)
            print("tidak merespon")
            # if notResponse > 500:
            #     showJson(poseCount, totalFrames)
            #     break

        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Mengirim Pesan dari Several

    
    # Menerima Pesan dari klien
    # message = conn.recv(1024).decode("UTF-8")
    # print(message)




    # Predict Image
    test_image = image.img_to_array(frame)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    poseIdx = np.argmax(result, axis=1)

    print("Gerakan terdeteksi gerakan :" + str(labels[np.argmax(result)]))
    poseCount[poseIdx[0]] = poseCount[poseIdx[0]] + 1
    totalFrames += 1



    # If not action
    label = labels[np.argmax(result)]
    if label == "Tidak ada gerakan":
        print(noAction)
        noAction += 1
        if noAction > 50:
            showJson(poseCount, totalFrames)
            break
    else:
        noAction = 0

    cv2.imshow('ImageWindow', frame)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        showJson(poseCount, totalFrames)
        break




cv2.destroyAllWindows()
s.close()
conn.close()

# os.execv(__file__, sys.argv)
os.system("python3 /home/pandu/Documents/eksperimen/eksperimenClasify/testAnotherFile/server.py")
