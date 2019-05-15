# -*- coding: utf-8 -*-
### Author : Andy
### Last modified : 2019-05-15
### This tool is used to split videos into images(video_folder/video.h264)
### ----------------EXAMPLE-------------------
###  python3 video2pic.py \
###  		home/andy/data/train/video_folder \
###			home/andy/data/train/output_folder --interval 10  --waitTime 5

### -----------------Video Folder Tree---------------------
### The tree of video_folders: 
###                             video_folder:
###                               -- video1.avi
###                               -- video2.avi
###                               -- video3.avi

import os
import cv2
import sys
import shutil
import argparse


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('video_dir', help='video files directory', type=str)
  parser.add_argument('output_dir', help='output images directory ', type=str)
  parser.add_argument('--interval', help='take one in every interval frames', default=10, type=int)
  parser.add_argument('--waitTime', help='image display wait time', default=5, type=int)

  args = parser.parse_args()
  return args

def video2pic(video_path, output_dir, interval, waitTime):
  # folder_info = os.path.split(video_path)    # [文件夹, 视频]
  video_name = os.path.basename(video_path)  # video.avi
  video_infor = video_name.split(".")       # [video, avi]
  # print(folder_info)
  # print(video_name)
  # print(video_infor)

  ## set dst video folder
  output_folder = os.path.join(output_dir, video_infor[0])
  if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
  os.makedirs(output_folder)


  if video_infor[-1] != "h264" and video_infor[-1] != "mkv" and video_infor[-1] != "mp4" and video_infor[-1] != "avi":
    print("文件夹下有非视频文件，请检查！")
    return

  cap = cv2.VideoCapture(video_path)
  fps = cap.get(5)   # CV_CAP_PROP_FPS
  print("Frame per second : %s , interval : %s"%(fps, interval))

  retval, frame = cap.read()
  frame_num = 0
  count = 0

  while retval:
    if frame_num%interval == 0:
      count += 1
      pic_name = str(count).zfill(5) + ".jpeg"
      pic_path = os.path.join(output_folder, pic_name)

      cv2.imwrite(pic_path, frame)
      win = cv2.namedWindow('Clip Show', flags=cv2.WINDOW_AUTOSIZE)
      cv2.imshow('Clip Show', frame)
      cv2.waitKey(waitTime)
    frame_num +=1
    retval, frame = cap.read()

  cv2.destroyAllWindows()
  cap.release()
  
  print(video_path, " done!")


if __name__ == '__main__':
  args = parse_args()

  video_dir = args.video_dir
  output_dir = args.output_dir
  interval = args.interval
  waitTime = args.waitTime

  if not os.path.exists(video_dir):
    print("Error !!! %s is not exists, please check the parameter"%video_dir)
    sys.exit(0)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Create video folder: ", output_dir)
  
  video_list = os.listdir(video_dir)
  video_num = len(video_list)
  for i, video in enumerate(os.listdir(video_dir)):
    video_path = os.path.join(video_dir, video)
    print(">>> {}/{}".format((i+1), video_num), end=", ")
    video2pic(video_path, output_dir, interval, waitTime)
