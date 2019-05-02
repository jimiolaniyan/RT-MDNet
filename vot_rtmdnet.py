# import vot
# from vot import Rectangle
import sys
import cv2  # imread
import torch
import numpy as np
from os.path import realpath, dirname, join

from tracker_vot import RTMDNet_init, RTMDNet_track
from utils import get_axis_aligned_bbox
# from utils import get_axis_aligned_bbox, cxy_wh_2_rect

net_file = join(realpath(dirname(__file__)), 'models/rt-mdnet.pth')

# # warm up
# for i in range(10):
#     net.temple(torch.autograd.Variable(torch.FloatTensor(1, 3, 127, 127)).cuda())
#     net(torch.autograd.Variable(torch.FloatTensor(1, 3, 255, 255)).cuda())

# start to track
handle = vot.VOT("polygon")
Polygon = handle.region()
bbox = get_axis_aligned_bbox(Polygon)

# image_file = handle.frame()
# if not image_file:
#     sys.exit(0)

# target_pos, target_sz = np.array([cx, cy]), np.array([w, h])
# im = cv2.imread(image_file)  # HxWxC
# state = RTMDNet_init(net_file, image_file, bbox)  # init tracker
RTMDNet_init(net_file, image_file, bbox)  # init tracker

# while True:
#     image_file = handle.frame()
#     if not image_file:
#         break
#     im = cv2.imread(image_file)  # HxWxC
#     state = SiamRPN_track(state, im)  # track
#     res = cxy_wh_2_rect(state['target_pos'], state['target_sz'])

#     handle.report(Rectangle(res[0], res[1], res[2], res[3]))
