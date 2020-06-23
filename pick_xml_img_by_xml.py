# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-10

# This tool is used to pick xml and image from the some folder
# This file should put on the same path with the folder
# input: pick_xml_img_by_xml.py  ./xml ./img
# output:
# 	./pickedXml
# 	./pickedImg

import os
import shutil
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('xmldir', help='xml file directory', type=str)
    parser.add_argument('imgdir', help='image file directory', type=str)

    args = parser.parse_args()
    return args



def pick(xmldir, imgdir):
    xmldir = os.path.abspath(xmldir)
    if xmldir[-1] == "/":
        xmldir = xmldir[:-1]
    imgdir = os.path.abspath(imgdir)
    if imgdir[-1] == "/":
        imgdir = imgdir[:-1]

    pickedXml_dir = "./pickedXml"
    pickedImg_dir = "./pickedImg"
    # recreate folder
    if os.path.exists(pickedXml_dir):
        shutil.rmtree(pickedXml_dir)
    os.makedirs(pickedXml_dir) 

    if os.path.exists(pickedImg_dir):
        shutil.rmtree(pickedImg_dir)
    os.makedirs(pickedImg_dir)

    xmllist = os.listdir(xmldir)

    for file in xmllist:
        print(file + "-->start!")
        fileInfor = file.split(".")
        if fileInfor[-1] != "xml":
            continue
        
        src_img = os.path.join(imgdir, fileInfor[0] + ".jpg")
        dst_img = os.path.join(pickedImg_dir, fileInfor[0] + ".jpg")
        if not os.path.exists(src_img):
            src_img = os.path.join(imgdir, fileInfor[0] + ".png")
            dst_img = os.path.join(pickedImg_dir, fileInfor[0] + ".png")
        if not os.path.exists(src_img):
            print(os.path.basename(src_img), " is not exits!")
            continue

        src_xml = os.path.join(xmldir, fileInfor[0] + ".xml")
        dst_xml = os.path.join(pickedXml_dir, fileInfor[0] + ".xml")
		
        shutil.copyfile(src_xml, dst_xml)
        shutil.copyfile(src_img, dst_img)
    print("Path of picked xmls = ",os.path.abspath(pickedXml_dir))
    print("Path of picked images = ",os.path.abspath(pickedImg_dir))

if __name__ == '__main__':
    print("Pick images and xml by xml")
    args = parse_args()
    xmldir = args.xmldir
    imgdir = args.imgdir

    if not os.path.exists(xmldir):
        print("Error !!! %s is not exists, please check the parameter"%xmldir)
        sys.exit(0)
    if not os.path.exists(imgdir):
        print("Error !!! %s is not exists, please check the parameter"%imgdir)
        sys.exit(0)

    pick(xmldir, imgdir)
    print("Done!")
