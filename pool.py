from math import floor, ceil
import numpy as np
import random
import config
from sprite import Ball, Hole
from table import Table
from tree2 import TreeNode
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import algo

fig, ax = plt.subplots()
# ax.set_xlim((-600, 800))
# ax.set_ylim((-600, 800))
ax.set_xlim((-600, 800))
ax.set_ylim((-600, 800))

radius = config.radius
length = config.length
width = config.width

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []

cushion_amt = int(input())
mtable_list = []   

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
hole = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[length/2], [0]])), Hole(np.matrix([[length], [0]]))
        , Hole(np.matrix([[0], [width]])), Hole(np.matrix([[length/2], [width]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

for i in range(0, 10):
    tballs.append(Ball(np.matrix([[random.randint(10, 120)+10*i], [random.randint(10, 120)+10*i]])))

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, hole)


# Append mirror table to mtable via mtable index tree
count = 0
mtable_index_tree = TreeNode.find_mtable_tree(cushion_amt)
q = []
q.append(mtable_index_tree)
while len(q) > 0:
    index = q.pop(0)
    # print(index.index)
    t = table.mirror_table(np.matrix([[index.index[0]], [index.index[1]]]))
    mtable_list.append(t)
    # count = count + 1
    for child in index.child:
        q.append(child)

root_table = mtable_list[0]
root_mball_pos = root_table.mball.pos
root_table_index = root_table.index_rr

# Need to connected mball to hit_pos of all mirror table
# And to hit_pos to holes of mirror table
for mtable in mtable_list:
    for hit_pos in mtable.tballs[0].hit_pos:
        
        print("\norigin x-axis pos")
        print(root_mball_pos[0,0], hit_pos[0,0])
        print("btw x-axis pos")
        print(algo.multiples_btw_interval(root_mball_pos[0,0], hit_pos[0,0], length))
        print("\norigin y-axis pos")
        print(root_mball_pos[1,0], hit_pos[1,0])
        print("btw y-axis pos")
        print(algo.multiples_btw_interval(root_mball_pos[1,0], hit_pos[1,0], length))

        # print("root_ball\n", root_mball_pos, "\ntarget_ball\n", hit_pos)
    # for hit_pos in mtable.tballs[0].hit_pos:
        # for index_x in range(root_table_index[0,0], mtable_index[0,0]+1):

        # print((root_table.mball.pos[0,0], hit_pos[0,0]), (root_table.mball.pos[1,0], hit_pos[1,0]))
        # plt.plot((root_table.mball.pos[0,0], hit_pos[0,0]), (root_table.mball.pos[1,0], hit_pos[1,0]), linewidth=0.5)
        # print("hit_pos", hit_pos)
# print(count)
# plt.show()

# [-200, -150] [150, 200] [-200, 200]