# A set of different algorithms used in other files

from math import ceil
import math
import numpy as np
import config

conf = config.conf
length = config.length
width = config.width

def hit_pos(self, m, t, r):
        diff = t - m
        if diff[0,0] != 0:
            theta = math.atan(abs(diff[1,0] / diff[0,0]))
        else:
            theta = math.pi / 2
        x_coef = -1 if diff[0,0] > 0 else 1
        y_coef = -1 if diff[1,0] > 0 else 1
        x = m[0,0] + x_coef*2*r*math.cos(theta)
        y = m[1,0] + y_coef*2*r*math.sin(theta)
        pos = np.matrix([[x], [y]])
        return pos

def mirror_transform(pos:np.matrix, index_rr:np.matrix=None, index_ij:np.matrix=None, inverse=False):
    x_reflect = np.matrix([[1, 0], [0, -1]])
    y_reflect = np.matrix([[-1, 0], [0, 1]])

    if (inverse == True):
        i = int((pos[0,0] / length))
        j = int((pos[1,0] / width))
        i = i - 1 if pos[0,0] < 0 else i
        j = j - 1 if pos[1,0] < 0 else j
        index_ij = np.matrix([[i], [j]]) + index_rr

    index_diff = index_ij - index_rr
    cx = abs(index_diff[1,0] % 2)
    cy = abs(index_diff[0,0] % 2)
    
    if cx:
        index_diff = index_diff + np.matrix([[0], [1]])
    if cy:
        index_diff = index_diff + np.matrix([[1], [0]])
    
    if (inverse == False):
        comp_mat = x_reflect ** cx * y_reflect ** cy
        return comp_mat * pos + conf * index_diff
    else:
        comp_mat = y_reflect ** (-cy) * x_reflect ** (-cx)
        return comp_mat * (pos - conf * index_diff)
    

def multiples_btw_interval(start, end, multiple):
    mx = max(start, end)
    mn = min(start, end)
    mn = ceil(mn/multiple) * multiple
    mx = ceil(mx/multiple) * multiple
    return list(range(mn, mx, multiple))

# print(mirror_transform(np.matrix([[0], [00]]), np.matrix([[3], [3]]), inverse=True))

# def calculate_path()