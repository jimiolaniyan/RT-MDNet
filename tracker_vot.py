import argparse
import sys
import time
import logging

import torch.optim as optim
from torch.autograd import Variable
from random import randint

sys.path.insert(0,'./modules')
from model import MDNet
from options import *
from img_cropper import *
from roi_align.modules.roi_align import RoIAlignAdaMax


def set_optimizer(model, lr_base, lr_mult=opts['lr_mult'], momentum=opts['momentum'], w_decay=opts['w_decay']):
    params = model.get_learnable_params()
    param_list = []
    for k, p in params.iteritems():
        lr = lr_base
        for l, m in lr_mult.iteritems():
            if k.startswith(l):
                lr = lr_base * m
        param_list.append({'params': [p], 'lr':lr})
    optimizer = optim.SGD(param_list, lr = lr, momentum=momentum, weight_decay=w_decay)
    # optimizer = optim.SGD(param_list, lr = 1., momentum=momentum, weight_decay=w_decay)
    return optimizer

def RTMDNet_init(model_path, image_file, init_bbox):
    target_bbox = np.array(init_bbox)
    model = MDNet(model_path)

    if opts['adaptive_align']:
        align_h = model.roi_align_model.aligned_height
        align_w = model.roi_align_model.aligned_width
        spatial_s = model.roi_align_model.spatial_scale
        model.roi_align_model = RoIAlignAdaMax(align_h, align_w, spatial_s)
    if opts['use_gpu']:
        model = model.cuda()

    model.set_learnable_params(opts['ft_layers'])

    # Init image crop model
    img_crop_model = imgCropper(1.)
    if opts['use_gpu']:
        img_crop_model.gpuEnable()

    # Init criterion and optimizer
    criterion = BinaryLoss()
    init_optimizer = set_optimizer(model, opts['lr_init'])
    update_optimizer = set_optimizer(model, opts['lr_update'])

    cur_image = Image.open(image_file).convert('RGB')
    cur_image = np.asarray(cur_image)

    logging.info(curr_image.shape)

def RTMDNet_track():
    print('I was called')