# plot PR curve by COCO API and mmdet API

import os
import mmcv
import numpy as np
import matplotlib.pyplot as plt

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

from mmcv import Config
from mmdet.datasets import build_dataset

MODEL = "mask_rcnn"
MODEL_NAME = "mask_rcnn_r50_fpn_1x_coco_senet"

CONFIG_FILE = f"configs/{MODEL}/{MODEL_NAME}.py"
RESULT_FILE = f"test_result/{MODEL_NAME}/latest.pkl"

def plot_pr_curve(config_file, result_file, metric="bbox"):
    """plot precison-recall curve based on testing results of pkl file.
        Args:
            config_file (list[list | tuple]): config file path.
            result_file (str): pkl file of testing results path.
            metric (str): Metrics to be evaluated. Options are
                'bbox', 'segm'.
    """
    
    cfg = Config.fromfile(config_file)
    # turn on test mode of dataset
    if isinstance(cfg.data.test, dict):
        cfg.data.test.test_mode = True
    elif isinstance(cfg.data.test, list):
        for ds_cfg in cfg.data.test:
            ds_cfg.test_mode = True

    # build dataset
    dataset = build_dataset(cfg.data.test)
    # load result file in pkl format
    pkl_results = mmcv.load(result_file)
    # convert pkl file (list[list | tuple | ndarray]) to json
    json_results, _ = dataset.format_results(pkl_results)
    # initialize COCO instance
    coco = COCO(annotation_file=cfg.data.test.ann_file)
    coco_gt = coco
    coco_dt = coco_gt.loadRes(json_results[metric]) 
    # initialize COCOeval instance
    coco_eval = COCOeval(coco_gt, coco_dt, metric)
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()
    # extract eval data
    precisions = coco_eval.eval["precision"]
    '''
    precisions[T, R, K, A, M]
    T: iou thresholds [0.5 : 0.05 : 0.95], idx from 0 to 9
    R: recall thresholds [0 : 0.01 : 1], idx from 0 to 100
    K: category, idx from 0 to ...
    A: area range, (all, small, medium, large), idx from 0 to 3
    M: max dets, (1, 10, 100), idx from 0 to 2
    '''
    pr_array1 = precisions[0, :, 0, 0, 2] 
    pr_array2 = precisions[1, :, 0, 0, 2] 
    pr_array3 = precisions[2, :, 0, 0, 2] 
    pr_array4 = precisions[3, :, 0, 0, 2] 
    pr_array5 = precisions[4, :, 0, 0, 2] 
    pr_array6 = precisions[5, :, 0, 0, 2] 
    pr_array7 = precisions[6, :, 0, 0, 2] 
    pr_array8 = precisions[7, :, 0, 0, 2] 
    pr_array9 = precisions[8, :, 0, 0, 2] 
    pr_array10 = precisions[9, :, 0, 0, 2] 

    x = np.arange(0.0, 1.01, 0.01)
    # plot PR curve
    plt.plot(x, pr_array1, label="iou=0.5")
    plt.plot(x, pr_array2, label="iou=0.55")
    plt.plot(x, pr_array3, label="iou=0.6")
    plt.plot(x, pr_array4, label="iou=0.65")
    plt.plot(x, pr_array5, label="iou=0.7")
    plt.plot(x, pr_array6, label="iou=0.75")
    plt.plot(x, pr_array7, label="iou=0.8")
    plt.plot(x, pr_array8, label="iou=0.85")
    plt.plot(x, pr_array9, label="iou=0.9")
    plt.plot(x, pr_array10, label="iou=0.95")

    plt.xlabel("recall")
    plt.ylabel("precison")
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.01)
    plt.grid(True)
    plt.legend(loc="lower left")
    plt.show()

if __name__ == "__main__":
    plot_pr_curve(config_file=CONFIG_FILE, result_file=RESULT_FILE, metric="segm")

    


    
