#!/usr/bin/python

import vot
from vot import Rectangle
import sys
import logging
import torch
import numpy as np
from os.path import realpath, dirname, join

from tracker_vot import RTMDNet_init, RTMDNet_track
from vot_utils import get_axis_aligned_bbox, cxy_wh_2_rect
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


c = 0
logging.info('************* %s *************',c)

image_file = handle.frame()
logging.info(image_file)
if not image_file:
    sys.exit(0)

#state = RTMDNet_init(net_file, image_file, bbox)  # init tracker

try:
    state = RTMDNet_init(net_file, image_file, bbox)  # init tracker
except Exception as e:
    logging.info('error %s', e)

while True:
    c = c + 1
    logging.info('************* %s *************',c)
    image_file = handle.frame()
    logging.info(image_file)

    if not image_file:
        break

#    state = RTMDNet_track(state, image_file)
 #   box = state['target_bbox']
  #  #res = cxy_wh_2_rect(box)
   # #handle.report(Rectangle(res[0], res[1], res[2], res[3]))
    #handle.report(Rectangle(box[0], box[1], box[2], box[3]))

    #logging.info('box: %s, res: %s', box, res)
#    if c == 5:
#	sys.exit(0)
    try:
	state = RTMDNet_track(state, image_file)
	box = state['target_bbox']
        #res = cxy_wh_2_rect(box)
        #handle.report(Rectangle(res[0], res[1], res[2], res[3]))
        handle.report(Rectangle(box[0], box[1], box[2], box[3]))

    except Exception as e:
	logging.info('error is: %s',e)
