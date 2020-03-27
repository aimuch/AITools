import os
import scipy.misc as misc
from xml.dom.minidom import Document
import numpy as np
import copy
import cv2
import sys
import shutil
sys.path.append('../../..')

from help_utils.tools import mkdir


def save_to_xml(save_path, im_height, im_width, objects_axis, label_name):
    im_depth = 0
    object_num = len(objects_axis)
    doc = Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('VOC2007')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    filename_name = doc.createTextNode('000024.jpg')
    filename.appendChild(filename_name)
    annotation.appendChild(filename)

    source = doc.createElement('source')
    annotation.appendChild(source)

    database = doc.createElement('database')
    database.appendChild(doc.createTextNode('The VOC2007 Database'))
    source.appendChild(database)

    annotation_s = doc.createElement('annotation')
    annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
    source.appendChild(annotation_s)

    image = doc.createElement('image')
    image.appendChild(doc.createTextNode('flickr'))
    source.appendChild(image)

    flickrid = doc.createElement('flickrid')
    flickrid.appendChild(doc.createTextNode('322409915'))
    source.appendChild(flickrid)

    owner = doc.createElement('owner')
    annotation.appendChild(owner)

    flickrid_o = doc.createElement('flickrid')
    flickrid_o.appendChild(doc.createTextNode('knautia'))
    owner.appendChild(flickrid_o)

    name_o = doc.createElement('name')
    name_o.appendChild(doc.createTextNode('yang'))
    owner.appendChild(name_o)

    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(im_width)))
    height = doc.createElement('height')
    height.appendChild(doc.createTextNode(str(im_height)))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(im_depth)))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    segmented = doc.createElement('segmented')
    segmented.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segmented)
    for i in range(object_num):
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode(label_name[int(objects_axis[i][-1])]))
        objects.appendChild(object_name)
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        objects.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        objects.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        objects.appendChild(difficult)
        bndbox = doc.createElement('bndbox')
        objects.appendChild(bndbox)

        x0 = doc.createElement('x0')
        x0.appendChild(doc.createTextNode(str((objects_axis[i][0]))))
        bndbox.appendChild(x0)
        y0 = doc.createElement('y0')
        y0.appendChild(doc.createTextNode(str((objects_axis[i][1]))))
        bndbox.appendChild(y0)

        x1 = doc.createElement('x1')
        x1.appendChild(doc.createTextNode(str((objects_axis[i][2]))))
        bndbox.appendChild(x1)
        y1 = doc.createElement('y1')
        y1.appendChild(doc.createTextNode(str((objects_axis[i][3]))))
        bndbox.appendChild(y1)

        x2 = doc.createElement('x2')
        x2.appendChild(doc.createTextNode(str((objects_axis[i][4]))))
        bndbox.appendChild(x2)
        y2 = doc.createElement('y2')
        y2.appendChild(doc.createTextNode(str((objects_axis[i][5]))))
        bndbox.appendChild(y2)

        x3 = doc.createElement('x3')
        x3.appendChild(doc.createTextNode(str((objects_axis[i][6]))))
        bndbox.appendChild(x3)
        y3 = doc.createElement('y3')
        y3.appendChild(doc.createTextNode(str((objects_axis[i][7]))))
        bndbox.appendChild(y3)

    f = open(save_path, 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


class_list = ['bus', 'car', 'child', 'cyclist',
              'dog', 'electric_cyclist', 'motocyclist',
              'person', 'person_sitting',
              'train', 'tricyclist',
              'truck', 'van', 'cat']


def format_label(txt_list):
    format_data = []
    for i in txt_list:
        if len(i.split(' ')) < 9:
            continue
        format_data.append(
            [float(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8])]
        )

        if i.split(' ')[8] not in class_list:
            print('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)


def move_file(image_path, save_dir, boxes_all, width, height):
    if len(boxes_all) > 0:      
        dst_xml_path = os.path.join(save_dir, 'labeltxt')
        dst_img_path = os.path.join(save_dir, 'images')
        if not os.path.exists(dst_xml_path):
            os.makedirs(dst_xml_path)
        if not os.path.exists(dst_img_path):
            os.makedirs(dst_img_path)
        dst_img_path_ = os.path.join(dst_img_path, os.path.basename(image_path))
        shutil.copyfile(image_path, dst_img_path_)
        xml = os.path.join(dst_xml_path, os.path.basename(image_path).replace(".jpg", ".xml"))
        save_to_xml(xml, width, height, boxes_all, class_list)


print('class_list', len(class_list))
raw_data = 'data/FISHEYE/train/'
raw_images_dir = os.path.join(raw_data, 'images')
raw_label_dir = os.path.join(raw_data, 'labelTxt')

save_dir = 'data/FISHEYE/FISHEYE_train/trainval/'

images = [i for i in os.listdir(raw_images_dir) if 'jpg' in i]
labels = [i for i in os.listdir(raw_label_dir) if 'txt' in i]

print('find image', len(images))
print('find label', len(labels))

min_length = 1e10
max_length = 1

img_h, img_w = 800, 800

for idx, img in enumerate(images):
    print(idx, 'read image', img)
    img_path = os.path.join(raw_images_dir, img)

    txt_data = open(os.path.join(raw_label_dir, img.replace('jpg', 'txt')), 'r').readlines()
    box = format_label(txt_data)
    move_file(img_path, save_dir, box, img_w, img_h)
