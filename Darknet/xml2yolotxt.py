# -*- coding: utf-8 -*-
# Reference VOC scrips
# Author : Andy Liu
# last modify : 2020-03-21

# This tool is used to convert VOC xml format to YOLO V3 format
# And pick 80% for train, left for val
# input : python xml2txt.py "/home/andy/data/xml"   "/home/andy/data/img"
# output :
#       ./txt
#		./train.txt
#		./val.txt
#       ./trainAll.txt

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

classes = ["Car","Van","Bus","Truck","Train","Cyclist","Motocyclist",
            "Electric_cyclist","Tricyclist","Person","Person_sitting","Child",
            "Dog","Cat","Sheep","Cow","Pig","Other_animal"]
            
classesRemoved = ["lane", "License_plate"]

error_log = "./log.txt"

draw_path = "./draw_img"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml_dir', help='xml directory', type=str)
    if WITH_IMAGE:
        parser.add_argument('img_dir', help='image directory', type=str)

    args = parser.parse_args()
    return args

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = abs(box[1] - box[0]) #box[1] - box[0]
    h = abs(box[3] - box[2]) #box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_dir, img_dir):
    xml_dir = os.path.abspath(xml_dir)
    if xml_dir[-1] == "/":
        xml_dir = xml_dir[:-1]
    
    if WITH_IMAGE:
        img_dir = os.path.abspath(img_dir)
        if img_dir[-1] == "/":
            img_dir = img_dir[:-1]

    filelist = os.listdir(xml_dir)
    print("images num = ", len(filelist))

    trainnum = int(len(filelist)*0.8)
    trainset = random.sample(filelist, trainnum)

    txt_dir = "./txt"
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    txt_train_path = "./train.txt"
    txt_val_path = "./val.txt"
    
    if REWRITE:
        txt_train_list = open(txt_train_path, 'a+')
        txt_val_list = open(txt_val_path, 'a+')
        log_file = open(error_log, 'a+')
    else:
        txt_train_list = open(txt_train_path, 'w')
        txt_val_list = open(txt_val_path, 'w')
        log_file = open(error_log, 'w')

    for f in filelist:
        print(f + "-->start!")
        fileInfor = f.split(".")
        # xmlfile = fileInfor[0][:fileInfor[0].rfind("_")] + ".xml"
        xml_path = os.path.join(xml_dir, f)

        if not os.path.exists(xml_path):
            print(f, "is not exists!")
            log_file.write(f + "\n")
            continue

        out_file = open(txt_dir + "/" + fileInfor[0] + ".txt", 'w')
        
        imgfile = img_dir + "/" + fileInfor[0] + ".jpg"
        if not os.path.exists(imgfile):
            imgfile = img_dir + "/" + fileInfor[0] + ".png"
        if not os.path.exists(imgfile):
            print(imgfile, " is not exists!")
            log_file.write(imgfile + "\n")
            continue

        # Check whether the image is complete
        img = cv2.imread(imgfile)
        if img is None:
            print("%s can't read!"%imgfile)
            continue
        
        if not os.path.exists(draw_path):
            os.makedirs(draw_path)
        new_img = os.path.join(draw_path, os.path.basename(imgfile))
        #print("new_img", new_img)

        if f in trainset:
            txt_train_list.write(imgfile + '\n')
        else:
            txt_val_list.write(imgfile + '\n')

        dom = xml.dom.minidom.parse(xml_path)
        annotation = dom.documentElement
        xml_img = annotation.getElementsByTagName('filename')[0].childNodes[0].data
        if xml_img != os.path.basename(imgfile):
            continue
        img_size = annotation.getElementsByTagName('size')[0]
        w = int(img_size.getElementsByTagName("width")[0].childNodes[0].data)
        h = int(img_size.getElementsByTagName("height")[0].childNodes[0].data)
        for obj in annotation.getElementsByTagName('object'):
            label = obj.getElementsByTagName('name')[0].childNodes[0].data
            if label not in classes:
                continue
            for box in obj.getElementsByTagName('bndbox'):
                xtl = int(box.getElementsByTagName('xmin')[0].childNodes[0].data)
                ytl = int(box.getElementsByTagName('ymin')[0].childNodes[0].data)
                xbr = int(box.getElementsByTagName('xmax')[0].childNodes[0].data)
                ybr = int(box.getElementsByTagName('ymax')[0].childNodes[0].data)
                xtl = xtl if xtl > 0 else 0
                ytl = ytl if ytl > 0 else 0
                xbr = xbr if xbr < w else w
                ybr = ybr if ybr < h else h
                cv2.rectangle(img, (int(xbr), int(ybr)), (int(xtl), int(ytl)), (0, 0, 255))
                # print(label, xtl, ytl, xbr, ybr)
                label_id = classes.index(label)
                b = (float(xtl), float(xbr), float(ytl), float(ybr))
                bb = convert((w, h), b)
                out_file.write(str(label_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                # out_file.flush()
                cv2.rectangle(img, (xtl, ytl), (xbr, ybr), (255, 0, 0))

        cv2.imwrite(new_img, img)
    
    print("Path of txt folder = ", os.path.abspath(txt_dir))
    print("Path of train text = ", os.path.abspath(txt_train_path))
    print("Path of valid text = ", os.path.abspath(txt_val_path))

if __name__ == '__main__':
    args = parse_args()
    xml_dir = args.xml_dir
    if not os.path.exists(xml_dir):
        print("Error !!! %s is not exists, please check the parameter"%xml_dir)
        sys.exit(0)
    
    
    if WITH_IMAGE:
        img_dir = args.img_dir
        if not os.path.exists(img_dir):
            print("Error !!! %s is not exists, please check the parameter"%img_dir)
            sys.exit(0)
    else:
        img_dir = None

    convert_annotation(xml_dir, img_dir)
    print("Done!")
    os.system("cat train.txt val.txt > trainAll.txt")
    print("Path of all train text =", os.path.abspath("./trainAll.txt"))
