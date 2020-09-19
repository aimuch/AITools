# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-06-15

import os
import shutil
import sys
import argparse
import random
from tqdm import tqdm

val_rate = 0.8

train_img = "./train_img"
train_xml = "./train_xml"
val_img = "./val_img"
val_xml = "./val_xml"
if os.path.exists(train_img):
        shutil.rmtree(train_img)
os.makedirs(train_img)

if os.path.exists(train_xml):
        shutil.rmtree(train_xml)
os.makedirs(train_xml)

if os.path.exists(val_img):
        shutil.rmtree(val_img)
os.makedirs(val_img)

if os.path.exists(val_xml):
        shutil.rmtree(val_xml)
os.makedirs(val_xml)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcxml', help='xml directory', type=str)
    parser.add_argument('srcimg', help='images directory', type=str)

    args = parser.parse_args()
    return args


def pick(srcxml, srcimg):
    srcxml = os.path.abspath(srcxml)
    if srcxml[-1] == "/":
        srcxml = srcxml[:-1]

    xmllists = os.listdir(srcxml)
    random.shuffle(xmllists)
    # val_num = int(len(xmllists)*val_rate)
    val_num = 800
    valset = random.sample(xmllists, val_num)


    for xml in tqdm(xmllists):
        xml_info = xml.split(".")
        if xml_info[-1] != "xml":
            continue

        xml_path = os.path.join(srcxml, xml)
        img_path = os.path.join(srcimg, xml_info[0]+".jpg")
        if(not os.path.exists(img_path)):
            img_path = os.path.join(srcimg, xml_info[0]+".png")
        if xml in valset:
            xml_path_dst = os.path.join(val_xml, os.path.basename(xml_path))
            img_path_dst = os.path.join(val_img, os.path.basename(img_path))
            shutil.copyfile(xml_path, xml_path_dst)
            shutil.copyfile(img_path, img_path_dst)
        else:
            xml_path_dst = os.path.join(train_xml, os.path.basename(xml_path))
            img_path_dst = os.path.join(train_img, os.path.basename(img_path))
            shutil.copyfile(xml_path, xml_path_dst)
            shutil.copyfile(img_path, img_path_dst)

if __name__ == '__main__':
    args = parse_args()
    srcxml = args.srcxml
    srcimg = args.srcimg

    if not os.path.exists(srcxml):
        print("Error !!! %s is not exists, please check the parameter"%srcxml)
        sys.exit(0)
    if not os.path.exists(srcimg):
        print("Error !!! %s is not exists, please check the parameter"%srcimg)
        sys.exit(0)

    pick(srcxml, srcimg)
    print("Done!")
