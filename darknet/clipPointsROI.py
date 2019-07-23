# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2019-07-23

# This tool is used to clip images by reading txt labels
# input: python3 clipImg.py ./img ./txt ./dst
# output:
#	./dst/obj1
#	./dst/obj2

# The Label txt format:
# classNO center_x center_y width height

import argparse
import os
import sys
import random
import shutil
from glob import glob
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('imgDir', help='img directory', type=str)
    parser.add_argument('txtDir', help='label directory', type=str)
    parser.add_argument('dstDir', help='dst directory', type=str)

    args = parser.parse_args()
    return args

def saveROI(imgDir, txtDir, dstDir):
    imgDir = os.path.abspath(imgDir)
    txtDir = os.path.abspath(txtDir)
    dstDir = os.path.abspath(dstDir)
    if imgDir[-1] == "/":
        imgDir = imgDir[:-1]
    if txtDir[-1] == "/":
        txtDir = txtDir[:-1]
    if os.path.exists(dstDir):
        shutil.rmtree(dstDir)
    # recursive
    os.makedirs(dstDir)
    print(dstDir, " has been created!")


    imgList = os.listdir(imgDir)
    txtList = os.listdir(txtDir)
    # filelist = glob(os.path.join(imgDir, "*.jpg"))
    for img in imgList:
        if os.path.isdir(img):
            continue

        file_name, file_extend = os.path.splitext(img)
        imgPath = os.path.join(imgDir, img)
        txtPath = os.path.join(txtDir, file_name+".txt")
        if not os.path.exists(txtPath):
            print("Warning %s is not exits!!!!"%txtPath)
        print(imgPath)
        print(txtPath)
        imgArray = cv2.imread(imgPath)
        imgShape = imgArray.shape
        imgWidth = imgShape[1]
        imgHeight = imgShape[0]
        with open(txtPath, "r") as txt:
            lines = txt.read().split('\n')
            for i, line in enumerate(lines):
                if line is '' or line is ' ' or line is None:
                    continue
                lineInfo = line.split(" ")
                # print(lineInfo)
                obj = lineInfo[0]
                x = int(float(lineInfo[1])*imgWidth)
                y = int(float(lineInfo[2])*imgHeight)
                # w = int(float(lineInfo[3])*imgWidth)
                # h = int(float(lineInfo[4])*imgHeight)
                # left = x-int(w/2) if x-int(w/2)>0 else 0
                # right = x+int(w/2) if x+int(w/2)<imgHeight else imgHeight
                # top = y-int(h/2) if y-int(h/2)>0 else 0
                # bottom = y+int(h/2) if y+int(h/2)<imgHeight else imgHeight
                w = 46
                h = 46
                left = x-23 if x-23>0 else 0
                right = x+23 if x+23<imgWidth else imgWidth
                top = y-23 if y-23>0 else 0
                bottom = y+23 if y+23<imgHeight else imgHeight

                objDir = os.path.join(dstDir, obj)
                if not os.path.exists(objDir):
                    os.mkdir(objDir)
                roiPath = os.path.join(objDir, file_name+"_"+str(i)+".jpg")
                roiArray = imgArray[top:bottom, left:right, :]
                cv2.imwrite(roiPath, roiArray)



if __name__ == '__main__':
    args = parse_args()
    imgDir = args.imgDir
    txtDir = args.txtDir
    dstDir = args.dstDir

    if not os.path.exists(imgDir):
        print("Error !!! %s is not exists, please check the parameter"%imgDir)
        sys.exit(0)
    if not os.path.exists(txtDir):
        print("Error !!! %s is not exists, please check the parameter"%txtDir)
        sys.exit(0)
    if not os.path.exists(dstDir):
        print("Warning !!! %s is not exists, please check the parameter"%dstDir)

    saveROI(imgDir, txtDir, dstDir)
    print("Done!")
