from matplotlib.pyplot import connect
import numpy as np
from table import Table
from sprite import Hole
import algo
import config
import copy
import math

length = config.length
width = config.width
radius = config.radius

class PathNode:
    counter = 0
    def __init__(self, prev=None, next=None, connection_list=None):
        PathNode.counter += 1
        self.no = "PATH " + str(PathNode.counter)
        self.next = next
        self.prev = prev
        self.connection_list = connection_list
    
    def insert_next(self, node):
        self.next = node
        node.prev = self

    def __str__(self) -> str:
        return "No: " + self.no

class ConnectionNode:
    def __init__(self, pos:np.matrix, type, next=None):
        self.pos = pos
        self.type = type
        self.next = next

    def __str__(self) -> str:
        return "Type: " + str(self.type) + "\nPos: " + str(self.pos)
    
class LinkedList:
    def __init__(self, first=None):
        self.first = first

    # Time Complexity = O(n), it can be implemented in O(1)
    def push_back(self, node):
        current_node = self.first
        if current_node == None:
            self.first = node
        else:
            while current_node.next != None:
                current_node = current_node.next
            current_node.insert_next(node)
    def remove(self, node):
        current_node = self.first
        if current_node == None:
            return False
        else:
            while current_node != None:
                if current_node == node:
                    # Case of only one node in linkedlist, then free the first node to None
                    if current_node.prev == None and current_node.next == None:
                        self.first = None
                    # Case of node being head
                    elif current_node.prev == None:
                        next = current_node.next
                        next.prev = None
                        self.first = next
                    elif current_node.next == None:
                        prev = current_node.prev
                        prev.next = None
                    else:
                        current_node.prev.next = current_node.next
                        current_node.next.prev = current_node.prev
                current_node = current_node.next

    def traverse(self):
        current = self.first
        while current != None:
            print("Current", current, "Next", current.next, "Prev", current.prev)
            current = current.next

def is_connection_valid(connection_list, table):
    

    if not is_angle_valid(connection_list):
        return False
    
    if is_table_collided_to_path(connection_list, table):
        print("collided", True)
        return False
        
    return True

def is_angle_valid(connection_list):
    for i in range(1, len(connection_list)-1):
        current_connection = connection_list[i+1]
        next_connection = connection_list[i]
        prev_connection = connection_list[i-1]
        if current_connection.type != next_connection.type:
            current_to_next_vect = next_connection.pos - current_connection.pos
            current_to_prev_vect = prev_connection.pos - current_connection.pos
            print("angle", algo.angle_between_two_vectors(current_to_next_vect, current_to_prev_vect), algo.angle_between_two_vectors(current_to_next_vect, current_to_prev_vect) < math.pi/2)
            return algo.angle_between_two_vectors(current_to_next_vect, current_to_prev_vect) < math.pi/2

def is_table_collided_to_path(connection_list, table):
    # This is extremely important
    tballs = copy.deepcopy(table.tballs)
    tballs.pop(0)

    holes = copy.deepcopy(table.holes)

    sprites = []

    for tball in tballs:
        sprites.append(tball)
    
    for hole in holes:
        sprites.append(hole)
    
    for sprite in sprites:
        if is_sprite_collided_to_path(connection_list, sprite):
            return True
    return False

def is_sprite_collided_to_path(connection_list, sprite):
    sprite_pos = sprite.pos
    for i in range(len(connection_list)-1):
        current_connection_pos = connection_list[i].pos
        next_connection_pos = connection_list[i+1].pos
        # if sprite is hole, only radius should be assigned
        # if sprite is ball, 2*radius should be assigned
        basic = config.radius if isinstance(sprite, Hole) else 2*config.radius
        if algo.distance_from_point_to_segment(sprite_pos, current_connection_pos, next_connection_pos) < basic:
            return True
    return False

def find_all_paths(root_table:Table, mirror_table:Table, cushion_type=None):
    path_ll = LinkedList()
    mball = root_table.mball
    tballs = None
    real_hit_holes_pos = mirror_table.real_hit_holes_pos

    if cushion_type == 'mball':
        tballs = mirror_table.tballs
    elif cushion_type == 'tball':
        tballs = root_table.tballs
    
    tball = tballs[0]
    # for tball in tballs:
    for hole_pos in real_hit_holes_pos:
        connection_list = calculate_path(mball.pos, tball.pos, hole_pos, length, width)
        # Remember to transform coordinates of connection node to the form of root table
        for index in range(len(connection_list)):
            connection_list[index].pos = algo.mirror_transform(connection_list[index].pos, mirror_table.index_rr, inverse=True)
        path_ll.push_back(PathNode(connection_list=connection_list))
    return path_ll    

