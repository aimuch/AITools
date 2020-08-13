# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-08-13

# This tool is used to pick images by text list
# input: python3 remove_img_by_list.py "delete.txt" "/home/andy/data/img"
# output:
# 	./pickedImgOut

import os
import shutil
import sys
import argparse
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('delListTxt', help='text file', type=str)
    parser.add_argument('imgDir', help='images directory', type=str)

    args = parser.parse_args()
    return args



def pick(delListTxt, imgDir):
    pickedImg_dir = "./pickedImgOut"

    imgDir = os.path.abspath(imgDir)
    if imgDir[-1] == "/":
        imgDir = imgDir[:-1]

    imglists = os.listdir(imgDir)

    # recreate folder
    if os.path.exists(pickedImg_dir):
        shutil.rmtree(pickedImg_dir)
    os.makedirs(pickedImg_dir)

    file_ = open(delListTxt, 'r')
    delimglists = [f.strip() for f in file_.readlines()]
    file_.close()

    for img in tqdm(imglists):
        img = img.strip()
        imgname = os.path.basename(img)
        if imgname in delimglists:
            continue

        src_img = os.path.join(imgDir, img)
        dst_img = os.path.join(pickedImg_dir, imgname)

        shutil.copyfile(src_img, dst_img)
    print("Path of picked images = ",os.path.abspath(pickedImg_dir))

if __name__ == '__main__':
    args = parse_args()
    delListTxt = args.delListTxt
    imgDir = args.imgDir

    if not os.path.exists(delListTxt):
        print("Error !!! %s is not exists, please check the parameter"%delListTxt)
        sys.exit(0)

    if not os.path.exists(imgDir):
        print("Error !!! %s is not exists, please check the parameter"%imgDir)
        sys.exit(0)

    pick(delListTxt, imgDir)
    print("Done!")
