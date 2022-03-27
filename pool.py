from math import floor, ceil
import numpy as np
import random
import config
from sprite import Ball, Hole
from table import Table
from tree2 import Tree
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import algo
import path

fig, ax = plt.subplots()
# ax.set_xlim((-600, 800))
# ax.set_ylim((-600, 800))
ax.set_xlim((0, 200))
ax.set_ylim((0, 200))

radius = config.radius
length = config.length
width = config.width

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []

# cushion_amt = int(input())
cushion_amt = 3

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
holes = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[length/2], [0]])), Hole(np.matrix([[length], [0]]))
        , Hole(np.matrix([[0], [width]])), Hole(np.matrix([[length/2], [width]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

mball_circle = plt.Circle([mball.pos[0,0], mball.pos[1,0]], radius=radius, color="g")
ax.add_patch(mball_circle)
for i in range(0, 3):
    tballs.append(Ball(np.matrix([[random.randint(0, 120)+10*i], [random.randint(0, 120)+10*i]])))
    tball = plt.Circle([tballs[i].pos[0,0], tballs[i].pos[1,0]], radius=radius, color="b")
    ax.add_patch(tball)

for hole in holes:
    hole = plt.Circle([hole.pos[0,0], hole.pos[1,0]], radius=radius, color="black")
    ax.add_patch(hole)

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, holes)

cushion_type_list = ["mball", "tball"]
print("cushion type: mball or tball:")
cushion_type = cushion_type_list[int(input())]
# path_to_json = path.path_to_json
paths = path.find_all_paths(table, table.mirror_table(np.matrix([[int(input())], [int(input())]])), cushion_type)
# path_to_json(path)
path_node = paths.first
while path_node != None:
    print(path_node.no)
    # path.is_angle_valid(path_node.connection_list)
    if not path.is_connection_valid(path_node.connection_list, table):
        paths.remove(path_node)
        print("removed", path_node.no)
        # paths.remove(path_node)
        
    
    # if not path.is_connection_valid(path_node.connection_list, table):
        # paths.remove(path_node)
    path_node = path_node.next

print("paths.first", paths.first)
path_node = paths.first
print("after validation")
while path_node != None:
    print(path_node.no)
    path_node = path_node.next

path_node = paths.first
# paths.traverse()
while path_node != None:
    # print(path_node.no)
    connection_list = path_node.connection_list
    color_changed = False
    for index in range(len(connection_list)-1):
        connection_node = connection_list[index]
        next_node = connection_list[index+1]
        # if connection_node.type == next_node.type:
        if not color_changed:
            color = np.random.rand(3,)
            color_changed = True
        index_rr = table.index_rr
        # current_pos = algo.mirror_transform(connection_node.pos, index_rr, inverse=True)
        # next_pos = algo.mirror_transform(next_node.pos, index_rr, inverse=True)
        current_pos = connection_node.pos
        next_pos = next_node.pos
        line = Line2D([current_pos[0,0], next_pos[0,0]], [current_pos[1,0], next_pos[1,0]], linewidth=0.5, color=color)
        ax.text((current_pos[0,0] + next_pos[0,0]) / 2, (current_pos[1,0] + next_pos[1,0]) / 2, path_node.no, fontsize=3)
        ax.add_line(line)
    path_node = path_node.next
    print("\n")

plt.show()

# # Append mirror table to mtable via mtable index tree
# count = 0
# mtable_index_tree = Tree.find_mtable_tree(cushion_amt)
# tree_root = mtable_index_tree.root
# q = []
# q.append(tree_root)
# while len(q) > 0:
#     index = q.pop(0)
#     print(index.index)
#     # print(index.index)
#     t = table.mirror_table(np.matrix([[index.index[0]], [index.index[1]]]))
#     print(t.origin)
#     # count = count + 1
#     for child in index.child:
#         q.append(child)