# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-11-01
"""
├── test
│   ├── ann
│   └── img
└── train
    ├── ann
    └── img
"""

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
    parser.add_argument('train', default='./train', help='train directory', type=str)
    parser.add_argument('val', default='./val', help='test directory', type=str)
    parser.add_argument('val_rate', default=0.2 help='val rate', type=float)

    args = parser.parse_args()
    return args


def pick(srclabel, srcimg, train_path, val_path, val_rate):
    srclabel = os.path.abspath(srclabel)
    if srclabel[-1] == "/":
        srclabel = srclabel[:-1]
    if srcimg[-1] == "/":
        srcimg = srcimg[:-1]

    train_path = os.path.abspath(train_path)
    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    os.makedirs(train_path)
    os.makedirs(os.path.join(train_path, 'img'))
    os.makedirs(os.path.join(train_path, 'ann'))

    val_path = os.path.abspath(val_path)
    if os.path.exists(val_path):
        shutil.rmtree(val_path)
    os.makedirs(val_path)
    os.makedirs(os.path.join(val_path, 'img'))
    os.makedirs(os.path.join(val_path, 'ann'))

    labellists = os.listdir(srclabel)
    random.shuffle(labellists)
    val_num = int(len(labellists)*val_rate)
    if val_num <= 50:
        val_num = 50
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
