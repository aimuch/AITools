# -*- coding: utf-8 -*-
'''
@Time          : 2020/11/09 11:06
@Author        : Andy
@File          : darknetTxt_1img1line.py
@Noice         :
@Modificattion :
    @Author    :
    @Time      :
    @Detail    :
'''

import os
import sys
import argparse
import shutil
from tqdm import tqdm


TRAIN_RATE = 0.8
TXT_PATH = "./new.txt"
ERROR_LOG = "./errorLog.txt"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('label_dir', help='label directory', type=str)
    parser.add_argument('img_dir', help='image directory', type=str)

    args = parser.parse_args()
    return args


def convert_annotation(label_dir, img_dir):
    '''
    image_path1 x1,y1,x2,y2,id x1,y1,x2,y2,id x1,y1,x2,y2,id ...
    image_path2 x1,y1,x2,y2,id x1,y1,x2,y2,id x1,y1,x2,y2,id ...
        @image_path : Image absolute path
        @x1,y1 : Coordinates of upper left corner
        @x2,y2 : Coordinates of the lower right corner
        @id : Object category
    '''
    label_dir = os.path.abspath(label_dir)
    if label_dir[-1] == "/":
        label_dir = label_dir[:-1]

    img_dir = os.path.abspath(img_dir)
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]

    labelList = os.listdir(label_dir)
    imgList = os.listdir(img_dir)
    imgNum = len(imgList)

    # print("images num = ", imgNum)

    # trainnum = int(labelList*TRAIN_RATE)
    # trainset = random.sample(labelList, trainnum)
    # txt_train_path =  os.path.join(os.path.dirname(label_dir), "train.txt")
    # txt_val_path =  os.path.join(os.path.dirname(label_dir), "val.txt")



    txt = open(TXT_PATH, 'w')
    log_file = open(ERROR_LOG, 'w')

    for f in labelList:
        print(f + "-->start!")
        labelInfor = f.split(".")
        labelPath = os.path.join(label_dir, f)

        if not os.path.exists(labelPath):
            print(labelPath, " is not exists!")
            log_file.write(labelPath + "\n")
            continue

        if labelInfor[-1] !="txt":
            print(labelPath, " is not txt file!")
            log_file.write(labelPath + "\n")
            continue

        imgPath = os.path.join(img_dir, f.replace("txt", "jpg"))
        if not os.path.exists(imgPath):
            imgPath = imgPath.replace("jpg", "png")
            if not os.path.exists(imgPath):
                print(imgPath, " is not exists!")
                log_file.write(labelPath + "\n")
                continue

        # txt.write(imgPath + " ")
        box_info = imgPath + " "
        with open(labelPath) as t:
            lines = t.readlines()
            for line in lines:
                box = line.strip().split(" ")
                box_info += box[1] + "," + box[2] + "," + box[3] + "," + box[4] + "," + box[0] + " "
                # txt.write(box[1] + "," + box[2] + "," + box[3] + "," + box[4] + "," + box[0] + " ")
            # txt.write("\n")
            txt.write(box_info.strip() + "\n")


    log_file.close()
    txt.close()
    print("\n")
    print("-------------------------------------- OUTPUT --------------------------------------")
    print("Path of txt file = ", os.path.abspath(TXT_PATH))
    print("Path of error log file = ", os.path.abspath(ERROR_LOG))
    print("------------------------------------------------------------------------------------")
    print("\n")

if __name__ == '__main__':
    # args = parse_args()
    # label_dir = args.label_dir
    # if not os.path.exists(label_dir):
    #     print("Error !!! %s is not exists, please check the parameter"%label_dir)
    #     sys.exit(0)

    # img_dir = args.img_dir
    # if not os.path.exists(img_dir):
    #     print("Error !!! %s is not exists, please check the parameter"%img_dir)
    #     sys.exit(0)

    label_dir = "./picked_txt"
    img_dir = "./picked_img"

    convert_annotation(label_dir, img_dir)
    print("Done!")
