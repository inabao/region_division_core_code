import os
import time
import numpy as np
import pickle
size_x = 0.26
size_y = 0.34
begin_x = -74.03
begin_y = 40.58
xregin=(begin_x, size_x + begin_x)
yregin=(begin_y, size_y + begin_y)

def get_one_day(filename, day):
    if os.path.exists("data/day_%d.pl" % day):
        return
    with open(filename, 'r', encoding='utf8') as f:
        _ = f.readline()
        _ = f.readline()
        content = f.readline()
        d = []
        while len(content) != 0:
            data = content.split(",")
            xx = float(data[5])
            yy = float(data[6])
            t = time.strptime(data[1], '%Y-%m-%d %H:%M:%S')
            if xregin[0] < xx < xregin[1] and yregin[1] > yy > yregin[0] and t.tm_mday == day:
                d.append(((t.tm_hour, t.tm_min), (xx, yy)))
            content = f.readline()
    with open("data/day_%d.pl" % day, "wb") as f:
        pickle.dump(d, f)


def regin_part(loc, x, y):
    return int((loc[0]-xregin[0]) / (size_x / x)), int((loc[1]-yregin[0]) / (size_y / y))


def dataset_generate(day, regx=4, regy=8, depart=(16, 16), interval=1):
    X = []
    y = []
    def subProcess(day):
        with open("data/day_%d.pl" % day, "rb") as f:
            data = pickle.load(f)
        seq = [0] * (1440 // interval)
        for t, loc in data:
            if regin_part(loc, depart[0], depart[1]) == (regx, regy):
                seq[(t[0] * 60 + t[1])//interval] += 1
        seq = seq[-15:] + seq
        for i in range(15, len(seq)):
            X.append(seq[i-15:i])
            y.append(seq[i])
    if type(day) != list:
        subProcess(day)
    else:
        for i in day:
            subProcess(i)
    X = np.array(X)
    y = np.array(y)
    X = (X - X.min())/ (X.max() / 2) - 1
    y = (y - y.mean())
    return X, y

def dataset_generate_both(day, depart=(16, 16), interval=30):
    X = [[[] for _ in range(depart[1])] for _ in range(depart[0])]
    y = [[[] for _ in range(depart[1])] for _ in range(depart[0])]
    def subProcess(day):
        with open("data/day_%d.pl" % day, "rb") as f:
            data = pickle.load(f)
        seq = [[[0] * (1440 // interval) for _ in range(depart[1])] for _ in range(depart[0])]
        for t, loc in data:
            regx, regy = regin_part(loc, depart[0], depart[1])
            seq[regx][regy][(t[0] * 60 + t[1])//interval] += 1
        for regx in range(depart[0]):
            for regy in range(depart[1]):
                seq[regx][regy] = seq[regx][regy][-15:] + seq[regx][regy]
                for i in range(15, len(seq[regx][regy])):
                    X[regx][regy].append(seq[regx][regy][i-15:i])
                    y[regx][regy].append(seq[regx][regy][i])
    if type(day) != list:
        subProcess(day)
    else:
        for i in day:
            subProcess(i)
    X = np.array(X)
    y = np.array(y)
    X = (X - X.min())/ (X.max() / 2) - 1
    y = (y - y.mean())
    return X, y

def order_distribution(day, depart=(16, 16), start=(7,0), end=(8,0)):
    distribution = [[0]*depart[1] for _ in range(depart[0])]
    if type(day) == int:
        day = [day]
    for i in day:
        with open("data/day_%d.pl" % i, "rb") as f:
            data = pickle.load(f)
        for t, loc in data:
            if start < t < end:
                regx, regy = regin_part(loc, depart[0], depart[1])
                distribution[regx][regy] += 1
    return distribution


if __name__ == '__main__':
    interval = 1
    with open("data/day_%d.pl" % 14, "rb") as f:
        data = pickle.load(f)
    seq = [0] * (1440 // interval)
    for t, loc in data:
        if regin_part(loc, 16, 16) == (4, 8):
            seq[(t[0] * 60 + t[1]) // interval] += 1
    seq = np.array(seq)
    rand = np.random.normal(seq.mean(), seq.var(), seq.size)
    print(np.sqrt(np.mean((rand-seq)**2)))