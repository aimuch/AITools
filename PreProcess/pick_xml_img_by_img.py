# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-9-07

# This tool is used to pick labels and image by the images
# input: python pick_all_xml_img.py "/home/andy/data/labels" "/home/andy/data/img" 
# output:
# 	./pickedLabel
# 	./pickedImg

import os
import shutil
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srclabel', help='labels directory', type=str)
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args



def pick(srclabel, srcimg):
    pickedLabel_dir = "./pickedLabel"
    pickedImg_dir = "./pickedImg"

    srclabel = os.path.abspath(srclabel)
    if srclabel[-1] == "/":
        srclabel = srclabel[:-1]

    srcimg = os.path.abspath(srcimg)
    if srcimg[-1] == "/":
        srcimg = srcimg[:-1]

    # recreate folder
    if os.path.exists(pickedLabel_dir):
        shutil.rmtree(pickedLabel_dir)
    os.makedirs(pickedLabel_dir) 

    if os.path.exists(pickedImg_dir):
        shutil.rmtree(pickedImg_dir)
    os.makedirs(pickedImg_dir)

    imglist = os.listdir(srcimg)

    for img in imglist:
        print(img + "-->start!")
        fileInfor = img.split(".")

        if fileInfor[-1] != "jpg" and fileInfor[-1] != "png":
            continue
        
        src_img = srcimg + "/" + img
        dst_img = pickedImg_dir + "/" + img

        src_label = srclabel + "/" + fileInfor[0] + ".xml"
        dst_label = pickedLabel_dir + "/" + fileInfor[0] + ".xml"

        if not os.path.exists(src_label):
            src_label = srclabel + "/" + fileInfor[0] + ".txt"
            dst_label = pickedLabel_dir + "/" + fileInfor[0] + ".txt"
        if not os.path.exists(src_label):
            continue
		
        shutil.copyfile(src_label, dst_label)
        shutil.copyfile(src_img, dst_img)
    print("Path of picked labels = ",os.path.abspath(pickedLabel_dir))
    print("Path of picked images = ",os.path.abspath(pickedImg_dir))

if __name__ == '__main__':
    args = parse_args()
    srclabel = args.srclabel
    srcimg = args.srcimg
    
    if not os.path.exists(srclabel):
        print("Error !!! %s is not exists, please check the parameter"%srclabel)
        sys.exit(0)

    if not os.path.exists(srcimg):
        print("Error !!! %s is not exists, please check the parameter"%srcimg)
        sys.exit(0)

    pick(srclabel, srcimg)
    print("Done!")
