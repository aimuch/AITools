# import torch
# import torch.nn as nn

import numpy as np

def add_weight_decay(net, l2_value, skip_list=()):
    # https://raberrytv.wordpress.com/2017/10/29/pytorch-weight-decay-made-easy/

    decay, no_decay = [], []
    for name, param in net.named_parameters():
        if not param.requires_grad:
            continue # frozen weights
        if len(param.shape) == 1 or name.endswith(".bias") or name in skip_list:
            no_decay.append(param)
        else:
            decay.append(param)

    return [{'params': no_decay, 'weight_decay': 0.0}, {'params': decay, 'weight_decay': l2_value}]

# function for colorizing a label image:
def color_to_label_img(img):
    color_to_label = {
        (128, 64,128) : 0,
        (244, 35,232) : 1,
        (70, 70, 70) : 2,
        (102,102,156) : 3,
        (189,153,153) : 4,
        (153,153,153) : 5,

        (250,170, 30) : 6,
        (220,220,  0) : 7,
        (107,142, 35) : 8,
        (152,251,152) : 9,
        (70,130,180) : 10,

        (220, 20, 60) : 11,
        (255,  0,  0) : 12,
        (0,  0,142) : 13,
        (0,  0, 70) : 14,
        (0, 60,100) : 15,

        (0, 80,100) : 16,
        (0,  0,230) : 17,
        (119, 11, 320) : 18,
        (0,  0,  0) : 19,
        (250, 250, 210) : 20,

        (218,  165,  32) : 21,
        (124,  252,  0) : 22 
        }

    img_height, img_width, _ = img.shape

    img_label = np.zeros((img_height, img_width))
    for row in range(img_height):
        for col in range(img_width):
            color1 = img[row, col, 0]
            color2 = img[row, col, 1]
            color3 = img[row, col, 2]
            color = (color1, color2, color3)
            print("color=",color)
            img_label[row, col] = np.array(color_to_label[color])

    return img_label