# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2018-08-15

# This tool is used to convert VOC xml format to YOLO V3 format
# And pick 80% for train, left for val
# input : python xml2txt.py "/home/andy/data/xml"   "/home/andy/data/img"
# output :
#       ./txt
#		./train.txt
#		./val.txt
#       ./trainAll.txt

import xml.etree.ElementTree as ET
import random
import pickle
import os
import sys
import cv2
import argparse
from os import listdir, getcwd
from os.path import join

#sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["0","3","5"] #顺序要跟voc.names顺序一致
#classes = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]
#classes = ["person","rider","motor","car","bus","truck","ts","tl_g","tl_r","tl_y","tl_n","50","60","30","20","40","80","15","5"]#顺序要跟voc.names顺序一致

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dir', help='xml directory', type=str)
    parser.add_argument('img_dir', help='image directory', type=str)

    args = parser.parse_args()
    return args

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_dir, img_dir):
    xml_dir = os.path.abspath(xml_dir)
    if xml_dir[-1] == "/":
        xml_dir = xml_dir[:-1]
    img_dir = os.path.abspath(img_dir)
    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]
    print(xml_dir)
    print(img_dir)
    filelist = os.listdir(xml_dir)

    trainnum = int(len(filelist)*0.8)
    trainset = random.sample(filelist, trainnum)

    txt_dir = "./txt"
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    txt_train_path = "./train.txt"
    txt_val_path = "./val.txt"
    txt_train_list = open(txt_train_path, 'w')
    txt_val_list = open(txt_val_path, 'w')
    for file in filelist:
        print(file + "-->start!")
        fileInfor = file.split(".")
        in_file = open(xml_dir + "/" + file)
        out_file = open(txt_dir + "/" + fileInfor[0] + ".txt", 'w')
        
        imgfile = img_dir + "/" + fileInfor[0] + ".jpg"
        if not os.path.exists(imgfile):
            imgfile = img_dir + "/" + fileInfor[0] + ".png"
        if not os.path.exists(imgfile):
            continue

        # Check whether the image is complete
        img = cv2.imread(imgfile)
        if img is None:
            print("%s can't read!"%imgfile)
            continue


        if file in trainset:
            txt_train_list.write(imgfile + '\n')
        else:
            txt_val_list.write(imgfile + '\n')

        tree=ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('Difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult)==1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    
    print("Path of txt folder = ", os.path.abspath(txt_dir))
    print("Path of train text = ", os.path.abspath(txt_train_path))
    print("Path of valid text = ", os.path.abspath(txt_val_path))

if __name__ == '__main__':
    args = parse_args()
    xml_dir = args.xml_dir
    img_dir = args.img_dir

    if not os.path.exists(xml_dir):
        print("Error !!! %s is not exists, please check the parameter"%xml_dir)
        sys.exit(0)
    if not os.path.exists(img_dir):
        print("Error !!! %s is not exists, please check the parameter"%img_dir)
        sys.exit(0)

    convert_annotation(xml_dir, img_dir)
    print("Done!")
    os.system("cat train.txt val.txt > trainAll.txt")
    print("Path of all train text =", os.path.abspath("./trainAll.txt"))
