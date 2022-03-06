from sprite import Ball, Hole
import random
import config
import numpy as np
from table import Table
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import tree
import time
time_start = round(time.time() * 1000)
fig, ax = plt.subplots()
# ax.set_xlim((-600, 800))
# ax.set_ylim((-600, 800))
ax.set_xlim((-200, 200))
ax.set_ylim((-200, 200))

radius = config.radius

def print_table(root, tables):
    
    ball_start = np.array((root.mball.pos[0,0], root.mball.pos[1,0]))
    for table in tables:
        line_x, line_y = (table.holes[0].pos[0,0], table.holes[2].pos[0,0]), (table.holes[0].pos[1,0], table.holes[2].pos[1,0])
        line = Line2D(line_x, line_y)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[3].pos[0,0], table.holes[5].pos[0,0]), (table.holes[3].pos[1,0], table.holes[5].pos[1,0])
        line = Line2D(line_x, line_y)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[0].pos[0,0], table.holes[3].pos[0,0]), (table.holes[0].pos[1,0], table.holes[3].pos[1,0])
        line = Line2D(line_x, line_y)
        ax.add_line(line)
        
        line_x, line_y = (table.holes[2].pos[0,0], table.holes[5].pos[0,0]), (table.holes[2].pos[1,0], table.holes[5].pos[1,0])
        line = Line2D(line_x, line_y)
        ax.add_line(line)
        
        ball = plt.Circle(np.array((table.mball.pos[0,0], table.mball.pos[1,0])), radius, color='blue')
        
        ax.add_patch(ball)
        for tball in table.tballs:
            circle = plt.Circle(np.array((tball.pos[0,0], tball.pos[1,0])), radius, color='green')
            ax.add_patch(circle)
            for pos in tball.hit_pos:
                # print(pos)
                ball_end = np.array((pos[0,0], pos[1,0]))
                hit = plt.Circle(ball_end, 0.5, color='red')
                ax.add_patch(hit)
                line = Line2D((ball_start[0], ball_end[0]), (ball_start[1], ball_end[1]), linewidth=0.05)
                ax.add_line(line)
            
        for hole in table.holes:
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

table = Table(np.matrix([[3], [3]]), np.matrix([[0], [0]]), mball, tballs, hole)


mtable = []
for i in range(3, 4):
    for j in range(2, 4):
        t = table.mirror_table(np.matrix([[i], [j]]))
        mtable.append(t)

# q = []
# mtable = []        
# tree_node = tree.TreeNode.find_mtable_tree(3)
# q.append(tree_node)
# while len(q) > 0:
#     node = q.pop(0)
#     print(node.index)
#     t = table.mirror_table(np.matrix([[node.index[0]], [node.index[1]]]))
#     mtable.append(t)
#     for child in node.child:
#         q.append(child)
time_mid = round(time.time() * 1000)
print(time_mid - time_start)

print_table(table, mtable)

time_end = round(time.time() * 1000)

print(time_end - time_mid)