# A set of different algorithms used in other files

from math import ceil, dist, floor
import math
import numpy as np

import config

conf = config.conf
length = config.length
width = config.width
radius = config.radius

def contact_pos(tpos, hpos):
        diff = hpos - tpos
        if diff[0,0] != 0:
            theta = math.atan(abs(diff[1,0] / diff[0,0]))
        else:
            theta = math.pi / 2
        x_coef = -1 if diff[0,0] > 0 else 1
        y_coef = -1 if diff[1,0] > 0 else 1
        x = tpos[0,0] + x_coef*2*radius*math.cos(theta)
        y = tpos[1,0] + y_coef*2*radius*math.sin(theta)
        contact_pos = np.matrix([[x], [y]])
        return contact_pos

def mirror_transform(pos:np.matrix, index_rr:np.matrix=None, index_ij:np.matrix=None, inverse=False):
    x_reflect = np.matrix([[1, 0], [0, -1]])
    y_reflect = np.matrix([[-1, 0], [0, 1]])

    if inverse:
        # i = int((pos[0,0] / length))
        # j = int((pos[1,0] / width))
        # i = i - 1 if pos[0,0] < 0 else i
        # j = j - 1 if pos[1,0] < 0 else j
        i = floor((pos[0,0] / length))
        j = floor((pos[1,0] / width))
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
    

def multiples_between_interval(start, end, multiple):
    mx = max(start, end)
    mn = min(start, end)
    mn = ceil(mn/multiple) * multiple
    mx = ceil(mx/multiple) * multiple
    return list(range(mn, mx, multiple))

def point_between_two_points(x, p1, p2, inverse=False):
    slope = (p2[1,0]-p1[1,0]) / (p2[0,0]-p1[0,0])
    if not inverse:
        return np.matrix([[x], [slope * (x-p1[0,0]) + p1[1,0]]])
    else:
        return np.matrix([[(x-p1[1,0]) / slope + p1[0,0]], [x]])

def angle_between_two_vectors(p1, p2):
    return math.acos(dot(p1, p2) / (norm(p1) * norm(p2)))

def distance_from_point_to_segment(p, p1, p2):
    ab_vect = p2 - p1
    ap_vect = p - p1
    ac_proj_vect = dot(ap_vect, ab_vect) * ab_vect / (norm(ab_vect) ** 2)
    r = dot(ab_vect, ap_vect) / (norm(ab_vect) ** 2)
    if r <= 0:
        return norm(ap_vect)
    elif r >= 1:
        bp_vect = p - p2
        return norm(bp_vect)
    else:
        cp_vect = ap_vect - ac_proj_vect
        return norm(cp_vect)

def distance_from_point_to_line(p, p1, p2):
    slope = (p2[1,0]-p1[1,0]) / (p2[0,0]-p1[0,0])
    b = -slope * p1[0,0] + p1[1,0]
    x, y = p[0,0], p[1,0]
    return abs((slope * x - y + b) / ((slope ** 2 + 1) ** (1/2)))

def norm(p):
    return (p[0,0] ** 2 + p[1,0] ** 2) ** (1/2)

def dot(p1, p2):
    return (p1.T * p2)[0,0]

print(distance_from_point_to_segment(np.matrix([[-10], [-10]]), np.matrix([[0], [0]]), np.matrix([[100], [100]])))
# print(angle_between_two_vectors(np.matrix([[2], [0]]), np.matrix([[-2], [2]])))
# print(is_collided_to_segment(np.matrix([[116], [114]]), np.matrix([[0], [25.34]]), np.matrix([[117], [104]]), 5))
# print(distance_from_point_to_line(np.matrix([[0], [0]]), np.matrix([[0], [0]]), np.matrix([[100], [0]])))
# print(mirror_transform(np.matrix([[200], [600]]), index_rr=np.matrix([[3], [3]]), inverse=True))
# p1 = np.matrix([[4], [4]])
# p2 = np.matrix([[4.001], [5]])
# print(point_between_two_points(5, p1, p2, True))
# # print(mirror_transform(np.matrix([[-300], [-350]]), np.matrix([[3], [3]]), inverse=True))

# def calculate_path()