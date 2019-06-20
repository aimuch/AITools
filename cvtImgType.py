# -*- coding: utf-8 -*-

import os
import cv2
import sys
import shutil
import glob
from tqdm import tqdm

img_src_folder = "./trainID_874x774"
img_dst_folder = "./trainID"
dst_size = (513, 513)
dst_format = ".png"

if not os.path.exists(img_dst_folder):
    os.makedirs(img_dst_folder)

img_list = os.listdir(img_src_folder)
for img in tqdm(img_list):
    img_name = img.split(".")[0]
    img_src_path = os.path.join(img_src_folder, img)
    img_src = cv2.imread(img_src_path)
    # img_src = cv2.resize(img_src, dst_size, interpolation=cv2.INTER_LINEAR) # 原始图像
    img_src = cv2.resize(img_src, dst_size, interpolation=cv2.INTER_NEAREST) # trainID图像
    img_dst_path = os.path.join(img_dst_folder, img_name + dst_format)
    cv2.imwrite(img_dst_path, img_src)