# -*- coding: utf-8 -*-

"""Preview
Code for 'Inf-Net: Automatic COVID-19 Lung Infection Segmentation from CT Scans'
submit to Transactions on Medical Imaging, 2020.
First Version: Created on 2020-05-13 (@author: Ge-Peng Ji)
"""

import torch
import torch.nn.functional as F
import numpy as np
import os
import argparse
from scipy import misc
#from Code.model_lung_infection.InfNet_ResNet import Inf_Net as Network
#from Code.model_lung_infection.InfNet_Res2Net import Inf_Net as Network
#from Code.model_lung_infection.InfNet_VGGNet import Inf_Net as Network
#from Code.model_lung_infection.InfNet_iresnet import Inf_Net as Network
#from Code.model_lung_infection.InfNet_ResNext import Inf_Net as Network
from Code.model_lung_infection.InfNet_ResNest import Inf_Net as Network
from Code.utils.dataloader_LungInf import test_dataset


def inference():
    parser = argparse.ArgumentParser()
    parser.add_argument('--testsize', type=int, default=352, help='testing size')
    parser.add_argument('--data_path', type=str, default='./Dataset/TestingSet/LungInfection-Test/',
                        help='Path to test data')
    parser.add_argument('--pth_path', type=str, default='./Snapshots/save_weights/Inf-Net/Inf-Net-100.pth',
                        help='Path to weights fileif `semi-sup`, edit it to `Semi-Inf-Net/Semi-Inf-Net-100.pth`')
    parser.add_argument('--save_path', type=str, default='./Results/Lung infection segmentation/Inf-Net/',
                        help='Path to save the predictions. if `semi-sup`, edit it to `Semi-Inf-Net`')
    parser.add_argument('--backbone', type=str, default='resNest',
                        help='change different backbone, choice: VGGNet16, ResNet50, Res2Net50, iresnet50, resnext, resNest')
   
    opt = parser.parse_args()
    

    print("#" * 20, "\nStart Testing (Inf-Net)\n{}\nThis code is written for 'Inf-Net: Automatic COVID-19 Lung "
                    "Infection Segmentation from CT Scans', 2020, arXiv.\n"
                    "----\nPlease cite the paper if you use this code and dataset. "
                    "And any questions feel free to contact me "
                    "via E-mail (gepengai.ji@163.com)\n----\n".format(opt.backbone, opt), "#" * 20)

    model = Network()
    # model = torch.nn.DataParallel(model, device_ids=[0, 1]) # uncomment it if you have multiply GPUs.
    model.load_state_dict(torch.load(opt.pth_path))
    model.cuda()
    model.eval()
         

    image_root = '{}/Imgs/'.format(opt.data_path)
    gt_root = '{}/GT/'.format(opt.data_path)
    test_loader = test_dataset(image_root, gt_root, opt.testsize)
    os.makedirs(opt.save_path, exist_ok=True)

    for i in range(test_loader.size):
        image, gt, name = test_loader.load_data()
        gt = np.asarray(gt, np.float32)
        gt /= (gt.max() + 1e-8)
        image = image.cuda()

        lateral_map_5, lateral_map_4, lateral_map_3, lateral_map_2, lateral_map_1, lateral_edge = model(image)
        res = lateral_map_2
        res = F.upsample(res, size=gt.shape, mode='bilinear', align_corners=False)
        res = res.sigmoid().data.cpu().numpy().squeeze()
        res = (res - res.min()) / (res.max() - res.min() + 1e-8)
        misc.imsave(opt.save_path + name, res)

    print('Test Done!')


if __name__ == "__main__":
    inference()