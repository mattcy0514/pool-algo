import copy

class A:
    value = 0
    
a = A()
print(a.value)

b = copy.copy(a)
print(b.value)

b.value = 2
print(a.value)
