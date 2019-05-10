#-*-coding=utf-8 -*-
import json
import os
import re
import numpy as np
import math
import pandas as pd


import PIL.Image
import PIL.ImageDraw


def shape_to_mask(img_shape, points, shape_type=None, line_width=10, point_size=5):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]
    if shape_type == 'circle':
        assert len(xy) == 2, 'Shape of shape_type=circle must have 2 points'
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
    elif shape_type == 'rectangle':
        assert len(xy) == 2, 'Shape of shape_type=rectangle must have 2 points'
        draw.rectangle(xy, outline=1, fill=1)
    elif shape_type == 'line':
        assert len(xy) == 2, 'Shape of shape_type=line must have 2 points'
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == 'linestrip':
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == 'point':
        assert len(xy) == 1, 'Shape of shape_type=point must have 1 points'
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
    else:
        # assert len(xy) > 2, 'Polygon must have points more than 2'
        if len(xy) > 2:
            draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


def get_edge_num(points):
    num = 0
    length = len(points)
    for index in range(1, length-1):
        diff_x = abs(points[index-1][0] + points[index+1][0] - 2*points[index][0])
        diff_y = abs(points[index-1][1] + points[index+1][1] - 2*points[index][1])
        if diff_x > 2 and diff_y > 2:
            num += 1

    diff_x = abs(points[length-1][0] + points[1][0] - 2 * points[0][0])
    diff_y = abs(points[length-1][1] + points[1][1] - 2 * points[0][1])
    if diff_x > 2 and diff_y > 2:
        num += 1

    diff_x = abs(points[length-2][0] + points[0][0] - 2 * points[length-1][0])
    diff_y = abs(points[length-2][1] + points[0][1] - 2 * points[length-1][1])
    if diff_x > 2 and diff_y > 2:
        num += 1

    return num


def shapes_to_label(img_shape, shapes):
    cls = np.zeros(img_shape[:2], dtype=np.int32)
    label_edge_num = {}
    for index, shape in enumerate(shapes):
        points = shape['polygon']

        cls_id = index+1
        mask = shape_to_mask(img_shape[:2], points, 'polygon')
        cls[mask] = cls_id

        num = get_edge_num(points)
        label_edge_num[index+1] = num

    return cls, label_edge_num


def get_every_object_pix_num(image):
    class_num = image.max()
    obj_num = dict(zip(range(class_num+1), [0]*(class_num+1)))
    height, width = image.shape
    for index_i in range(height):
        for index_j in range(width):
            obj_num[image[index_i][index_j]] +=1
    return obj_num

def not_satisfy_num(lbl_num, label_edge_num, pix_thresh, edge_thresh):
    pix_num, edge_num = 0, 0
    for label,num in lbl_num.items():
        if num >= pix_thresh and label != 0:
            pix_num += 1

    # for label, num in label_edge_num.items():
    #     if num <= edge_thresh:
    #         edge_num += 1
    return pix_num, edge_num


def write_data_to_excle(file_path, column_name, datas):
    data = pd.np.vstack(datas)
    column_name = column_name
    df = pd.DataFrame(data=data.transpose(), columns=column_name)
    df.to_excel(file_path, index=False)



if __name__ == '__main__':
    #   注意：tx保存的是jpg， 其他的是png格式的
    print('正在处理数据....,请等待！！')
    #   '''将json的整个文件夹放在./data下'''
    # files_path = './data'
    
    files_path = '/media/andy/Data/Data/APA_SSE/APA_xinboyou/收回成品/a'
    #file_org = './result_area_edge'
    #if not os.path.isdir(file_org):
    #    os.mkdir(file_org)

    all_name, all_pix_num, all_edge_num = [],[],[]
    i = 1
    file_names = os.listdir(files_path)
    for file_name in file_names:
        file_path = os.path.join(files_path, file_name)
        files = os.listdir(file_path)
        json_file = [name for name in files if name.endswith('json')]

        for json_name in json_file:
            # json_name = '4_jpg.json'
            json_path = os.path.join(file_path, json_name)
            if os.path.isfile(json_path):
                json_data = json.load(open(json_path))
                img_name = json_name.replace('.json', '.png')
                image_path = os.path.join(file_path, img_name)
                # image_data = json_data['imageData']
                Height = json_data['imgHeight']
                Width = json_data['imgWidth']
                # b = cv2.imread(image_path)  #路径必须是中文的 与img结构是一样的
                # with open(image_path, 'rb') as f:  #路径含中文的，读取二进制
                #     image_data = f.read()
                #     image_data = base64.b64encode(image_data).decode('utf-8')
                # img = img_b64_to_arr(image_data)  # 解析原图片数据
                # json_data['shapes'] = modify_point(json_data['shapes'], img.shape)
                # lbl_names = get_name_label(label_dict_init, json_data['shapes'])
                lbl, label_edge_num = shapes_to_label((Height, Width), json_data['objects'])

                lbl_num = get_every_object_pix_num(lbl)
                pix_num, edge_num = not_satisfy_num(lbl_num, label_edge_num, 1, 3)
                all_name.append(json_name)
                all_pix_num.append(pix_num)
                # all_edge_num.append(edge_num)
                print(i)
                i =i+1
                print(json_name)

                print('像素>=10的个数: ', pix_num, '边<=3的格式: ', edge_num)
    write_data_to_excle('./output.xlsx', ['json_name', 'pix_num'], [all_name, all_pix_num])
    print('数据处理完成！！')
