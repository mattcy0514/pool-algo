from collections import deque

class TreeNode:
    def __init__(self, index, parent, child, level):
        self.index = index
        self.parent = parent
        self.child = child
        self.level = level
    
    @staticmethod
    def find_mtable_tree(cushion_amt):
        root_node = TreeNode((cushion_amt, cushion_amt), None, [], 0)
        q = []
        parent_dict = {}
        q.append(root_node)
        
        i = 0
        
        while len(q) > 0:
            current_node = q.pop(0)
            current_index = current_node.index
            # print(i, current_index)
            i = i + 1
            first = current_index[0]
            second = current_index[1]
            level = current_node.level
            child_indices = [(first+1, second), (first-1, second), (first, second+1), (first, second-1)]

            for child_index in child_indices:
                child_node = TreeNode(child_index, current_node, [], level+1)
                # print(child_node.index)
                q.append(child_node)
                current_node.child.append(child_node)
                                
            if level == cushion_amt:
                break
        return root_node
            
# root_node = TreeNode.find_mtable_tree(3)
# for child in root_node.child:
    # print(child.index)