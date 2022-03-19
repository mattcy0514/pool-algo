# This file is to create Table Object
# Containing init_hit_pos, mirror_table
# init_hit_pos: utilized other balls and holes on the table to calculate responding hit position
# mirror table: utilized linear algebra to generate mirror table to calculate cushion

from __future__ import annotations
import copy
import numpy as np 

import config
import algo

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
        # holes transform
        for i in range(len(mtable.holes)):
            mtable.holes[i].pos = algo.mirror_transform(mtable.holes[i].pos, self.index_rr, index_ij)
            # print(mtable.holes[i].pos)
        
        return mtable    
   