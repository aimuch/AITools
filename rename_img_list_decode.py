# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2021-01-20

import os
import shutil
import sys
import argparse
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcImgPath', type=str, default='./rename_img_encode', help='src image directory')
    parser.add_argument('--dstImgPath', type=str, default='./rename_img_decode' , help='dst image directory')
    parser.add_argument('--srcTxtPath', type=str, default='./rename_txt_encode', help='src txt directory')
    parser.add_argument('--dstTxtPath', type=str, default='./rename_txt_decode' , help='dst txt directory')
    parser.add_argument('--matchedListPath', type=str, default='./match_list.txt' , help='matched list file path')

    args = parser.parse_args()
    return args


def rename(srcImgPath, dstImgPath, srcTxtPath, dstTxtPath, matchedListPath):
    src_list = []
    dst_list = []
    srcImgList = os.listdir(srcImgPath)
    srcTxtList = os.listdir(srcTxtPath)
    file_ = open(matchedListPath, 'r')
    lines = [f.strip() for f in file_.readlines()]
    file_.close()
    for line in lines:
        i, imgName = line.split(",")
        imgInfor = imgName.split(".")
        i_img = i+"."+imgInfor[-1]
        i_txt = i+".txt"
        if i_img not in srcImgList:
            print(f"{i_img} is not exists!")
            continue
        if i_txt not in srcTxtList:
            print(f"{i_txt} is not exists!")
            continue
        srcImgFilePath = os.path.join(srcImgPath, i_img)
        srcTxtFilePath = os.path.join(srcTxtPath, i_txt)
        dstImgFilePath = os.path.join(dstImgPath, imgName)
        dstTxtFilePath = os.path.join(dstTxtPath, imgName.split(".")[0]+".txt")
        shutil.copyfile(srcImgFilePath, dstImgFilePath)
        shutil.copyfile(srcTxtFilePath, dstTxtFilePath)

if __name__ == '__main__':
    args = parse_args()
    srcImgPath = args.srcImgPath
    dstImgPath = args.dstImgPath
    srcTxtPath = args.srcTxtPath
    dstTxtPath = args.dstTxtPath
    matchedListPath = args.matchedListPath

    if not os.path.exists(srcImgPath):
        print("Error !!! %s is not exists, please check the parameter"%srcImgPath)
        sys.exit(0)
    if not os.path.exists(dstImgPath):
        os.makedirs(dstImgPath)
        print("Warning !!! %s is not exists, using the default path: ./rename_img"%dstImgPath)
        # sys.exit(0)
    if not os.path.exists(srcTxtPath):
        print("Error !!! %s is not exists, please check the parameter"%srcTxtPath)
        sys.exit(0)
    if not os.path.exists(dstTxtPath):
        os.makedirs(dstTxtPath)
        print("Warning !!! %s is not exists, using the default path: ./rename_txt_decode"%dstTxtPath)
        # sys.exit(0)
    if not os.path.exists(matchedListPath):
        print("Warning !!! %s is not exists, using the default path: ./match_list.txt"%matchedListPath)
        # sys.exit(0)

    rename(srcImgPath, dstImgPath, srcTxtPath, dstTxtPath, matchedListPath)
    print("Done!")