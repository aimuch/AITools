# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-06-15

import os
import shutil
import sys
import argparse
import random
from tqdm import tqdm

train_rate = 0.8

train_path_txt = "./train.txt"
val_path_txt = "./val.txt"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args



def pick(srcimg):
    srcimg = os.path.abspath(srcimg)
    if srcimg[-1] == "/":
        srcimg = srcimg[:-1]

    imglists = os.listdir(srcimg)
    train_num = int(len(imglists)*train_rate)
    trainset = random.sample(imglists, train_num)
    train_file =open(train_path_txt,'w+')
    val_file = open(val_path_txt,'w+')

    for img in tqdm(imglists):
        img_info = img.split(".")
        if img_info[-1] != "jpg":
            continue
        
        img_path = os.path.join(srcimg, img)
        if img in trainset:
            train_file.write(img_path+'\n')
        else:
            val_file.write(img_path+'\n')

if __name__ == '__main__':
    args = parse_args()
    srcimg = args.srcimg

    if not os.path.exists(srcimg):
        print("Error !!! %s is not exists, please check the parameter"%srcimg)
        sys.exit(0)

    pick(srcimg)
    print("Done!")
