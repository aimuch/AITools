# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-15

# This tool is used to create VOC-like txt file by reading image folder
# input: python create_txt_list.py "/home/andy/Data/img"
# output: 
#	./train.txt
#	./val.txt

import argparse
import os,sys
import random
from os import listdir, getcwd
from os.path import join


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcdir', help='file directory', type=str)

    args = parser.parse_args()
    return args

def makelist(srcdir):
    srcdir = os.path.abspath(srcdir)
    if srcdir[-1] == "/":
        srcdir = srcdir[:-1]

    train_path_txt = "./train.txt"
    val_path_txt = "./val.txt"
    train_file=open(train_path_txt,'w+')   # 'w+' rewrite, 'a' add
    val_file=open(val_path_txt,'w+')

    filelist = os.listdir(srcdir)
    trainset = random.sample(filelist, int(len(filelist)*0.8))

    for file in filelist:
        file_name,file_extend=os.path.splitext(file)

        if file in trainset:
            train_file.write(srcdir+"/"+file+'\n')
        else:
            val_file.write(srcdir+"/"+file+'\n')

    train_file.close()
    val_file.close()

    print("Path of train text = ",os.path.abspath(train_path_txt))
    print("Path of valid text = ",os.path.abspath(val_path_txt))

if __name__ == '__main__':
    args = parse_args()
    srcdir = args.srcdir
  
    if not os.path.exists(srcdir):
        print("Error !!! %s is not exists, please check the parameter")
        sys.exit(0)

    makelist(srcdir)
    print("Done!")
