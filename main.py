import random

json_str = "{"
for i in range(6):
    json_str += '"{}": [[{}], [{}]]'.format(i, random.randint(0, 200), random.randint(0, 200))
    json_str += ','
json_str = json_str[:-1]
json_str += "}"
print(json_str)