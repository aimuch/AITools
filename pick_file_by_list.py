# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2021-08-04

# This tool is used to pick images by text list
# input: python3 remove_img_by_list.py "good.txt" "/home/andy/data/img"
# output:
# 	./pickedImgOut

import os
import shutil
import sys
import argparse
import collections
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('fileListTxt', help='text file', type=str)
    parser.add_argument('fileDir', help='images directory', type=str)
    parser.add_argument('ext', help='file ext', type=str)

    args = parser.parse_args()
    return args



def pick(fileListTxt, fileDir, ext):
    if "." in ext:
        ext = ext.split(".")[-1]
    pickedPath = "./pickedFilesOut"

    fileDir = os.path.abspath(fileDir)
    if fileDir[-1] == "/":
        fileDir = fileDir[:-1]

    # recreate folder
    if os.path.exists(pickedPath):
        shutil.rmtree(pickedPath)
    os.makedirs(pickedPath)

    file_ = open(fileListTxt, 'r')
    goodfileList = [f.strip().split(".")[0] for f in file_.readlines()]

    # print([item for item, count in collections.Counter(goodfileList).items() if count > 1])

    file_.close()

    for f in tqdm(goodfileList):
        f = f.strip()
        fileName = os.path.splitext(os.path.basename(f))[0]
        srcFile = os.path.join(fileDir, fileName + "." + ext)
        if not os.path.exists(srcFile):
            print(srcFile, " is not exists!")
            continue

        dstFile = os.path.join(pickedPath, fileName + "." + ext)

        shutil.copyfile(srcFile, dstFile)
    print("Path of picked images = ",os.path.abspath(pickedPath))

if __name__ == '__main__':
    args = parse_args()
    fileListTxt = args.fileListTxt
    fileDir = args.fileDir
    ext = args.ext

    if not os.path.exists(fileListTxt):
        print("Error !!! %s is not exists, please check the parameter"%fileListTxt)
        sys.exit(0)

    if not os.path.exists(fileDir):
        print("Error !!! %s is not exists, please check the parameter"%fileDir)
        sys.exit(0)

    pick(fileListTxt, fileDir, ext)
    print("Done!")
