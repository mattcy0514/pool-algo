import numpy as np

class Sprite:
    def __init__(self, pos:np.matrix):
        self.pos = pos

class Ball(Sprite):
    hit_pos = []
    def __init__(self, pos:np.matrix, ball=None):
        super().__init__(pos)
    
    def append_hit_pos(self, pos:np.matrix):
        self.hit_pos.append(pos)

class Hole(Sprite):
    def __init__(self, pos:np.matrix):
        super().__init__(pos)