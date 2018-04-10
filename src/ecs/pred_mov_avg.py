# coding=utf-8
import datetime
from gbdt.data import DataSet
from gbdt.model import GBDT


def get_series(ecs_lines, d, train_start):
    for l in ecs_lines:
        id, k, t = l.strip().split("\t")
        dt = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
        if k in d:
            delta = (dt - train_start).days
            d[k][delta] += 1


def get_average(l, k):
    i = k
    s = 0
    j = 0
    while i < len(l):
        s += sum(l[i - k:i])
        j += 1
        i += 1
    return s / j


def mean(x):
    return float(sum(x)) / max(len(x), 1)


def multiply(x, y):
    return [i * j for i, j in zip(x, y)]


def coef(y):
    n = len(y)
    x = range(n)

    # mean of x and y vector
    m_x, m_y = mean(x), mean(y)

    # calculating cross-deviation and deviation about x
    tmp = n * m_y * m_x
    SS_xy = sum([i - tmp for i in multiply(x, y)])
    tmp = n * m_x * m_x

    SS_xx = sum([i - tmp for i in multiply(x, x)])

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return b_0, b_1


def get_linear_reg(l, k):
    # 计算滑动窗口的线性回归
    i = k
    s = []
    while i < len(l):
        s.append(sum(l[i - k:i]))
        i += 1
    b_0, b_1 = coef(s)
    return int(abs(b_0 + b_1 * i))


def predict(ecs_lines, pred_start, pred_end, flavors):
    result = dict()
    train_start = datetime.datetime.strptime(ecs_lines[0].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    train_end = datetime.datetime.strptime(ecs_lines[-1].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    total_days = (train_end - train_start).days + 1
    predict_days = (pred_end - pred_start).days + 1

    d = dict()

    for f in flavors:
        d[f] = [0] * total_days

    get_series(ecs_lines, d, train_start)

    for f in flavors:
        # result[f] = get_average(d[f], predict_days)
        result[f] = get_linear_reg(d[f], predict_days)

    return result
