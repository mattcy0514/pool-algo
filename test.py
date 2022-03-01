from sprite import Ball, Hole
import numpy as np
from table import Table
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.set_xlim((0, 200))
ax.set_ylim((0, 100))


def print_table(table):
    for tball in table.tballs:
        circle = plt.Circle(np.array((tball.pos[0,0], tball.pos[0,1])), 5, color='black')
        ax.add_patch(circle)
        for pos in tball.hit_pos:
            hit = plt.Circle(pos, 1, color='red')
            ax.add_patch(hit)
        
    for hole in table.holes:
        hole = plt.Circle(np.array((hole.pos[0,0], hole.pos[0,1])), 5, color='black')
        ax.add_patch(hole)
            
    fig.savefig('plotcircles.png')
    

# Init balls & holes
ballA = Ball(np.matrix([[10], [10]]))
ballB = []
for i in range(1, 2):
    ballB.append(Ball(np.matrix([[50+10*i], [50+10*i]])))

hole = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[100], [0]])), Hole(np.matrix([[200], [0]]))
        , Hole(np.matrix([[0], [100]])), Hole(np.matrix([[100], [100]])), Hole(np.matrix([[200], [100]]))]

table = Table(np.matrix([[3], [3]]), np.matrix([[0], [0]]), ballA, ballB, hole)
print(table.origin)
# print_table(table)
for tball in table.tballs:
    print(tball.hit_pos)
    
mtable = table.mirror_table(np.matrix([[4], [4]]))
print("MTABLE \n\n")
print(mtable.origin)
print(mtable.index_rr)
for tball in mtable.tballs:
    print(tball.hit_pos)