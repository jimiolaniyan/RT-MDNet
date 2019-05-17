import numpy as np

def get_axis_aligned_bbox(region):
    try:
        region = np.array([region[0][0][0], region[0][0][1], region[0][1][0], region[0][1][1],
                           region[0][2][0], region[0][2][1], region[0][3][0], region[0][3][1]])
    except:
        region = np.array(region)

    x_min = np.min(region[0::2])
    y_min = np.min(region[1::2])
    x_max = np.max(region[0::2])
    y_max = np.max(region[1::2])

    return np.array([x_min, y_min, x_max - x_min, y_max - y_min])

def cxy_wh_2_rect(box):
    return np.array([box[0]-box[2]/2, box[1]-box[3]/2, box[2], box[3]])
