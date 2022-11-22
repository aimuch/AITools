import os
import cv2
from tqdm import tqdm
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgSrc', required=True, help='source images directory', type=str)
    parser.add_argument('--imgDst', required=True, help='output images directory', type=str)
    parser.add_argument('--w', type=int, required=True)
    parser.add_argument('--h', type=int, default=None)
    parser.add_argument('--isSquare', type=bool, default=False)
    args = parser.parse_args()
    return args

def cropCenterSquare(img, w=None):
    """center crop to square"""
    width, height, _ = img.shape
    short_dim = min(height, width)
    img = img[int((width - short_dim) / 2) : int((width + short_dim) / 2),
                int((height - short_dim) / 2) : int((height + short_dim) / 2)]
    if w and w <= short_dim:
        img = img[int((width - w) / 2) : int((width + w) / 2),
                    int((height - w) / 2) : int((height + w) / 2)]
    return img

def cropCenterRectangle(img, w, h):
    """center crop to rectangle"""
    width, height, _ = img.shape
    short_dim = min(height, width)
    if w <= short_dim and h <= short_dim:
        img = img[int((width - w) / 2) : int((width + w) / 2),
                    int((height - h) / 2) : int((height + h) / 2)]
    return img

def main(srcImg, dstImg, w, h=None, isSquare=False):
    imgList = os.listdir(srcImg)
    for i in tqdm(imgList):
        img = cv2.imread(os.path.join(srcImg, i))
        if isSquare:
            cv2.imwrite(os.path.join(dstImg, i), cropCenterSquare(img, w), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        else:
            cv2.imwrite(os.path.join(dstImg, i), cropCenterRectangle(img, w, h), [int(cv2.IMWRITE_JPEG_QUALITY), 100])
if __name__ == '__main__':
    args = parse_args()
    main(args.imgSrc, args.imgDst, args.w, args.h, args.isSquare)
    print("Done!")
