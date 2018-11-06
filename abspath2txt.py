# -*- coding: utf-8 -*-
# Author : Andy Liu
# Last modified: 2018-9-6

# This tool is used to convert image abs path into txt
# input: python abspath2txt.py "/home/andy/Data/img"
# output: 
#	./imgPath.txt


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
    txt = "./imgPath.txt"
    txtfile=open(txt,'w+')   # 'w+' rewrite, 'a' add

    filelist = os.listdir(srcdir)

    for file in filelist:
        file_name,file_extend=os.path.splitext(file)
        txtfile.write(srcdir+"/"+file+'\n')

    txtfile.close()

    print("Path of text = ",os.path.abspath(txt))

if __name__ == '__main__':
    args = parse_args()
    srcdir = args.srcdir
  
    if not os.path.exists(srcdir):
        print("Error !!! %s is not exists, please check the parameter"%srcdir)
        sys.exit(0)

    makelist(srcdir)
    print("Done!")
