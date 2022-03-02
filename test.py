from sprite import Ball, Hole
import random
import numpy as np
from table import Table
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

fig, ax = plt.subplots()

ax.set_xlim((-600, 400))
ax.set_ylim((-600, 400))


def print_table(tables):
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
        
        
        ball = plt.Circle(np.array((table.mball.pos[0,0], table.mball.pos[1,0])), 8, color='blue')
        ax.add_patch(ball)
        for tball in table.tballs:
            circle = plt.Circle(np.array((tball.pos[0,0], tball.pos[1,0])), 8, color='green')
            ax.add_patch(circle)
            for pos in tball.hit_pos:
                # print(pos)
                hit = plt.Circle(np.array((pos[0,0], pos[1,0])), 0.5, color='red')
                ax.add_patch(hit)
            
        for hole in table.holes:
            # print(hole.pos)
            hole = plt.Circle(np.array((hole.pos[0,0], hole.pos[1,0])), 8, color='black')
            ax.add_patch(hole)
                    
    fig.savefig('plotcircles.png')
    

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
for i in range(0, 9):
    tballs.append(Ball(np.matrix([[random.randint(10, 120)+10*i], [random.randint(10, 120)+10*i]])))

hole = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[100], [0]])), Hole(np.matrix([[200], [0]]))
        , Hole(np.matrix([[0], [200]])), Hole(np.matrix([[100], [200]])), Hole(np.matrix([[200], [200]]))]

table = Table(np.matrix([[3], [3]]), np.matrix([[0], [0]]), mball, tballs, hole)

mtable = []
for i in range(0, 5):
    for j in range(0, 5):
        t = table.mirror_table(np.matrix([[i], [j]]))
        mtable.append(t)
        
print_table(mtable)