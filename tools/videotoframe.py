# Library
import cv2
import numpy as np

# Path
pathVideo = "/content/drive/MyDrive/skripsi/dataset/video/gerakan1.mp4"

# Read Video
cap = cv2.VideoCapture(pathVideo)

totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
frameIdx = 0

while True:
  ret, frame = cap.read()
  # Rotasi 90 derajat melawan arah jarum jam
  frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
  # Rubah ukuran gambar ke 200x200
  frame = cv2.resize(frame, (200, 200))

  frameIdx = frameIdx + 1 
  print(frameIdx)

  # Konversi gambar ke HSV
  hsvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsvImg)

  # Treshold Warna S pada HSV 
  retR, tholdR = cv2.threshold(s, 50, 255, cv2.THRESH_BINARY)
  frameR = np.array(tholdR)

  # Konversi Video Ke Gambar
  if (frameIdx != 0):
      NameFile = str(10000 + frameIdx)
      NameFile = NameFile[1:]+".jpg"
      # print(NameFile)

      # Buat file 
      cv2.imwrite("/content/gerakan1/"+NameFile, frameR)


  if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()