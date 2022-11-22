# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-09-25
# This tool is used to count numbers per class by text files
# input : python3 count_classes.py  /home/andy/data/txt_dir/
# output: ./classes_label_txt.txt
#         ./classes_index_txt.txt

import json
import os
import os.path
import shutil
import sys
import numpy as np
import argparse
from tqdm import tqdm


labelist = ["pedestrain", "cyclist", "others","car", "suv", "bus", "truck", "van", "forklift", "train", "motorbike", "bike", "tricycle", "other",
            "max_5", "max_10", "max_15", "max_20", "max_30", "max_40", "max_50", "max_60", "max_70", "max_80", "max_90", "max_100", "max_110", 
            "max_120", "max_130", "min_30","min_40","min_50", "min_60", "min_70", "min_80", "min_90", "min_100","end_20","end_30","end_40","end_50","end_60",
            "warning", "prohibitory", "indicative", "informational", "tourist", "others",
            "red_circle", "red_ahead", "red_left", "red_right", "red_back", "red_others","green_circle", "green_ahead", "green_left", "green_right", "green_back", "green_others",
            "yellow_circle", "yellow_ahead", "yellow_left", "yellow_right", "yellow_back", "yellow_others", 
            "other_circle", "other_ahead", "other_left", "other_right", "other_back","other_others"]

classes = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('txt_dir', help='Annotations directory', type=str)

    args = parser.parse_args()
    return args

 
def count_type(txt_dir):
    txt_dir = os.path.abspath(txt_dir)
    if txt_dir[-1] == "/":
        txt_dir = txt_dir[:-1]


    filelist = os.listdir(txt_dir)
    for file in tqdm(filelist):
        fileInfor = file.split(".")
        txtpath = txt_dir + "/" + file

        #txtfile = open(txtpath, "r")
        with open(txtpath, "r") as txtfile:
            lines = txtfile.read().split('\n')  # the last symbol is " "

            for line in lines:
                # remove the empty 
                if line == "":
                    continue

                obj = line.split(" ")[0] # get the object name
                if not obj in classes:
                    classes[obj] = 1
                else:
                    classes[obj] += 1

    classes_label_txt = open("classes_label_txt.txt", "w")
    classes_index_txt = open("classes_index_txt.txt", "w")
    ## method 1
    items=classes.items()
    for key, value in items:
        classes_label_txt.write(labelist[int(key)] + ": " + str(value) + "\n")
        classes_index_txt.write(key + ": " + str(value) + "\n")

    ## method 2
    # for key in classes:
    #     classes_label_txt.write(labelist[int(key)] + ": " + str(classes[key]) + "\n")
    #     classes_index_txt.write(key + ": " + str(classes[key]) + "\n")
    classes_index_txt.close()
    classes_label_txt.close()
    print("Path of classes label text = ", os.path.abspath("classes_label_txt.txt"))
    print("Path of classes index text = ", os.path.abspath("classes_index_txt.txt"))


if __name__ == '__main__':
    args = parse_args()
    txt_dir = args.txt_dir


    if not os.path.exists(txt_dir):
        print("Error !!! %s is not exists, please check the parameter"%txt_dir)
        sys.exit(0)

    count_type(txt_dir)
    print("Done!")
