import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader

class WoodspaceDataset(Dataset):
    def __init__(self, img_path):
        super(WoodspaceDataset, self).__init__()
        self.img_dir_path = os.path.abspath(img_path)
        self.img_list = os.listdir(self.img_dir_path)

    def __getitem__(self, index):
        img_path_ = self.img_list[index]
        img_path = os.path.join(self.img_dir_path, os.path.basename(img_path_))
        img_bgr = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
        # h, w, c = img_rgb.shape
        # img_rgb = img_rgb.reshape(-1, c, h, w)
        return img_rgb

    def __len__(self):
        return len(self.img_list)

def collate_fn(batch):
    if isinstance(batch, torch.Tensor):
        batch = batch.transpose(0, 3, 1, 2) # NHWC -> NCHW
    elif isinstance(batch, np.ndarray):
        batch = np.transpose(data, (0, 3, 1, 2)) # NHWC -> NCHW
    else:
        pass
    return batch


dataset = WoodspaceDataset("/Users/andy/data/datasets/WoodSpace/rgb_images")
loader = DataLoader(
    dataset,
    batch_size=10,
    num_workers=1,
    shuffle=False,
    # collate_fn=collate_fn
)


mean = 0.
std = 0.
nb_samples = 0.
for data in tqdm(loader):
    data = np.transpose(data, (0, 3, 1, 2)) # NHWC -> NCHW
    batch_samples = data.size(0) # batch_size
    data = data.view(batch_samples, data.size(1), -1)   # N x C x H x W - > N x C x H*W
    mean += data.mean(2).sum(0)
    std += data.std(2).sum(0)
    nb_samples += batch_samples

mean /= nb_samples
std /= nb_samples

print("Mean:", mean)
print("Std:", std)