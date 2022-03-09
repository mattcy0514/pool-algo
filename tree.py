# Tree structure of indices for generating mirror table

class TreeNode:
    def __init__(self, index, child, level):
        self.index = index
        self.child = child
        self.level = level
    
    @staticmethod
    def find_mtable_tree(cushion_amt):
        root_node = TreeNode((cushion_amt, cushion_amt), [], 0)

        # Queue is for traversing mtable tree inorder
        # Dict is for recording the child pointed by whom
        q = []
        level_ancestor_dict = {}
        q.append(root_node)
        count = 0
        while len(q) > 0:
            current_node = q.pop(0)
            current_index = current_node.index
            x = current_index[0]
            y = current_index[1]
            current_level = current_node.level
            # print(current_index)``

            if level_ancestor_dict.get(current_level) == None:
                level_ancestor_dict[current_level] = []
            level_ancestor_dict[current_level].append(current_index)
            # print(level_ancestor_dict)
            child_list = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            
            for child in child_list:
                if current_level > 0 and child in level_ancestor_dict[current_level-1]:
                    child_list.remove(child)


            child_level = current_level + 1

            if child_level == cushion_amt:
                break

            for child in child_list:
                child_node = TreeNode(child, [], child_level)
                current_node.child.append(child_node)
                q.append(child_node)
            count = count + 1
        return root_node

node = TreeNode.find_mtable_tree(6)
q = []
q.append(node)
count = 0
while len(q) > 0:
    n = q.pop(0)
    child_list = []
    for child in n.child:
        child_list.append(child.index)
    print(n.index, child_list)
    for child in n.child:
        q.append(child)
    count = count + 1
print(count)
