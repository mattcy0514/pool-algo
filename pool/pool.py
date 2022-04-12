import numpy as np
import random
import config
from sprite import Ball, Hole
from table import Table
from tree import Tree
import matplotlib.pyplot as plt
import path
from graphic import Graphic
import json

radius = config.radius
length = config.length
width = config.width

holes = [Hole(np.matrix([[0], [0]])), Hole(np.matrix([[0], [width/2]])), Hole(np.matrix([[0], [width]]))
        , Hole(np.matrix([[length], [0]])), Hole(np.matrix([[length], [width/2]])), Hole(np.matrix([[length], [width]]))]
origin = np.matrix([[0], [0]])

def pool(mball, tballs, cushion_amt, path_amt):

    graphic = Graphic()
    graphic._set_holes(holes, "black")
    graphic._set_mball(mball, "white")
    graphic._set_tballs(tballs, "red")
    table = Table(np.matrix([[cushion_amt], [cushion_amt]]), origin, mball, tballs, holes)
    tree_node = Tree.find_mtable_tree(cushion_amt).root

    avail_paths = path.LinkedList()
    q = []
    q.append(tree_node)
    while(len(q) > 0):
        current = q.pop(0)

        # mother cushion path
        mball_paths = path.find_all_paths(table, table.mirror_table(np.matrix([[current.index[0]], [current.index[1]]])), "mball")
        path_node = mball_paths.first
        while path_node != None:
            if not path.is_moving_valid(path_node.moving_list, table):
                mball_paths.remove(path_node)
            else:
                to_be_inserted_node = path.PathNode(no=path_node.no, moving_list=path_node.moving_list)
                avail_paths.push_back(to_be_inserted_node)
            path_node = path_node.next
        
        # target cushion path
        tball_paths = path.find_all_paths(table, table.mirror_table(np.matrix([[current.index[0]], [current.index[1]]])), "tball")
        path_node = tball_paths.first
        while path_node != None:
            if not path.is_moving_valid(path_node.moving_list, table):
                tball_paths.remove(path_node)
            else:
                to_be_inserted_node = path.PathNode(no=path_node.no, moving_list=path_node.moving_list)
                avail_paths.push_back(to_be_inserted_node)
            path_node = path_node.next
        
        for child in current.child:
            q.append(child)
        
    print("after validation")
    path_node = avail_paths.first
    path_dict = {}
    while path_node != None:
        moving_list = path_node.moving_list
        evaluation = path.calculate_evaluation(moving_list)
        path_dict[evaluation] = path_node
        path_node = path_node.next

    sorted_paths = sorted(path_dict.items())

    path_json = {}
    if len(sorted_paths) > path_amt:
        for i in range(len(sorted_paths)-path_amt, len(sorted_paths)):
            path_no = sorted_paths[i][1].no
            evaluation = sorted_paths[i][0]
            print(path_no, "evaluation", evaluation)
            moving_list = sorted_paths[i][1].moving_list
            graphic._set_moving_list(moving_list)
            path_json[path_no] = {"evaluation": str(evaluation),\
                "moving_list": [(str(moving.pos[0,0]), str(moving.pos[1,0])) for moving in moving_list]}
    graphic._savefig('pool.png', 1200)

    pool_json = {
        "mball": [str(mball.pos[0,0]), str(mball.pos[1,0])],
        "tballs": [(str(tball.pos[0,0]), str(tball.pos[1,0])) for tball in tballs],\
        "paths": path_json} 

    return json.dumps(pool_json)



# tballs = []
# for i in range(0, 5):
#         color = "b"
#         ball = None
#         if i == 0:
#             color = "r"
#             # ball = Ball(np.matrix([[30], [75]]))
#         # else:
#         ball = Ball(np.matrix([[random.randint(0, config.length)], [random.randint(0, config.width)]]))
#         # ball = Ball(pos_list[i])
#         tballs.append(ball)
#         tball = plt.Circle([tballs[i].pos[0,0], tballs[i].pos[1,0]], radius=radius, color=color)

# print(pool(Ball(np.matrix([[150], [50]])), tballs, holes, 5, 3))
# graphic._show()