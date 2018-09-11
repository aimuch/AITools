# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-9-11

# This tool is used to pick images by text list
# input: python3 pick_img_by_list.py "/home/andy/data/val.txt" "/home/andy/data/labels" "/home/andy/data/img" 
# output:
# 	./pickedLabel
# 	./pickedImg

import os
import shutil
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srctxt', help='text file', type=str)
    parser.add_argument('srclabel', help='labels directory', type=str)
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args



def pick(srctxt, srclabel, srcimg):
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

    file_ = open(srctxt, 'r')
    imglists = file_.readlines()
    file_.close()

    for img in imglists:
        img = img.strip()
        imgname = os.path.basename(img)
        print(imgname + " -->start!")
        fileInfor = imgname.split(".")
        
        dst_img = pickedImg_dir + "/" + imgname

        src_label = srclabel + "/" + fileInfor[0] + ".xml"
        dst_label = pickedLabel_dir + "/" + fileInfor[0] + ".xml"

        if not os.path.exists(src_label):
            src_label = srclabel + "/" + fileInfor[0] + ".txt"
            dst_label = pickedLabel_dir + "/" + fileInfor[0] + ".txt"

        if not os.path.exists(src_label):
            continue
		
        shutil.copyfile(src_label, dst_label)
        shutil.copyfile(img, dst_img)
    print("Path of picked labels = ",os.path.abspath(pickedLabel_dir))
    print("Path of picked images = ",os.path.abspath(pickedImg_dir))

if __name__ == '__main__':
    args = parse_args()
    srctxt = args.srctxt
    srclabel = args.srclabel
    srcimg = args.srcimg
    
    if not os.path.exists(srctxt):
        print("Error !!! %s is not exists, please check the parameter"%srctxt)
        sys.exit(0)

    if not os.path.exists(srclabel):
        print("Error !!! %s is not exists, please check the parameter"%srclabel)
        sys.exit(0)

    if not os.path.exists(srcimg):
        print("Error !!! %s is not exists, please check the parameter"%srcimg)
        sys.exit(0)

    pick(srctxt, srclabel, srcimg)
    print("Done!")
