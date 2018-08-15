# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-15

# This tool is used to create VOC-like txt file by reading image folder
# input: python create_txt_list.py "/home/andy/Data/img"
# output: 
#	./VOC/ImageSets/Main/train.txt
#	./VOC/ImageSets/Main/val.txt
#	./train.txt
#	./val.txt

import argparse
import os
import random
from os import listdir, getcwd
from os.path import join



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcdir', help='file directory', type=str)

    args = parser.parse_args()
    return args

def makelist(srcdir):
    folderPath = "./VOC/ImageSets/Main"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    main_train_txt = folderPath + "/train.txt"
    main_val_train = folderPath + "/val.txt"
    train_path_txt = "./train.txt"
    val_path_txt = "./val.txt"
    main_train_file=open(main_train_txt,'w+')   # 'w+' rewrite, 'a' add
    main_val_file=open(main_val_train,'w+') 
    train_file=open(train_path_txt,'w+')
    val_file=open(val_path_txt,'w+')

    filelist = os.listdir(srcdir)
    trainset = random.sample(filelist, int(len(filelist)*0.7))

    for file in filelist:
        file_name,file_extend=os.path.splitext(file)

        if file in trainset:
            main_train_file.write(file_name+'\n')
            train_file.write(srcdir+"/"+file+'\n')
        else:
            main_val_file.write(file_name+'\n')
            val_file.write(srcdir+"/"+file+'\n')

    main_train_file.close()
    main_val_file.close()
    train_file.close()
    val_file.close()


if __name__ == '__main__':
    args = parse_args()
    srcdir = args.srcdir
  
    if not os.path.exists(srcdir):
        print("Error !!! %s is not exists, please check the parameter")
        sys.exit(0)

    makelist(srcdir)
    print("Done!")
