# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2021-01-20

import os
import shutil
import sys
import argparse
import random

matched_list_path = "./match_list.txt"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcImgPath', type=str, help='src image directory')
    parser.add_argument('--dstImgPath', type=str, default='./rename_img' , help='dst image directory')
    parser.add_argument('--matchedListPath', type=str, default='./match_list.txt' , help='matched list file path')

    args = parser.parse_args()
    return args


def rename(srcPath, dstPath, matchedListPath):
    src_list = []
    dst_list = []
    print(matchedListPath)
    srcList = os.listdir(srcPath)
    outputFile = open(matchedListPath,'w+')
    for i, f in enumerate(srcList):
        fileInfo = f.split(".")
        srcFilePath = os.path.join(srcPath, f)
        dstFilePath = os.path.join(dstPath, str(i)+"."+fileInfo[-1])
        shutil.copyfile(srcFilePath, dstFilePath)
        outputFile.write(f"{i},{f}\n")

    outputFile.close()


if __name__ == '__main__':
    args = parse_args()
    srcImgPath = args.srcImgPath
    dstImgPath = args.dstImgPath
    matchedListPath = args.matchedListPath

    if not os.path.exists(srcImgPath):
        print("Error !!! %s is not exists, please check the parameter"%srcImgPath)
        sys.exit(0)
    if not os.path.exists(dstImgPath):
        os.makedirs(dstImgPath)
        print("Warning !!! %s is not exists, using the default path: ./rename_img"%dstImgPath)
        # sys.exit(0)
    if not os.path.exists(matchedListPath):
        print("Warning !!! %s is not exists, using the default path: ./match_list.txt"%matchedListPath)
        # sys.exit(0)

    rename(srcImgPath, dstImgPath, matchedListPath)
    print("Done!")