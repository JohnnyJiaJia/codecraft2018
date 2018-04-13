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
    s = []
    while i < len(l):
        s.append(sum(l[i - k:i]))
        i += 1
    totalsum = 0
    for j in range(len(s)):
        totalsum += sum(s[j:])/(len(s)-j)
    return totalsum/len(s)

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
        result[f] = get_average(d[f], predict_days)
        # result[f] = get_linear_reg(d[f], predict_days)

    return result
