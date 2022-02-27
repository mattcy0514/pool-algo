import numpy as np 
import math
import config
from sprite import Ball, Hole

radius = config.radius

class Table:
    length = 100
    width = 100
    origin = np.matrix((0, 0))
    mball = None
    tballs = None
    holes = None
    
    def __init__(self, origin:np.matrix, mball, tballs, holes):
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
        if diff[0, 0] != 0:
            theta = math.atan(abs(diff[0, 1] / diff[0, 0]))
        else:
            theta = math.pi / 2
        x_coef = -1 if diff[0, 0] > 0 else 1
        y_coef = -1 if diff[0, 1] > 0 else 1
        x = m[0,0] + x_coef*2*r*math.cos(theta)
        y = m[0,1] + y_coef*2*r*math.sin(theta)
        pos = np.array((x, y))
        return pos
    