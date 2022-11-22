import os
from tqdm import tqdm
import numpy as np
import argparse
from mmcv.utils import Config

from mmseg.models.segmentors import *
from mmseg.datasets.builder import build_dataset, build_dataloader
from mmcv.parallel import DataContainer


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate weights for each class in a dataset")
    parser.add_argument("cfg")
    return parser.parse_args()


def CalculateWeigthsLabels(dataloaders, num_classes):
    z = np.zeros((num_classes,))
    for i, dl in enumerate(dataloaders):
        print('Calculating classes weights in dataset ' + str(i))
        tqdm_batch = tqdm(dl)
        for sample in tqdm_batch:
            try:
                if isinstance(sample['gt_semantic_seg'], DataContainer):
                    y = sample['gt_semantic_seg'].data[0]
                elif isinstance(sample['gt_semantic_seg'], list):
                    y = sample['gt_semantic_seg'][0].data[0]
                else:
                    raise NotImplementedError
            except:
                print('[Warning!] gt_semantic_seg is not in ', sample, " and skipped!")
                break
            y = y.detach().cpu().numpy()
            mask = (y >= 0) & (y < num_classes)
            labels = y[mask].astype(np.uint8)
            count_l = np.bincount(labels, minlength=num_classes)
            z += count_l

        tqdm_batch.close()
    total_frequency = np.sum(z)
    class_weights = []
    for frequency in z:
        class_weight = 1 / (np.log(1.1 + (frequency / total_frequency)))
        class_weights.append(class_weight)
    ret = np.array(class_weights)
    print(ret)

    return ret


if __name__ == '__main__':
    args = parse_args()
    cfg = Config.fromfile(args.cfg)
    cfg.gpu_ids = [6]

    datasets = [build_dataset(cfg.data[k]) for k, _ in cfg.data.items() if k in ['train', 'test']]

    loader_cfg = dict(num_gpus=len(cfg.gpu_ids), dist=False, seed=0, drop_last=True)
    loader_cfg.update({k: v
                       for k, v in cfg.data.items() if k not in [
                           'train', 'val', 'test', 'train_dataloader', 'val_dataloader', 'test_dataloader']
                       })
    train_loader_cfg = {**loader_cfg, **cfg.data.get('train_dataloader', {})}
    dataloaders = [build_dataloader(ds, **train_loader_cfg) for ds in datasets]
    CalculateWeigthsLabels(dataloaders, len(datasets[0].CLASSES))
