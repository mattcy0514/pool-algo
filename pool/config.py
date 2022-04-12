# Configuration of this project

import numpy as np

scale = 2
radius = 6.15 * scale
length = 127 * scale
width = 254 * scale
conf = np.matrix([[length, 0], [0, width]])

e = radius * 0.001

alpha = 0.8