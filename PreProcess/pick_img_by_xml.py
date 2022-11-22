# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2020-05-22

# This tool is used to pick images by text list
# input: python3 pick_img_by_xml.py ./xml_folder ./img_folder ./dst_folder
# output:
# 	./pickedImg
#NOTE: xml file contains the image path
# |-- xml foler
#    |-- folder1
#        |--xml file
import os
import shutil
import sys
import argparse
import xml.dom.minidom
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcXML', help='XML file', type=str)
    parser.add_argument('srcIMG', help='images directory', type=str)
    parser.add_argument('dstFolder', help='target directory', type=str)


    args = parser.parse_args()
    return args


def pick(srcXML, srcIMG, dstFolder):
    pickedIMG_dir = os.path.join(dstFolder, "pickedIMG")
    pickedXML_dir = os.path.join(dstFolder, "pickedXML")

    srcXML = os.path.abspath(srcXML)
    if srcXML[-1] == "/":
        srcXML = srcXML[:-1]

    # recreate folder
    if not os.path.exists(pickedIMG_dir):
        os.makedirs(pickedIMG_dir)
    if not os.path.exists(pickedXML_dir):
        os.makedirs(pickedXML_dir)
    
    xmlFolderList = os.listdir(srcXML)

    for xmlFolder in xmlFolderList:
        xmlFolder = os.path.join(srcXML, xmlFolder)
        if not os.path.isdir(xmlFolder):
            continue
        print(">>>>>> ", os.path.basename(xmlFolder), " is processing ...")
        xmlList = os.listdir(xmlFolder)
        for xml_file in tqdm(xmlList):
            xml_path = os.path.join(xmlFolder, xml_file)
            xml_info = xml_path.split(".")
            # print(xml_info)
            if xml_info[-1] != "xml":
                continue
            
            dom = xml.dom.minidom.parse(xml_path)
            collection = dom.documentElement
            path = collection.getElementsByTagName('path')[0]
            img_path = path.childNodes[0].data
            img_path = os.path.join(srcIMG, img_path)
            img_name = os.path.basename(img_path)
            if not os.path.exists(img_path):
                print("IMG not found: ", img_name)
                continue

            img_new_folder = os.path.join(pickedIMG_dir, os.path.basename(xmlFolder))
            xml_new_folder = os.path.join(pickedXML_dir, os.path.basename(xmlFolder))
            if not os.path.exists(img_new_folder):
                os.makedirs(img_new_folder)
            if not os.path.exists(xml_new_folder):
                os.makedirs(xml_new_folder)
            img_new_path = os.path.join(img_new_folder, img_name)
            xml_new_path = os.path.join(xml_new_folder, xml_file)
            # print(">>>>>> ", img_name)
            
            # copy file
            shutil.copyfile(img_path, img_new_path)
            shutil.copyfile(xml_path, xml_new_path)
    print("Path of picked images = ", os.path.abspath(pickedIMG_dir))

if __name__ == '__main__':
    args = parse_args()
    srcXML = args.srcXML
    srcIMG = args.srcIMG
    dstFolder = args.dstFolder
    
    if not os.path.exists(srcXML):
        print("Error !!! %s is not exists, please check the parameter"%srcXML)
        sys.exit(0)


    if not os.path.exists(srcIMG):
        print("Error !!! %s is not exists, please check the parameter"%srcIMG)
        sys.exit(0)

    if not os.path.exists(dstFolder):
        print("Warning !!! %s is not exists, now has created "%dstFolder)

    pick(srcXML,  srcIMG, dstFolder)
    # pick("./xmlFolder",  "./imgfolder")
    print("Done!")
