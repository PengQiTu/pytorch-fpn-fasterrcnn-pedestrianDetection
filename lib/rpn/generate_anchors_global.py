from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from lib.rpn.generate_anchors import generate_anchors
import numpy as np

def generate_anchors_global(feat_stride, height, width, anchor_scales=(8,16,32), anchor_ratios=(0.5,1,2)):
  anchors = generate_anchors(base_size=feat_stride, ratios=np.array(anchor_ratios), scales=np.array(anchor_scales))

  # Enumerate all shifts
  shift_x = np.arange(0, width) * feat_stride
  shift_y = np.arange(0, height) * feat_stride
  shift_x, shift_y = np.meshgrid(shift_x, shift_y)
  shifts = np.vstack((shift_x.ravel(), shift_y.ravel(),
                      shift_x.ravel(), shift_y.ravel())).transpose()
  # Enumerate all shifted anchors:
  #
  # add A anchors (1, A, 4) to
  # cell K shifts (K, 1, 4) to get
  # shift anchors (K, A, 4)
  # reshape to (A*K, 4) shifted anchors
  A = anchors.shape[0]
  K = shifts.shape[0]
  anchors = anchors.reshape((1, A, 4)) + shifts.reshape((1, K, 4)).transpose((1, 0, 2))
  anchors = anchors.reshape((K * A, 4)).astype(np.float32, copy=False)

  return anchors