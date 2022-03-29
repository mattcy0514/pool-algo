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
import tree2

fig, ax = plt.subplots()
# ax.set_xlim((-600, 800))
# ax.set_ylim((-600, 800))
ax.set_xlim((0, config.length))
ax.set_ylim((0, config.width))

radius = config.radius
length = config.length
width = config.width

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []

# cushion_amt = int(input())
cushion_amt = 4

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
holes = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[length/2], [0]])), Hole(np.matrix([[length], [0]]))
        , Hole(np.matrix([[0], [width]])), Hole(np.matrix([[length/2], [width]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

mball_circle = plt.Circle([mball.pos[0,0], mball.pos[1,0]], radius=radius, color="g")
ax.add_patch(mball_circle)
pos_list = [np.matrix([[103], [33]]), np.matrix([[20], [102]]), np.matrix([[21], [94]]), np.matrix([[58], [55]]), np.matrix([[49], [86]])]
for i in range(0, 5):
    color = "b"
    ball = None
    if i == 0:
        color = "r"
        # ball = Ball(np.matrix([[30], [75]]))
    # else:
    # ball = Ball(np.matrix([[random.randint(0, 120)+10*i], [random.randint(0, 120)+10*i]]))
    ball = Ball(pos_list[i])
    tballs.append(ball)
    tball = plt.Circle([tballs[i].pos[0,0], tballs[i].pos[1,0]], radius=radius, color=color)
    ax.add_patch(tball)

for b in tballs:
    print("np.matrix([[{}], [{}]]))\n".format(b.pos[0,0], b.pos[1,0]))
for hole in holes:
    hole = plt.Circle([hole.pos[0,0], hole.pos[1,0]], radius=radius, color="black")
    ax.add_patch(hole)

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, holes)


# cushion_type_list = ["mball", "tball"]
# print("cushion type: mball or tball:")
# cushion_type = cushion_type_list[int(input())]

tree_node = Tree.find_mtable_tree(cushion_amt).root

all_paths = path.LinkedList()
q = []
q.append(tree_node)
while(len(q) > 0):
    current = q.pop(0)
    print(current.index)
    mball_paths = path.find_all_paths(table, table.mirror_table(np.matrix([[current.index[0]], [current.index[1]]])), "mball")
    tball_paths = path.find_all_paths(table, table.mirror_table(np.matrix([[current.index[0]], [current.index[1]]])), "tball")

    path_node = mball_paths.first
    while path_node != None:
        # print(path_node.no)
        if not path.is_connection_valid(path_node.connection_list, table):
            mball_paths.remove(path_node)
            # print("removed", path_node.no)
        path_node = path_node.next
    
    # print("\n\n\nPossible Path")
    path_node = mball_paths.first
    while path_node != None:
        to_be_inserted_node = path.PathNode(no=path_node.no, connection_list=path_node.connection_list)
        
        all_paths.push_back(to_be_inserted_node)
        path_node = path_node.next


    path_node = tball_paths.first
    while path_node != None:
        # print(path_node.no)
        if not path.is_connection_valid(path_node.connection_list, table):
            tball_paths.remove(path_node)
            # print("removed", path_node.no)
        path_node = path_node.next
    
    # print("\n\n\nPossible Path")
    path_node = tball_paths.first
    while path_node != None:
        to_be_inserted_node = path.PathNode(no=path_node.no, connection_list=path_node.connection_list)
        
        all_paths.push_back(to_be_inserted_node)
        path_node = path_node.next
    
    # print("\n\n")

    for child in current.child:
        q.append(child)
    


# print("paths.first", paths.first)
path_node = all_paths.first
print("after validation")
while path_node != None:
    print("HI", path_node.no)
    path_node = path_node.next

path_node = all_paths.first
# path_node = all_paths.first
# paths.traverse()
path_dict = {}
while path_node != None:
    connection_list = path_node.connection_list
    evaluation = path.calculate_evaluation(connection_list)
    path_dict[evaluation] = path_node
    path_node = path_node.next

sorted_paths = sorted(path_dict.items())

if len(sorted_paths) > 3:
    # for i in range(len(sorted_paths)-40, len(sorted_paths)-35):
    for i in range(len(sorted_paths)-3, len(sorted_paths)):
        print(sorted_paths[i][1].no, "evaluation", sorted_paths[i][0])
        connection_list = sorted_paths[i][1].connection_list
        color = np.random.rand(3,)
        for j in range(len(connection_list)-1):
            current_pos = connection_list[j].pos
            next_pos = connection_list[j+1].pos
            line = Line2D([current_pos[0,0], next_pos[0,0]], [current_pos[1,0], next_pos[1,0]], linewidth=0.5, color=color)
            ax.text((current_pos[0,0] + next_pos[0,0]) / 2, (current_pos[1,0] + next_pos[1,0]) / 2, sorted_paths[i][1].no, fontsize=3)
            ax.add_line(line)

# while path_node != None:
#     # if path_node.no == "PATH PATH 40":
#         # print(path_node.no)
#         connection_list = path_node.connection_list
#         evaluation = path.calculate_evaluation(connection_list)
#         print(path_node.no, "evaluation", evaluation)
#         color_changed = False
#         for index in range(len(connection_list)-1):
#             connection_node = connection_list[index]
#             next_node = connection_list[index+1]
#             # if connection_node.type == next_node.type:
#             if not color_changed:
#                 color = np.random.rand(3,)
#                 color_changed = True
#             index_rr = table.index_rr
#             # current_pos = algo.mirror_transform(connection_node.pos, index_rr, inverse=True)
#             # next_pos = algo.mirror_transform(next_node.pos, index_rr, inverse=True)
#             current_pos = connection_node.pos
#             next_pos = next_node.pos
#             line = Line2D([current_pos[0,0], next_pos[0,0]], [current_pos[1,0], next_pos[1,0]], linewidth=0.5, color=color)
#             ax.text((current_pos[0,0] + next_pos[0,0]) / 2, (current_pos[1,0] + next_pos[1,0]) / 2, path_node.no, fontsize=3)
#             ax.add_line(line)
#         path_node = path_node.next

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