from matplotlib.pyplot import connect
import numpy as np
from tree2 import Tree, TreeNode
from table import Table
import algo
import config

length = config.length
width = config.width

class PathNode:
    counter = 0
    def __init__(self, next=None, connected_ll=None):
        PathNode.counter += 1
        self.no = "PATH " + str(PathNode.counter)
        self.next = next
        self.connected_ll = connected_ll
    
    def insert_next(self, node):
        self.next = node
    
    def __str__(self) -> str:
        return "No: " + self.no

class ConnectedNode:
    def __init__(self, pos:np.matrix, type, next=None):
        self.pos = pos
        self.type = type
        self.next = next

    def insert_next(self, node):
        self.next = node

    def __str__(self) -> str:
        return "Type: " + str(self.type) + "\nPos: " + str(self.pos)
    
class LinkedList:
    def __init__(self, first=None):
        self.first = first
        self.last = first

    def push_back(self, node):
        if self.last != None:
            self.last.insert_next(node)
        else:
            self.first = node
        self.last = node
    
    def traverse(self):
        current = self.first
        while current != None:
            print(current)
            current = current.next

def find_paths(root_table:Table, mirror_table:Table, cushion_type=None):
    path_ll = LinkedList()
    mball = root_table.mball
    tballs = None
    holes = mirror_table.holes

    if cushion_type == 'mball':
        tballs = mirror_table.tballs
    elif cushion_type == 'tball':
        tballs = root_table.tballs
    
    for tball in tballs:
        for hole in holes:
            connected_ll = calculate_path(mball.pos, tball.pos, hole.pos, length, width)
            path_ll.push_back(PathNode(connected_ll=connected_ll))
    return path_ll    

def calculate_path(mball_pos, tball_pos, hole_pos, length, width):
    connected_ll = LinkedList()
    contact_pos = algo.contact_pos(tball_pos, hole_pos)
    # line between mball_pos and contact_pos
    mball_contact_connected_ll = calculate_connected_nodes(mball_pos, contact_pos, length, width, "m")
    # line between tball_pos and hole_pos
    tball_hole_connected_ll = calculate_connected_nodes(tball_pos, hole_pos, length, width, "t")

    push_ll_back(connected_ll, mball_contact_connected_ll)
    push_ll_back(connected_ll, tball_hole_connected_ll)

    return connected_ll

def calculate_connected_nodes(start, end, length, width, type):
    connected_ll = LinkedList()
    points_passing_by_border = [start]
    xs_passing_by_border = algo.multiples_between_interval(start[0,0], end[0,0], length)
    ys_passing_by_border = algo.multiples_between_interval(start[1,0], end[1,0], width)
    for x in xs_passing_by_border:
        points_passing_by_border.append(algo.point_between_two_points(x, start, end, False))
    for y in ys_passing_by_border:
        points_passing_by_border.append(algo.point_between_two_points(y, start, end, True))
    
    if type != 't':
        points_passing_by_border.append(end)


    reversed = (end-start)[0,0] < 0
    points_passing_by_border.sort(key=lambda p:p[0,0], reverse=reversed)

    print(points_passing_by_border)
    for point in points_passing_by_border:
        connected_ll.push_back(ConnectedNode(point, type))
    
    return connected_ll

def push_ll_back(target_ll, src_ll):
    current_node = src_ll.first
    while current_node != None:
        target_ll.push_back(current_node)
        current_node = current_node.next


# print(algo.multiples_between_interval(349, 200, 200))
# print(algo.multiples_between_interval(481, 600, 100))


# ll = calculate_connected_nodes(np.matrix([[10], [10]]), np.matrix([[740], [690]]), length, width, "m-t")
# ll.traverse()


# calculate_path(np.matrix([[10], [10]]), np.matrix([[740], [690]]), np.matrix([[800], [800]]), length, width).traverse()
# connected_node1 = ConnectedNode(np.matrix([[1], [2]]), "m")
# connected_node2 = ConnectedNode(np.matrix([[1], [2]]), "m")
# connected_node3 = ConnectedNode(np.matrix([[1], [2]]), "t")
# connected_node4 = ConnectedNode(np.matrix([[1], [2]]), "t")
# connected_ll = LinkedList(connected_node1)
# connected_ll.push_back(connected_node2)
# connected_ll.push_back(connected_node3)
# connected_ll.push_back(connected_node4)

# path_node1 = PathNode()
# path_node2 = PathNode()
# path_node3 = PathNode()
# path_node1.connected_ll = connected_ll
# path_node2.connected_ll = connected_ll
# path_node3.connected_ll = connected_ll
# connected_ll = LinkedList(path_node1)
# connected_ll.push_back(path_node2)
# connected_ll.push_back(path_node3)
# connected_ll.traverse()


# # path_node = path_node1

# # while path_node != None:
# #     print(path_node.name)
# #     connected_ll = path_node.connected_ll
# #     connected_node = connected_ll.first
# #     while connected_node != None:
# #         print(connected_node.type, "\n", connected_node.pos)
# #         connected_node = connected_node.next
# #     path_node = path_node.next
