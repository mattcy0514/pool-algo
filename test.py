from cmath import inf
from operator import invert
from sprite import Ball, Hole
import random
import config
import numpy as np
from table import Table
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import tree2, tree
import time
import algo

cushion_amt = 3
time_start = round(time.time() * 1000)
fig, ax = plt.subplots()
# ax.set_xlim((-600, 800))
# ax.set_ylim((-600, 800))
ax.set_xlim((-600, 800))
ax.set_ylim((-600, 800))

radius = config.radius
length = config.length
width = config.width

def take_first(element):
    return element[0]

def print_table(root, tables):
    
    ball_start = np.array((root.mball.pos[0,0], root.mball.pos[1,0]))
    for table in tables:
        line_x, line_y = (table.holes[0].pos[0,0], table.holes[2].pos[0,0]), (table.holes[0].pos[1,0], table.holes[2].pos[1,0])
        line = Line2D(line_x, line_y, linewidth=0.05)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[3].pos[0,0], table.holes[5].pos[0,0]), (table.holes[3].pos[1,0], table.holes[5].pos[1,0])
        line = Line2D(line_x, line_y, linewidth=0.05)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[0].pos[0,0], table.holes[3].pos[0,0]), (table.holes[0].pos[1,0], table.holes[3].pos[1,0])
        line = Line2D(line_x, line_y, linewidth=0.05)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[2].pos[0,0], table.holes[5].pos[0,0]), (table.holes[2].pos[1,0], table.holes[5].pos[1,0])
        line = Line2D(line_x, line_y, linewidth=0.05)
        ax.add_line(line)
        
        ball = plt.Circle(np.array((table.mball.pos[0,0], table.mball.pos[1,0])), radius, color='blue')
        ax.add_patch(ball)

        tball = table.tballs[0]

        circle = plt.Circle(np.array((tball.pos[0,0], tball.pos[1,0])), radius, color='green')
        ax.add_patch(circle)

        
        for tball in table.tballs:
            for pos in tball.hit_pos:
                border_intersection_list = []
                # print(pos)
                ball_end = np.array((pos[0,0], pos[1,0]))
                slope = (ball_end[1]-ball_start[1]) / (ball_end[0]-ball_start[0])
                print(slope)
                # if (slope == inf or slope == -inf):
                    # print("dx:", ball_end[0], ball_end[0], "dy:", ball_end[1], ball_start[1])
                    # print(ball_start, ball_end, "\n")
                
                x_multiples = algo.multiples_btw_interval(ball_start[0], ball_end[0], length)
                y_multiples = algo.multiples_btw_interval(ball_start[1], ball_end[1], width)

                for x in x_multiples:
                    y = slope * (x - ball_start[0]) + ball_start[1]
                    # intersection = plt.Circle((x, y), 0.01, color='black')
                    # ax.scatter(x, y, s=0.05)
                    border_intersection_list.append((x, y))
                    # ax.add_patch(intersection)

                for y in y_multiples:
                    x = (y - ball_start[1]) / slope + ball_start[0]
                    # intersection = plt.Circle((x, y), 0.01, color='black')
                    # ax.add_patch(intersection)
                    # ax.scatter(x, y, s=0.05)
                    border_intersection_list.append((x, y))
                
                border_intersection_list.sort(key=take_first)
                # print(border_intersection_list)

                for i in range(len(border_intersection_list)):
                    # print(np.matrix([[coordinates[0]], [coordinates[1]]]))
                    border_intersection_list[i] = algo.mirror_transform(np.matrix([[border_intersection_list[i][0]], [border_intersection_list[i][1]]]), root.index_rr, inverse=True)
                    # print(coordinates)
                    ax.scatter(border_intersection_list[i][0,0], border_intersection_list[i][1,0], s=0.05)
                
                border_intersection_list.insert(0, np.matrix([[ball_start[0]], [ball_start[1]]]))
                border_intersection_list.append(algo.mirror_transform(pos, root.index_rr, inverse=True))
                print(border_intersection_list)
                print("pos")
                print(pos)

                for i in range(len(border_intersection_list) - 1):
                    x = [border_intersection_list[i][0,0], border_intersection_list[i+1][0,0]]
                    y = [border_intersection_list[i][1,0], border_intersection_list[i+1][1,0]]

                    line = Line2D(x, y, linewidth=0.05)
                    ax.add_line(line)
                    # print(i)
                    # print(border_intersection_list[i], border_intersection_list[i+1])
                # print(ball_start, border_intersection_list)
                

                print('\n')



                hit = plt.Circle(ball_end, 0.5, color='red')
                ax.add_patch(hit)
                # print(ball_end - ball_start)
                # line = Line2D((ball_start[0], ball_end[0]), (ball_start[1], ball_end[1]), linewidth=0.05)
                # ax.add_line(line)
                
        for hole in table.holes:
            tball = table.tballs[0]
            line = Line2D((hole.pos[0,0], tball.pos[0,0]), (hole.pos[1,0], tball.pos[1,0]), linewidth=0.05, color="r")
            ax.add_line(line)
            # print(hole.pos)
            hole = plt.Circle(np.array((hole.pos[0,0], hole.pos[1,0])), radius, color='black')
            ax.add_patch(hole)
                    
    fig.savefig('plotcircles.png', dpi=1200)
    

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
for i in range(0, 5):
    tballs.append(Ball(np.matrix([[random.randint(10, 120)+10*i], [random.randint(10, 120)+10*i]])))

hole = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[100], [0]])), Hole(np.matrix([[200], [0]]))
        , Hole(np.matrix([[0], [200]])), Hole(np.matrix([[100], [200]])), Hole(np.matrix([[200], [200]]))]

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), np.matrix([[0], [0]]), mball, tballs, hole)


# mtable = []
# for i in range(3, 4):
#     for j in range(2, 4):
#         t = table.mirror_table(np.matrix([[i], [j]]))
#         mtable.append(t)
q = []
mtable = []        
tree_node = tree2.TreeNode.find_mtable_tree(cushion_amt)
q.append(tree_node)
while len(q) > 0:
    node = q.pop(0)
    # print(node.index)
    t = table.mirror_table(np.matrix([[node.index[0]], [node.index[1]]]))
    mtable.append(t)
    for child in node.child:
        q.append(child)
time_mid = round(time.time() * 1000)
# print(time_mid - time_start)

print_table(table, mtable)

time_end = round(time.time() * 1000)

# print(time_end - time_mid)