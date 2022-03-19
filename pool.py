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
ax.set_xlim((-600, 800))
ax.set_ylim((-600, 800))

radius = config.radius
length = config.length
width = config.width

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []

cushion_amt = int(input())

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
holes = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[length/2], [0]])), Hole(np.matrix([[length], [0]]))
        , Hole(np.matrix([[0], [width]])), Hole(np.matrix([[length/2], [width]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

for i in range(0, 1):
    tballs.append(Ball(np.matrix([[random.randint(50, 80)+10*i], [random.randint(50, 80)+10*i]])))

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, holes)

path = path.find_paths(table, table.mirror_table(np.matrix([[4], [5]])), "mball")
while path.first != None:
    print(path.first.no)
    path_node = path.first
    connected_node = path_node.connected_ll.first
    while connected_node.next != None:
        if connected_node.type == 'm':
            color = "g"
        else:
            color = "b"
        line = Line2D([connected_node.pos[0,0], connected_node.next.pos[0,0]], [connected_node.pos[1,0], connected_node.next.pos[1,0]], linewidth=0.5, color=color)
        ax.add_line(line)
        connected_node = connected_node.next
    path.first = path.first.next
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