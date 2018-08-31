# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-14
# This tool is used to remove empty text files frome txt folder
# input : python txt2xml.py "/home/andy/data/ann_dir" "/home/andy/data/img_dir"
# output:
#   ./dst_txt
#   ./dst_img


from xml.dom.minidom import Document
import os
import os.path
import shutil
import sys
import argparse
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ann_dir', help='Annotations directory', type=str)
    parser.add_argument('img_dir', help='Images directory', type=str)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    ann_dir = args.ann_dir
    img_dir = args.img_dir
    if not os.path.exists(ann_dir):
        print("Error !!! %s is not exists, please check the parameter"%ann_dir)
        sys.exit(0)
    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)

    dst_img = "./dst_img"
    dst_txt = "./dst_txt"
    if not os.path.exists(dst_img):
        os.mkdir(dst_img)
    if not os.path.exists(dst_txt):
        os.mkdir(dst_txt)

    if ann_dir[-1] == "/":
        ann_dir = ann_dir[:-1]
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]

    for files in os.walk(ann_dir): # os.walk return (root,dirs,files)
        for file in files[2]:
            print(file + "-->start!")
            fileInfor = os.path.splitext(file)
            img_name = fileInfor[0] + '.jpg'
            imgpath = img_dir + "/" + img_name
            if not os.path.exists(imgpath):
            	img_name = fileInfor[0] + '.png'
            	imgpath = img_dir + "/" + img_name
            if not os.path.exists(imgpath):
            	continue
            
            labelpath = ann_dir + "/" + file
            filelabel = open(labelpath, "r")
            lines = filelabel.read().split('\n')[:-1]
            if lines:
                shutil.copyfile(labelpath, dst_txt+'/'+file)
                shutil.copyfile(imgpath, dst_img+'/'+img_name)

            filelabel.close()
    print("Done!")
    print("Path of Text = ", os.path.abspath(dst_txt))
    print("Path of Image = ", os.path.abspath(dst_img))
