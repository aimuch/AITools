# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-8-15

# This tool is used to create txt file by reading image folder
# input: python create_txt_list.py "/home/andy/Data/"
# output: 
#	./train.txt
#	./val.txt

import argparse, os
from os import listdir, getcwd
from os.path import join



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('srcdir', help='file directory', type=str)

    args = parser.parse_args()
    return args

def makelist(srcdir):
    train_text = "./train.txt"
    val_text = "./val.txt"
    train_file=open(train_text,'w+')   # 'w+' rewrite, 'a' add
    val_file=open(val_text,'w+') 
    filelist = os.listdir(srcdir)

    trainNum = int(len(filelist)*0.7)
    mark = 0

    for file in filelist:
        file_name,file_extend=os.path.splitext(file)

        mark = mark + 1
        if mark < trainNum:
            train_file.write(file_name+'\n')
            print(file_name)
        else:
            val_file.write(file_name+'\n')

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
