import os
import cv2
import argparse
import shutil
from matplotlib.pyplot import box
import numpy as np
from scipy.io import loadmat
from tqdm import tqdm

yolo_format = True
box_len = 40

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', help='image directory', type=str)
    parser.add_argument('label_path', help='label directory', type=str)
    parser.add_argument('resolution', help='resolution', type=int)
    parser.add_argument('dst_path', help='dst directory', type=str)

    args = parser.parse_args()
    return args


def process(image_path, label_path, resolution, dst_path):
    image_list = []
    label_list = []
    image_dst_path = os.path.join(dst_path, "image_dst")
    label_dst_path = os.path.join(dst_path, "label_dst")

    if os.path.exists(image_dst_path):
        shutil.rmtree(image_dst_path)
    os.makedirs(image_dst_path)
    if os.path.exists(label_dst_path):
            shutil.rmtree(label_dst_path)
    os.makedirs(label_dst_path)

    for item_name in tqdm(os.listdir(image_path)):
        if item_name.split(".")[-1] != "jpg":
            continue
        item_label = loadmat(os.path.join(label_path, item_name.replace(".jpg", ".mat")))
        img_dst_path = os.path.join(image_dst_path, item_name)
        txt_dst_path = os.path.join(label_dst_path, item_name.replace(".jpg", ".txt"))
        slots = item_label['slots']
        if len(slots) > 0:
            txt_file = open(txt_dst_path, 'w')
            if resolution > 0:
                item_image = cv2.resize(cv2.imread(os.path.join(image_path,item_name)), (resolution, resolution))
            else:
                item_image = cv2.imread(os.path.join(image_path,item_name))
            height, width = item_image.shape[0], item_image.shape[1]

            # item_image = np.transpose(item_image, (2, 0, 1)) # HWC->CHW
            image_list.append(item_image)
            marks = item_label['marks']
            for mark in marks:

                if yolo_format:
                    if resolution > 0:
                        mark_x_re, mark_y_re = mark[0] * resolution / height, mark[1] * resolution / width
                    else:
                        mark_x_re, mark_y_re = mark[0] / height, mark[1] / width
                    txt_file.write("0 " + str(mark_x_re) + " "+ str(mark_y_re) + " " + str(box_len/width) + " " + str(box_len/height) + '\n')
                else:
                    mark_x_re, mark_y_re = mark[0], mark[1]
                    txt_file.write("0 " + str(mark_x_re) + " "+ str(mark_y_re) + " " + str(box_len) + " " + str(box_len) + '\n')

            txt_file.close()
            cv2.imwrite(img_dst_path, item_image)

if __name__ == '__main__':
    args = parse_args()
    image_path = args.image_path
    label_path = args.label_path
    resolution = args.resolution
    dst_path = args.dst_path

    process(image_path, label_path, resolution, dst_path)
    print("Done!")