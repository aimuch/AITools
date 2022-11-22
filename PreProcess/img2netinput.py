# -*- coding: utf-8 -*-

import os
import cv2
import shutil
import glob
import numpy as np
from tqdm import tqdm


IMAGE_SRC_PATH = './img'
IMAGE_DST_PATH = './net_img'
net_size = (224, 224)

IMAGE_SRC_PATH = os.path.abspath(IMAGE_SRC_PATH)
IMAGE_DST_PATH = os.path.abspath(IMAGE_DST_PATH)

if os.path.exists(IMAGE_DST_PATH):
    shutil.rmtree(IMAGE_DST_PATH)
os.makedirs(IMAGE_DST_PATH)

img_list = glob.glob(os.path.join(IMAGE_SRC_PATH, "*"))

for i in tqdm(img_list):
    img = cv2.imread(i)
    img = cv2.resize(img, net_size)
    cv2.imwrite(os.path.join(IMAGE_DST_PATH, os.path.basename(i)), img)