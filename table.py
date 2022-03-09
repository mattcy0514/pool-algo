# Containing init_hit_pos, mirror_table
# init_hit_pos: utilized other balls and holes on the table to calculate responding hit position
# mirror table: utilized linear algebra to generate mirror table to calculate cushion

from __future__ import annotations
import numpy as np 
import math
import config
import algo

import copy

radius = config.radius
conf = config.conf

class Table:
    length = config.length
    width = config.width
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
        for index in range(len(self.tballs)):
            for hole in self.holes:
                pos = algo.hit_pos(self.tballs[index].pos, hole.pos, radius)
                self.tballs[index].append_hit_pos(pos)

    def mirror_table(self, index_ij:np.matrix):
        # First, we need to clone object of itself
        # That is, deepcopy of itself
        mtable = copy.deepcopy(self)

        mtable.index_rr = index_ij
        
        # origin transform
        mtable.origin = algo.mirror_transform(mtable.origin, self.index_rr, index_ij)
        # mball transform
        mtable.mball.pos = algo.mirror_transform(mtable.mball.pos, self.index_rr, index_ij)
        
        for i in range(len(mtable.tballs)):
            # idk why deepcopy does not work with list in tballs?
            # So, we need to manually deepcopy hit_pos again here.
            mtable.tballs[i].hit_pos = copy.deepcopy(self.tballs[i].hit_pos)
            # tballs transform
            mtable.tballs[i].pos = algo.mirror_transform(mtable.tballs[i].pos, self.index_rr, index_ij)
            for j in range(len(mtable.tballs[i].hit_pos)):
                # hit_pos transform
                mtable.tballs[i].hit_pos[j] = algo.mirror_transform(mtable.tballs[i].hit_pos[j], self.index_rr, index_ij)
        # holes transform
        for i in range(len(mtable.holes)):
            mtable.holes[i].pos = algo.mirror_transform(mtable.holes[i].pos, self.index_rr, index_ij)
            # print(mtable.holes[i].pos)
        
        return mtable    
   