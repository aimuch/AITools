# -*- coding: utf-8 -*-

import os
import cv2
import sys
import shutil
import glob
from tqdm import tqdm

img_src_folder = "./img-first-1000"
img_dst_folder = "./img_png"

if not os.path.exists(img_dst_folder):
    os.makedirs(img_dst_folder)

img_list = os.listdir(img_src_folder)
for img in tqdm(img_list):
    img_name = img.split(".")[0]
    img_src_path = os.path.join(img_src_folder, img)
    img_src = cv2.imread(img_src_path)
    img_dst_path = os.path.join(img_dst_folder, img_name + ".png")
    cv2.imwrite(img_dst_path, img_src)