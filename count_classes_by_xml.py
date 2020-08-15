# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2020-08-15

# input : python count_classes_by_xml.py "/home/andy/data/xml"

import xml.dom.minidom
import random
import pickle
import os
import sys
import cv2
import argparse
from os import listdir, getcwd
from os.path import join
from tqdm import tqdm

WITH_IMAGE = True
REWRITE = False

classes = ["car", "person"]
count_dict = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dir', help='xml directory', type=str)
    args = parser.parse_args()
    return args

def count_num(xml_dir):
    xml_dir = os.path.abspath(xml_dir)
    if xml_dir[-1] == "/":
        xml_dir = xml_dir[:-1]

    filelist = os.listdir(xml_dir)

    for f in tqdm(filelist):
        fileInfor = f.split(".")
        xml_path = os.path.join(xml_dir, f)

        dom = xml.dom.minidom.parse(xml_path)
        annotation = dom.documentElement
        xml_img = annotation.getElementsByTagName('path')[0].childNodes[0].data
        img_size = annotation.getElementsByTagName('size')[0]
        w = int(img_size.getElementsByTagName("width")[0].childNodes[0].data)
        h = int(img_size.getElementsByTagName("height")[0].childNodes[0].data)
        for obj in annotation.getElementsByTagName('object'):
            label = obj.getElementsByTagName('name')[0].childNodes[0].data
            if label not in classes:
                continue
            if label in count_dict:
                count_dict[label] += 1
            else:
                count_dict[label] = 1

    print(count_dict)


if __name__ == '__main__':
    args = parse_args()
    xml_dir = args.xml_dir
    if not os.path.exists(xml_dir):
        print("Error !!! %s is not exists, please check the parameter"%xml_dir)
        sys.exit(0)

    count_num(xml_dir)
    print("Done!")

