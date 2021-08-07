import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import numpy as np
# from tensorflow.python import client
import summary
import errno
import os
# import koneksi
# import inspect


# Load Video
videoFile = "/home/pandu/Documents/eksperimen/video/s_cuci_tangan11.mp4"

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))
connection = client_socket.makefile('wb')


img_counter = 0
frameIdx = 0
resetConnection = 0

frameVideo = cam.get(cv2.CAP_PROP_FRAME_COUNT)
print(frameVideo)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
# while(True) and (frameIdx < (frameVideo-1)):
    ret, frame = cam.read()

    if ret:
        # Resize image
        mR = 96
        nR = 96
        inFrame = cv2.resize(frame, (nR, mR))

        # RGB Color Treshold
        b, g, r = cv2.split(inFrame)
        retR, tholdR = cv2.threshold(r, 50, 255, cv2.THRESH_BINARY)
        frameR = np.array(tholdR)
        cv2.imshow('Treshold Channel R color', frameR)
        frame = cv2.merge([frameR, frameR, frameR])

        result, frame = cv2.imencode('.jpg', frame, encode_param)
        # data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        
        img_counter += 1

        try:
            client_socket.sendall(struct.pack(">L", size) + data)
        except socket.error as e:
            print("Menghubungkan ke server")
            resetConnection += 1
            print(resetConnection)
            if resetConnection > 1:
                print("Request Time Out")
                summary.data()
                break
            time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        # summary.data()
        break
        # msg = client_socket.recv(1024)
        # while msg:
        #     print('Received:' + msg.decode())
        #     msg = client_socket.recv(1024)

        # while not msg:
        #     print("Please Wait")
        #     time.sleep(1)

        # break
        # message = client_socket.recv(1024).decode("UTF-8")
        # if message:
        #     print(message)
            
        # print("harap tunggu")
        # time.sleep(5)


cam.release()
cv2.destroyAllWindows()
# os.system("python3 /home/pandu/Documents/eksperimen/eksperimenClasify/testAnotherFile/client.py")
