from math import radians
import matplotlib.pyplot as plt
import numpy as np
import math


def hit_pos(m, t, r):
    diff = t - m
    if diff[0] != 0:
        theta = math.atan(abs(diff[1] / diff[0]))
    else:
        theta = math.pi / 2
    x_coef = -1 if diff[0] > 0 else 1
    y_coef = -1 if diff[1] > 0 else 1
    pos = np.array((m[0] + x_coef*2*r*math.cos(theta), m[1] + y_coef*2*r*math.sin(theta)))
    return pos
    
radius = 10
pos1 = np.array([50, 30])
pos2 = np.array([50, 50])
hit_pos = hit_pos(pos1, pos2, radius)
# print(pos1, pos2)
circle1 = plt.Circle(pos1, radius, color='r')
circle2 = plt.Circle(pos2, radius, color='blue')
circle3 = plt.Circle(hit_pos, 0.5, color='green')

fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
# (or if you have an existing figure)
# fig = plt.gcf()
# ax = fig.gca()

ax.set_xlim((0, 100))
ax.set_ylim((0, 100))

ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)

fig.savefig('plotcircles.png')