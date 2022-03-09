from math import ceil


def multiples_btw_interval(start, end, multiple):
    mx = max(start, end)
    mn = min(start, end)
    print("Start", "End")
    print(mn, mx)
    mn = ceil(mn/multiple) * multiple
    mx = ceil(mx/multiple) * multiple
    return list(range(mn, mx, multiple))

# Case 1 btw neg and pos
print(multiples_btw_interval(-275, 275, 100) == [-200, -100, 0, 100, 200])
# Case 2 btw neg and neg
print(multiples_btw_interval(-375, -175, 150) == [-300])
# Case 3 btw pos and pos
print(multiples_btw_interval(175, 375, 150) == [300])
# Case 4 from gt to lt
print(multiples_btw_interval(275, -275, 100) == [-200, -100, 0, 100, 200])

# Input is not divisible by multiple
    