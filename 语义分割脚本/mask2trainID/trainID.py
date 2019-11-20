# camera-ready

import pickle
import numpy as np
import cv2
import os
import glob
from collections import namedtuple
from utils import color_to_label_img
# (NOTE! this is taken from the official Cityscapes scripts:)


TRAINID_PATH = "../trainID"
MASK_PATH = "../uss_map_jpg"


TRAINID_PATH = os.path.abspath(TRAINID_PATH)
MASK_PATH = os.path.abspath(MASK_PATH)
print(TRAINID_PATH)
print(MASK_PATH)


Label = namedtuple( 'Label' , [

    'name'        , # The identifier of this label, e.g. 'car', 'person', ... .
                    # We use them to uniquely name a class

    'id'          , # An integer ID that is associated with this label.
                    # The IDs are used to represent the label in ground truth images
                    # An ID of -1 means that this label does not have an ID and thus
                    # is ignored when creating ground truth images (e.g. license plate).
                    # Do not modify these IDs, since exactly these IDs are expected by the
                    # evaluation server.

    'trainId'     , # Feel free to modify these IDs as suitable for your method. Then create
                    # ground truth images with train IDs, using the tools provided in the
                    # 'preparation' folder. However, make sure to validate or submit results
                    # to our evaluation server using the regular IDs above!
                    # For trainIds, multiple labels might have the same ID. Then, these labels
                    # are mapped to the same class in the ground truth images. For the inverse
                    # mapping, we use the label that is defined first in the list below.
                    # For example, mapping all void-type classes to the same ID in training,
                    # might make sense for some approaches.
                    # Max value is 255!

    'category'    , # The name of the category that this label belongs to

    'categoryId'  , # The ID of this category. Used to create ground truth images
                    # on category level.

    'hasInstances', # Whether this label distinguishes between single instances or not

    'ignoreInEval', # Whether pixels having this class as ground truth label are ignored
                    # during evaluations or not

    'color'       , # The color of this label
    ] )


# (NOTE! this is taken from the official Cityscapes scripts:)
labels = [
    #     name    id   trainId   category    catId   hasInstances    ignoreInEval   color(BGR)
    Label('unlabeled', 0, 0, 'void', 0, False, True, (0, 0, 0)),
    Label('Void', 0, 0, 'void', 0, False, True, (0, 0, 0)),
    Label('Road', 1, 1, 'flat', 1, False, False, (128, 64, 128)),
    Label('Guard Rail', 2, 2, 'construction', 2, False, True, (0, 255, 153)),
    Label('Obstacle', 3, 3, 'object', 3, False, False, (0, 153,  204)),
    Label('Sidewalk', 4, 4, 'flat', 1, False, False, (232, 35, 244)),
    Label('Wall', 5, 5, 'construction', 2, False, False, (156, 102, 102)),
    Label('Pole', 6, 6, 'object', 3, False, False, (153, 153, 153)),
    Label('Terrain', 7, 7, 'nature', 4, False, False, (152, 251, 152)),
    Label('Person', 8, 8, 'human', 6, True, False, (60, 20, 220)),
    Label('Car', 9, 9, 'vehicle', 7, True, False, (204, 0, 153)),
    Label('Bicycle', 10, 10, 'vehicle', 7, True, False, (70, 0, 0)),
    Label('Traffic Line', 11, 11, 'object', 3, False, False, (30, 170, 250)),
    Label('Slotline', 12, 12, 'construction', 2, False, False, (0, 220, 220)),
    Label('Center', 13, 13, 'object', 3, False, False, (0, 74, 111)),
    Label( 'Car Shadow',8,14,'nature',4,False,False, (217, 157, 12) ),
    # Label('Slot Text', 14, 14, 'nature', 4, False, False, (139,139,0)),
    # Label('Slot Pattern', 15, 15, 'nature', 4, False, False, (114,128,250)),

    # Label('parking', 9, 255, 'flat', 1, False, True, (250, 170, 160)),
    # Label('rail track', 10, 255, 'flat', 1, False, True, (230, 150, 140)),
    # Label('building', 11, 255, 'construction', 2, False, False, (70, 70, 70)),
    # Label('fence', 13, 255, 'construction', 2, False, False, (190, 153, 153)),
    # Label('bridge', 15, 255, 'construction', 2, False, True, (150, 100, 100)),
    # Label('tunnel', 16, 255, 'construction', 2, False, True, (150, 120, 90)),
    # Label('polegroup', 18, 255, 'object', 3, False, True, (153, 153, 153)),
    # Label('sky', 23, 255, 'sky', 5, False, False, (70, 130, 180)),
    # Label('rider', 25, 255, 'human', 6, True, False, (255, 0, 0)),
    # Label('truck', 27, 255, 'vehicle', 7, True, False, (0, 0, 70)),
    # Label('bus', 28, 255, 'vehicle', 7, True, False, (0, 60, 100)),
    # Label('caravan', 29, 255, 'vehicle', 7, True, True, (0, 0, 90)),
    # Label('trailer', 30, 255, 'vehicle', 7, True, True, (0, 0, 110)),
    # Label('train', 31, 255, 'vehicle', 7, True, False, (0, 80, 100)),
    # Label('motorcycle', 32, 255, 'vehicle', 7, True, False, (0, 0, 230)),
    # Label('license plate', -1, 255, 'vehicle', 7, False, True, (0, 0, 142)),
]

