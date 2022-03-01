import copy
import numpy as np

class A:
    value = 0
    pos = np.matrix([1, 2])
    
    def create():
        return "create"
    
    @staticmethod
    def hello():
        print("Hello")
        


def modify(mat):
    return mat * np.matrix([[2], [1]])
    
test_mat = np.matrix([1, 1])
print(test_mat)  
test_mat = modify(test_mat)
print(test_mat)



# a = A()
# str = a.create()
# A.hello()
# b = a.create()
# print(b.value, b.pos)
# a = A()
# print("Default Initialized")
# print(a.value, a.pos)

# b = a
# b.value = 2
# b.pos = np.matrix([3, 4])

# print("Assign a to b")
# print(a.value, a.pos)

# c = copy.deepcopy(a)
# c.value = 3
# c.pos = np.matrix([5, 6])

# print("Deep copy A")
# print(a.value, a.pos)
# print("Deep copy C")
# print(c.value, c.pos)
