import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

from keras.models import load_model
from keras.preprocessing import image

model = load_model("/home/pandu/Documents/handwashing/model/16jun21.h5")
os.system("clear")

# videoPath = "/home/pandu/Documents/eksperimen/video/"
# videoFile = "s_cuci_tangan11.mp4"

# cap = cv2.VideoCapture(videoPath+videoFile)


loadImage = cv2.imread("/home/pandu/Documents/handwashing/image/testImage.png")
cv2.imshow("image", loadImage)
inFrame = cv2.resize(loadImage, (96, 96))

test_image = image.img_to_array(inFrame)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)
print(result)


cv2.waitKey(0)
cv2.destroyAllWindows()