def calculate_path(mball_pos, tball_pos, hole_pos, length, width):
    connection_list = []
    contact_pos = algo.contact_pos(tball_pos, hole_pos)

    # line between mball_pos and contact_pos
    mball_contact_connection_list = calculate_connection_nodes(mball_pos, contact_pos, length, width, "m")
    # line between tball_pos and hole_pos
    tball_hole_connection_list = calculate_connection_nodes(tball_pos, hole_pos, length, width, "t")

    append_to_list(connection_list, mball_contact_connection_list)
    append_to_list(connection_list, tball_hole_connection_list)

    return connection_list

def calculate_connection_nodes(start, end, length, width, type):
    connection_list = []
    points_passing_by_border = [start]
    # Find out x, y passing by border
    xs_passing_by_border = algo.multiples_between_interval(start[0,0], end[0,0], length)
    ys_passing_by_border = algo.multiples_between_interval(start[1,0], end[1,0], width)

    for x in xs_passing_by_border:
        border_point = algo.point_between_two_points(x, start, end, False)
        points_passing_by_border.append(border_point)

    for y in ys_passing_by_border:
        border_point = algo.point_between_two_points(y, start, end, True)
        # Because it is probable that the y border point is identical to x border point
        # Hence, it must traverse points_passing_by_border to prevent repeated elements
        is_repeated = False
        for point in points_passing_by_border:
            if point[0,0] == border_point[0,0] and point[1,0] == border_point[1,0]:
                is_repeated = True
        if not is_repeated:
            points_passing_by_border.append(border_point)

    # Maybe the end point is identical to the last element of points_passing_by_border
    if end[0,0] != points_passing_by_border[len(points_passing_by_border)-1][0,0] and \
        end[1,0] != points_passing_by_border[len(points_passing_by_border)-1][1,0]:
        points_passing_by_border.append(end)
    
    reversed = (end-start)[0,0] < 0
    points_passing_by_border.sort(key=lambda p:p[0,0], reverse=reversed)

    for point in points_passing_by_border:
        connection_list.append(ConnectionNode(point, type))
    
    return connection_list

def append_to_list(target_list, src_list):
    for src in src_list:
        target_list.append(src)

# Todo path_to_json and how to traverse linked node or linked list
def path_to_json(path):
    path = path.first
# print(algo.multiples_between_interval(349, 200, 200))
# print(algo.multiples_between_interval(481, 600, 100))


# ll = calculate_connection_nodes(np.matrix([[10], [10]]), np.matrix([[740], [690]]), length, width, "m-t")
# ll.traverse()


# calculate_path(np.matrix([[10], [10]]), np.matrix([[740], [690]]), np.matrix([[800], [800]]), length, width).traverse()
# connection_node1 = ConnectionNode(np.matrix([[1], [2]]), "m")
# connection_node2 = ConnectionNode(np.matrix([[1], [2]]), "m")
# connection_node3 = ConnectionNode(np.matrix([[1], [2]]), "t")
# connection_node4 = ConnectionNode(np.matrix([[1], [2]]), "t")
# connection_ll = LinkedList(connection_node1)
# connection_ll.push_back(connection_node2)
# connection_ll.push_back(connection_node3)
# connection_ll.push_back(connection_node4)

# path_node1.connection_ll = connection_ll
# path_node2.connection_ll = connection_ll
# # path_node3.connection_ll = connection_ll

# path_ll remove test
# path_node = None
# path_ll = LinkedList()
# for i in range(1, 6):
#     print(i)
#     if i == 3:
#         path_node = PathNode()
#         path_ll.push_back(path_node)
#     else:
#         path_ll.push_back(PathNode())
# path_ll.traverse()
# path_ll.remove(path_node)
# path_ll.traverse()

# connection_ll.traverse()
# print("\n", path_node, "\n")
# current = connection_ll.first
# while current != None:
#     if False:
#         if current == path_node:
#             current.remove()
#     else:
#         print(current)
#         connection_ll.remove(current)
#     current = current.next
# connection_ll.remove(path_node)

# connection_ll.traverse()


# # path_node = path_node1

# # while path_node != None:
# #     print(path_node.name)
# #     connection_ll = path_node.connection_ll
# #     connection_node = connection_ll.first
# #     while connection_node != None:
# #         print(connection_node.type, "\n", connection_node.pos)
# #         connection_node = connection_node.next
# #     path_node = path_node.next
