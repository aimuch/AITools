# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-09-20

# This tool is used to pick some files into some folders
# input: python files2folders.py /home/andy/data/image_folder /home/andy/data/result_folder
# output:
# 	./result_folder

import os
import shutil
import sys
from tqdm import tqdm
import argparse

carNO = "re01"
date = "20180918"
cameraNO = "01"
per_num = 500

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcFolder', help='Source directory', type=str)
    parser.add_argument('dstFolder', help='Destination directory', type=str)

    args = parser.parse_args()
    return args

def pick(srcFolder, dstFolder):
    num = 1 # folder NO
    if srcFolder[-1] == "/":
        srcFolder = srcFolder[:-1]

    if dstFolder[-1] == "/":
        dstFolder = dstFolder[:-1]

    dstpath = dstFolder + "/" + carNO + "_"+ date + "_" + cameraNO + "_" + str(num).zfill(2)

    # recreate folder
    if os.path.exists(dstpath):
        shutil.rmtree(dstpath)
    os.makedirs(dstpath) 

    imglist = os.listdir(srcFolder)
    imgnum = len(imglist)

    for i in tqdm(range(imgnum)):
        if i%per_num == 0 and i !=0:
            num += 1
            dstpath = dstFolder + "/" + carNO + "_"+ date + "_" + cameraNO + "_" + str(num).zfill(2)
            if os.path.exists(dstpath):
                shutil.rmtree(dstpath)
            os.makedirs(dstpath)
        shutil.copyfile(srcFolder + "/" + imglist[i], dstpath + "/" + imglist[i])

if __name__ == '__main__':
    args = parse_args()
    srcFolder = args.srcFolder
    dstFolder = args.dstFolder
    
    if not os.path.exists(srcFolder):
        print("Error !!! %s is not exists, please check the parameter"%srcFolder)
        sys.exit(0)

    if not os.path.exists(dstFolder):
        print("Error !!! %s is not exists, please check the parameter"%dstFolder)
        sys.exit(0)

    pick(srcFolder, dstFolder)
    print("Done!")
