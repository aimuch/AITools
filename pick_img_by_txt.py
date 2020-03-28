# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-03-27
# This tool is used to pick image by txt
# input : python pick_img_by_txt.py  "/home/andy/data/txt_dir/"  "/home/andy/data/img_dir/" 
# |txt_dir
# |--1.txt
# |--2.txt
# 
# |img_dir
# |--1.png
# |--2.png
#
# output : 
#	./pickedImg

import os
import os.path
import shutil
import sys
import argparse
import cv2
# from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args

 
def pick(txt_dir, img_dir):
    dst_img = "./pickedImg"
    dst_txt = "./pickedTxt"
    txt_dir = os.path.abspath(txt_dir)
    img_dir = os.path.abspath(img_dir)
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]

    if not os.path.exists(dst_img):
        os.makedirs(dst_img)
    if not os.path.exists(dst_txt):
        os.makedirs(dst_txt)

    filelist = os.listdir(txt_dir)
    for file in filelist:
        print(file + "--->start!")
        txtpath = os.path.join(txt_dir, file)
        imgPath = os.path.join(img_dir, file.replace("txt", "jpg"))
        # print(txtpath)
        # print(imgPath)
        if not os.path.exists(imgPath):
            imgPath = os.path.join(imgPath, "iauto_01")
            if not os.path.exists(imgPath):
                continue
        imgArray = cv2.imread(imgPath)
        if imgArray is None:
            continue
        dst_txt_file = os.path.join(dst_txt, file)
        dst_img_file = os.path.join(dst_img, file.replace("txt", "jpg"))
        shutil.copyfile(txtpath, dst_txt_file)
        shutil.copyfile(imgPath, dst_img_file)
    print("Path of picked txt = ",os.path.abspath(dst_txt))
    print("Path of picked images = ",os.path.abspath(dst_img))

if __name__ == '__main__':
    args = parse_args()
    txt_dir = args.txt_dir
    img_dir = args.img_dir


    if not os.path.exists(txt_dir):
        print("Error !!! %s is not exists, please check the parameter"%txt_dir)
        sys.exit(0)
    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)
    

    pick(txt_dir,img_dir)
    print("Done!")
