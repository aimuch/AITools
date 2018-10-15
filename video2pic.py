# -*- coding: utf-8 -*-
### Author : zyy
### Modified by : Andy 
### Last modified : 2018-09-19
### This tool is used to split videos into images(video_folders/video_folder/video.h264)
### ----------------EXAMPLE-------------------
###  python video2pic.py \
###  		home/andy/data/train/video_folders \
###			home/andy/data/train/output_folder --interval 5  --waitTime 5

### -----------------NOTE---------------------
### The tree of video_folders: video_folders/video_folder/video.h264 
### Example:
###         20181013_city/dw_20181013_132808_0.000000_0.000000/video_first.h264

import os 
import cv2 
import sys
import shutil
import argparse

cars = {"re01":"re01_", "re02":"re02_", "re03":"re03_"}
cameras = {"1":"_01", "2":"_02", "3":"_03"}
weather = {"rainy":"rn", "cloudy":"cl", "foggy":"fg", "snowy":"sw", "sunny":"sn"}
roadstatus = {"highway":"hw", "tunnel":"tn", "city":"ct", "countryside":"cs"}

carNO = cars["re01"]
cameraNO = cameras["1"]
wt = weather["sunny"]
rs = roadstatus["highway"]

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('video_dir', help='video files directory', type=str)
  parser.add_argument('output_dir', help='output images directory ', type=str)
  parser.add_argument('--interval', help='take one in every interval frames', default=5, type=int)
  parser.add_argument('--waitTime', help='image display wait time', default=5, type=int)

  args = parser.parse_args()
  return args

def video2pic(video_dir, output_dir, interval, waitTime):
  folder_info = os.path.split(video_dir)  # ['/home/andy/Desktop', 'dw_20180927_145333_0.000000_0.000000')]
  folder_name = os.path.basename(video_dir) 

  # Set the folder prefix
  if folder_name[:3] == "dw_":
    folder_name = folder_name[3:]
  #print(folder_name)

  if folder_name[-18:] == "_0.000000_0.000000":
    folder_name = folder_name[:-18]
  #print(folder_name)

  if folder_name[:5] != carNO:
    folder_name = carNO + folder_name
  #print(folder_name)

  if folder_name[-3:] != cameraNO:
    folder_name = folder_name + cameraNO

  ## rename folder
  folder_rename = os.path.join(folder_info[0], folder_name)
  os.rename(video_dir, folder_rename)
  output_folder = os.path.join(output_dir, folder_name)
  #print(output_folder)

  if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
  os.makedirs(output_folder)
  
  video_num = 0
  for video_file in os.listdir(folder_rename):
    if video_file[-4:] != "h264" and video_file[-3:] != "mkv":
      continue
    else:
      video_num += 1

    ## raname videos 
    video_info = os.path.splitext(video_file)
    #print(video_info)
    video_rename = video_info[0] + "_" + str(video_num).zfill(2) + video_info[1]
    video_file_path = os.path.join(folder_rename, video_file)
    video_file_path_rename = os.path.join(folder_rename, video_rename)
    os.rename(video_file_path, video_file_path_rename)
    print("video file path : %s"%(video_file_path_rename))

    cap = cv2.VideoCapture(video_file_path_rename)
    fps = cap.get(5)   # CV_CAP_PROP_FPS
    print("frame per second : %s \n interval : %s"%(fps, interval))

    retval, frame = cap.read()
    frame_num = 0

    while retval:
      if frame_num%interval == 0:
        pic_name = folder_name + "_" + wt + "_" + rs + "_" + str(frame_num) + ".png" 
        pic_path = os.path.join(output_folder, pic_name)

        cv2.imwrite(pic_path, frame)
        win = cv2.namedWindow('Clip Show', flags=cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Clip Show', frame)
        cv2.waitKey(waitTime)
      frame_num +=1
      retval, frame = cap.read()

    cv2.destroyAllWindows()
    cap.release()
    
    print("------video reading done ^_^------")
  print("------------finished ^_^ ------------------")


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
  
  for folder in os.listdir(video_dir):
    folder = os.path.join(video_dir, folder)
    video2pic(folder, output_dir, interval, waitTime)
