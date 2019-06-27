
import os
import cv2
import numpy as np
from tqdm import tqdm

'''
img1 = cv2.imread('000001.jpg')
img2 = cv2.imread('1.png')
res = cv2.addWeighted(img1, 0.6, img2, 0.4, 0)

cv2.imwrite('mix01.jpg',res)
'''
img_dir  = './APATEST07_img'
color_dir = './APATEST07_color'
mix_dir = './APATEST07_mix'

target = []
img_list = os.listdir(img_dir)
color_list = os.listdir(color_dir)

for i in tqdm(img_list):
    index = i.split(".")[0].split("_")[-1]
    img_path = os.path.join(img_dir, i)
    color_path = os.path.join(color_dir, "color_"+ index + ".jpg")
    # print(color_path)
    img1 = cv2.imread(img_path)
    img1_shape = np.shape(img1)
    img2 = cv2.imread(color_path)
    img2_shape = np.shape(img2)

    img_mix = np.zeros((600,1200,3), np.uint8)
    img_mix[:,0:600,:] = img1
    img_mix[:,600:,] = img2

    path_out = os.path.join(mix_dir, "mix_"+ index + ".png")
    # print(path_out)

    cv2.imwrite(path_out, img_mix)