# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2019-11-20
# 
# 首先用sh命令`ls ./file_foler | tee imglist.txt`生成文件名列表，或者自己提前准备文件名
# 根据文件名list重命名文件


import os
import shutil
import numpy as np
from tqdm import tqdm


txt_path = "./imglist.txt"
src_folder = "./npy_rgb"
dst_folder = "./rename_folder"
file_list = os.listdir(src_folder)

with open(txt_path) as txt:
    namelist = txt.readlines()
    for name_, f in tqdm(zip(namelist, file_list)):
        name = name_.split(".")[:-1]
        ext = f.split(".")[-1]
        dot = "."
        dst_name = dot.join(name) + "." + ext
        dst_path = os.path.join(dst_folder, dst_name)
        src_path = os.path.join(src_folder, f)
        shutil.copyfile(src_path, dst_path) 

