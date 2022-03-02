from __future__ import annotations
import numpy as np 
import math
import config

import copy

radius = config.radius
conf = config.conf

class Table:
    length = 100
    width = 100
    origin = np.matrix((0, 0))
    mball = None
    tballs = None
    holes = None
    
    def __init__(self, index_rr:np.matrix, origin:np.matrix, mball, tballs, holes):
        self.index_rr = index_rr
        self.origin = origin
        self.mball = mball
        self.tballs = tballs
        self.holes = holes
        self.init_hit_pos()
                
    def init_hit_pos(self):
        for tball in self.tballs:
            for hole in self.holes:
                pos = self.hit_pos(tball.pos, hole.pos, radius)
                tball.append_hit_pos(pos)
                        
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
    
    def mirror_table(self, index_ij:np.matrix):
        # First, we need to clone object of itself
        # That is, deepcopy of self
        mtable = copy.deepcopy(self)

        mtable.index_rr = index_ij
        
        # origin transform
        mtable.origin = self.mirror_transform(mtable.origin, index_ij)
        # mball transform
        mtable.mball.pos = self.mirror_transform(mtable.mball.pos, index_ij)
        
        for i in range(len(mtable.tballs)):
            # idk why deepcopy does not work with list in tballs?
            # So, we need to manually deepcopy hit_pos again here.
            mtable.tballs[i].hit_pos = copy.deepcopy(self.tballs[i].hit_pos)
            # tballs transform
            mtable.tballs[i].pos = self.mirror_transform(mtable.tballs[i].pos, index_ij)
            for j in range(len(mtable.tballs[i].hit_pos)):
                # hit_pos transform
                mtable.tballs[i].hit_pos[j] = self.mirror_transform(mtable.tballs[i].hit_pos[j], index_ij)
        # holes transform
        for i in range(len(mtable.holes)):
            mtable.holes[i].pos = self.mirror_transform(mtable.holes[i].pos, index_ij)
            # print(mtable.holes[i].pos)
        
        return mtable    
    
    def mirror_transform(self, pos:np.matrix, index_ij:np.matrix):
        x_reflect = np.matrix([[1, 0], [0, -1]])
        y_reflect = np.matrix([[-1, 0], [0, 1]])

        index_diff = index_ij - self.index_rr

        cx = abs(index_diff[1,0] % 2)
        cy = abs(index_diff[0,0] % 2)
        
        if cx:
            index_diff = index_diff + np.matrix([[0], [1]])
        if cy:
            index_diff = index_diff + np.matrix([[1], [0]])
        
        comp_mat = x_reflect ** cx * y_reflect ** cy

        return comp_mat * pos + conf * index_diff