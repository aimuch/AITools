# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-04-14

import os
import shutil
import sys
import argparse
import random
from tqdm import tqdm

test_rate = 0.2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srctxt', help='text file', type=str)
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args


def pick(srctxt, srcimg):
    train_dir = "./train"
    test_dir = "./test"

    srctxt = os.path.abspath(srctxt)
    if srctxt[-1] == "/":
        srctxt = srctxt[:-1]

    # recreate folder
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # file_ = open(srctxt, 'r')
    # imglists = file_.readlines()
    # file_.close()
    txtlists = os.listdir(srctxt)
    test_num = int(len(txtlists)*test_rate)
    test_samples = random.sample(txtlists, test_num)

    for txt in tqdm(txtlists):
        txt_info = txt.split(".")
        # print(txt_info)
        if txt_info[-1] != "txt":
            continue
        
        txt_old_path = os.path.join(srctxt, txt.strip())
        # print(txt_old_path)
        
        img = txt.replace("txt", "jpg")
        img_old_path = os.path.join(srcimg, img)
        # print(img_old_path)
        
         
        if txt in test_samples:
            txt_new_path = os.path.join(os.path.join(test_dir, "labelTxt"), txt.strip())
            img_new_path = os.path.join(os.path.join(test_dir, "images"), img)
            if not os.path.exists(os.path.join(test_dir, "labelTxt")):
                os.makedirs(os.path.join(test_dir, "labelTxt"))
            if not os.path.exists(os.path.join(test_dir, "images")):
                os.makedirs(os.path.join(test_dir, "images"))
            shutil.copyfile(txt_old_path, txt_new_path)
            shutil.copyfile(img_old_path, img_new_path)
        else:
            txt_new_path = os.path.join(os.path.join(train_dir, "labelTxt"), txt.strip())
            img_new_path = os.path.join(os.path.join(train_dir, "images"), img)
            if not os.path.exists(os.path.join(train_dir, "labelTxt")):
                os.makedirs(os.path.join(train_dir, "labelTxt"))
            if not os.path.exists(os.path.join(train_dir, "images")):
                os.makedirs(os.path.join(train_dir, "images"))
            shutil.copyfile(txt_old_path, txt_new_path)
            shutil.copyfile(img_old_path, img_new_path)

if __name__ == '__main__':
    args = parse_args()
    srctxt = args.srctxt
    srcimg = args.srcimg
    
    if not os.path.exists(srctxt):
        print("Error !!! %s is not exists, please check the parameter"%srctxt)
        sys.exit(0)


    if not os.path.exists(srcimg):
        print("Error !!! %s is not exists, please check the parameter"%srcimg)
        sys.exit(0)

    pick(srctxt,  srcimg)
    print("Done!")
