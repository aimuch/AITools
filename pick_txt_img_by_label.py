# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-14
# This tool is used to pick .txt and image by label
# input : python pick_txt_img_by_label.py  "/home/andy/data/label_dir/"  "/home/andy/data/img_dir/" 
# output : 
#	./pickedLabel
#	./pickedImg

from xml.dom.minidom import Document
import os
import os.path
import shutil
import sys
import argparse
from PIL import Image


labelset = ["6"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args

 
def pick(txt_dir, img_dir):
    dst_label = "./pickedLabel"
    dst_img = "./pickedImg"
    txt_dir = os.path.abspath(txt_dir)
    img_dir = os.path.abspath(img_dir)
    if txt_dir[-1] == "/":
        txt_dir = txt_dir[:-1]
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]

    if not os.path.exists(dst_label):
        os.makedirs(dst_label)
    if not os.path.exists(dst_img):
        os.makedirs(dst_img)


    filelist = os.listdir(txt_dir)
    for file in filelist:
        print(file + "-->start!")
        fileInfor = file.split(".")
        txtpath = txt_dir + "/" + file
        txtfile = open(txtpath, "r")
        lines = txtfile.read().split('\n')[:-1] # the last symbol is " "
        for line in lines:
                obj = line.split(" ")[0]
                if not obj in labelset:
                    continue
                dst_label_file = dst_label + "/" + file
                srcimg = img_dir + "/" + fileInfor[0] + ".jpg"
                dst_img_file = dst_img + "/" + fileInfor[0] + ".jpg"
                if not os.path.exists(srcimg):
                    srcimg = img_dir + "/" + fileInfor[0] + ".png"
                    dst_img_file = dst_img + "/" + fileInfor[0] + ".png"

                if not os.path.exists(srcimg):
                    break

                shutil.copyfile(txtpath, dst_label_file)
                shutil.copyfile(srcimg, dst_img_file)
    print("Path of picked labels = ",os.path.abspath(dst_label))
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
