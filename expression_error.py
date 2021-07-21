import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from data_deal import order_distribution
from gbrt import predict_error
K1 = 200
K2 = 200 * 8


def fast_calculate_expression_error(aList, j):
   aList = list(aList)
   m = len(aList)
   akj = sum(aList[:j] + aList[j + 1:])
   aij = aList[j]
   ex = np.exp(- akj - aij)
   r1_tmp = 0
   r2_tmp = 0
   p2 = 1
   for k2 in range(K2):
      p2 *= akj
      r2_tmp -= p2
      p2 /= (k2 + 1)
      r1_tmp -= p2
   r1 = 0
   r2 = ex * r2_tmp
   p1 = ex
   p2 = akj
   for k1 in range(1, K1):
      for k2 in range((m - 1) * (k1 - 1), min((m - 1) * k1, K2)):
         r2_tmp += 2 * p2
         p2 /= (k2 + 1)
         r1_tmp += 2 * p2
         p2 *= akj
      r1 += r1_tmp * p1
      p1 *= (aij / k1)
      r2 += r2_tmp * p1
   return (r1 * ((m - 1) / m) - r2 / m)

def calculate_expression_error(aList, j):
    aList = list(aList)
    m = len(aList)
    e = 0
    akj = sum(aList[:j] + aList[j + 1:])
    p1 = np.exp(-aList[j])
    for k1 in range(K1):
        p2 = np.exp(-akj)
        for k2 in range(K2):
            tmpE = (abs((m - 1) * k1 - k2) / m) * p1 * p2
            e += tmpE
            p2 *= akj
            p2 /= (k2 + 1)
        p1 *= aList[j]
        p1 /= (k1 + 1)
    return e

def calculate_expression(sqrt_n, sqrt_N, day):
    m = sqrt_N // sqrt_n + 1
    sqrt_N = sqrt_n * m
    print(sqrt_N)
    distribution = np.array(order_distribution(day, depart=(sqrt_N, sqrt_N), start=(7, 0), end=(7, 10)))
    res = 0
    for i in range(sqrt_n):
        for j in range(sqrt_n):
            data = distribution[i * m: (i+1) * m, j * m: (j+1) * m].flatten()
            for k in range(m*m):
                a = fast_calculate_expression_error(data, k)
                res += a
    return res

def calculate_d_alpha(distribution):
   distribution = np.array(distribution)
   return np.sum(np.abs(distribution - distribution.mean()))


def d_alpha_expression_error(sqrt_n, sqrt_N, day):
    m = sqrt_N // sqrt_n + 1
    sqrt_N = sqrt_n * m
    print(sqrt_N)
    distribution = np.array(order_distribution(day, depart=(sqrt_N, sqrt_N), start=(7, 0), end=(7, 10)))
    x = []
    y = []
    for i in range(sqrt_n):
        print(x,y)
        for j in range(sqrt_n):
            data = distribution[i * m: (i+1) * m, j * m: (j+1) * m].flatten()
            x.append(calculate_d_alpha(data))
            tmp_y = 0
            for k in range(m*m):
                a = fast_calculate_expression_error(data, k)
                tmp_y += a
            y.append(tmp_y)

    m = { i:j for j, i in zip(x, y)}
    return x, y


