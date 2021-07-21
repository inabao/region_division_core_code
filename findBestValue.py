import math
import pickle
with open("real_error_result.pl", "rb") as f:
    value = pickle.load(f)


lookup = 0
def find(i):
    global lookup
    if calculated[i] == 0:
        lookup += 1
    calculated[i] = 1
    return value[i]

def threesplit():
    left = 0
    right = len(value)
    while right - left > 2:
        middleright = int(left / 3 + 2 * right / 3)
        middleleft = int(2 * left / 3 + right / 3)
        if find(middleleft) > find(middleright):
            left = middleleft
        else:
            right = middleright
    if find(right) > find(left): return left
    if find(right) < find(left): return right

def stepFind(step):
    previosError = find(0)
    current = step
    while find(current) < previosError:
        previosError = find(current)
        current += step
    minError = 1000
    res = 0
    for i in range(current - 2 * step, current):
        if find(i) < minError:
            res = i
            minError = find(i)
        else:
            return res
    return res

def stepDecre():
    step = math.ceil(len(value) / 4)
    pos = math.ceil(len(value) / 2)
    while abs(step) > 1:
        if find(pos + step) < find(pos):
            pos = pos + step
            step = math.ceil(step / 2)
        else:
            pos = pos - step
            step = - math.ceil(step / 2)
    print(step)
    return pos

def localsearch(start):
    current_value = find(start)
    bound = 2
    flag = True
    while flag:
        flag = False
        for i in range(bound, 0, -1):
            if find(i + start) < find(start):
                start = i + start
                flag = True
                break
            elif find(start - i) < find(start):
                start = start - i
                flag = True
                break
    return start





print(find(localsearch(16)))

print(lookup)