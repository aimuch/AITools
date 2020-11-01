# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-11-01

import os
import shutil
import sys
import argparse
import random
from tqdm import tqdm

val_rate = 0.2

train_img = "./train_img"
train_label = "./train_label"
val_img = "./val_img"
val_label = "./val_label"
if os.path.exists(train_img):
        shutil.rmtree(train_img)
os.makedirs(train_img)

if os.path.exists(train_label):
        shutil.rmtree(train_label)
os.makedirs(train_label)

if os.path.exists(val_img):
        shutil.rmtree(val_img)
os.makedirs(val_img)

if os.path.exists(val_label):
        shutil.rmtree(val_label)
os.makedirs(val_label)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srclabel', help='label directory', type=str)
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args


def pick(srclabel, srcimg):
    srclabel = os.path.abspath(srclabel)
    if srclabel[-1] == "/":
        srclabel = srclabel[:-1]

    labellists = os.listdir(srclabel)
    random.shuffle(labellists)
    val_num = int(len(labellists)*val_rate)
    # val_num = 800
    valset = random.sample(labellists, val_num)


    for label in tqdm(labellists):
        label_info = label.split(".")
        if label_info[-1] != "xml":
            if label_info[-1] != "txt":
                continue

        label_path = os.path.join(srclabel, label)
        img_path = os.path.join(srcimg, label_info[0]+".jpg")
        if(not os.path.exists(img_path)):
            img_path = os.path.join(srcimg, label_info[0]+".png")
        if label in valset:
            label_path_dst = os.path.join(val_label, os.path.basename(label_path))
            img_path_dst = os.path.join(val_img, os.path.basename(img_path))
            shutil.copyfile(label_path, label_path_dst)
            shutil.copyfile(img_path, img_path_dst)
        else:
            label_path_dst = os.path.join(train_label, os.path.basename(label_path))
            img_path_dst = os.path.join(train_img, os.path.basename(img_path))
            shutil.copyfile(label_path, label_path_dst)
            shutil.copyfile(img_path, img_path_dst)

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
