from sprite import Ball, Hole

from table import Table

import numpy as np
import config
import random

import path

length = config.length
width = config.width

cushion_amt = 3
# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []

# Init balls & holes
mball = Ball(np.matrix([[150], [75]]))
tballs = []
holes = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[length/2], [0]])), Hole(np.matrix([[length], [0]]))
        , Hole(np.matrix([[0], [width]])), Hole(np.matrix([[length/2], [width]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

for i in range(0, 1):
    tballs.append(Ball(np.matrix([[random.randint(100, 120)+10*i], [random.randint(100, 120)+10*i]])))

table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, holes)
# path_to_json = path.path_to_json
paths = path.find_all_paths(table, table.mirror_table(np.matrix([[3], [3]])), "mball")
current_path = paths.first

while current_path != None:
    print(path.is_connection_valid(current_path.connection_list, table))
    current_path = current_path.next