# create a function which maps id to trainId:
id_to_trainId = {label.id: label.trainId for label in labels}
id_to_trainId_map_func = np.vectorize(id_to_trainId.get)

#train_dirs = ["/media/tory/DATA1/qulei/apa/sse_json/gtCoarse/"]
val_dirs = [""]
test_dirs = [""]

cityscapes_data_path = os.path.join(MASK_PATH, "*.jpg")
print(cityscapes_data_path)
imgList = glob.glob(cityscapes_data_path)


################################################################################
# convert all labels to label imgs with trainId pixel values (and save to disk):
################################################################################
train_label_img_paths = []

#img_dir = cityscapes_data_path
label_dir = cityscapes_data_path
for img in imgList:
    print (img)
    imgName = os.path.basename(img)
    # train_img_dir_path = img_dir + img
    train_label_dir_path = label_dir

    # file_names = os.listdir(cityscapes_meta_path)
    # i = 0
    gtFine_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
    # convert gtFine_img from id to trainId pixel values:
    #  gtFine_img = cv2.imread("/media/tory/DATA1/qulei/APA_xinboyou/train_id-1000/2.png", 0)
    #   label_img = id_to_trainId_map_func(gtFine_img) # (shape: (1024, 2048))
    label_img = gtFine_img.astype(np.uint8)
    print (label_img.shape)
    label_img=color_to_label_img(label_img) # generate color_map
    # i += 1
    cv2.imwrite(os.path.join(MASK_PATH, str(imgName)), label_img)
    # train_label_img_paths.append(cityscapes_meta_path + "/label_imgs/" + imgName + "_train_id.png")

#img_dir = cityscapes_data_path + "/leftImg8bit/val/"
#label_dir = cityscapes_data_path + "/gtFine/val/"
#for val_dir in val_dirs:
#    print (val_dir)
#
#    val_img_dir_path = img_dir + val_dir
#    val_label_dir_path = label_dir + val_dir
#
#    file_names = os.listdir(val_img_dir_path)
#    for file_name in file_names:
#        imgName = file_name.split("_leftImg8bit.png")[0]
#
#        gtFine_img_path = val_label_dir_path + imgName + "_gtFine_labelIds.png"
#        gtFine_img = cv2.imread(gtFine_img_path, -1) # (shape: (1024, 2048))
#
#        # convert gtFine_img from id to trainId pixel values:
#        label_img = id_to_trainId_map_func(gtFine_img) # (shape: (1024, 2048))
#        label_img = label_img.astype(np.uint8)
#
#        cv2.imwrite(cityscapes_meta_path + "/label_imgs/" + imgName + ".png", label_img)
#
#################################################################################
## compute the class weigths:
#################################################################################
#print ("computing class weights")
#
#num_classes = 20
#
#trainId_to_count = {}
#for trainId in range(num_classes):
#    trainId_to_count[trainId] = 0
#
## get the total number of pixels in all train label_imgs that are of each object class:
#for step, label_img_path in enumerate(train_label_img_paths):
#    if step % 100 == 0:
#        print (step)
#
#    label_img = cv2.imread(label_img_path, -1)
#
#    for trainId in range(num_classes):
#        # count how many pixels in label_img which are of object class trainId:
#        trainId_mask = np.equal(label_img, trainId)
#        trainId_count = np.sum(trainId_mask)
#
#        # add to the total count:
#        trainId_to_count[trainId] += trainId_count
#
## compute the class weights according to the ENet paper:
#class_weights = []
#total_count = sum(trainId_to_count.values())
#for trainId, count in trainId_to_count.items():
#    trainId_prob = float(count)/float(total_count)
#    trainId_weight = 1/np.log(1.02 + trainId_prob)
#    class_weights.append(trainId_weight)
#
#print (class_weights)
#
# with open(cityscapes_meta_path + "/class_weights.pkl", "wb") as file:
#     pickle.dump(class_weights, file, protocol=2) # (protocol=2 is needed to be able to open this file with python2)