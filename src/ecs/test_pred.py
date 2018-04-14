# coding=utf-8
import sys
# from pred_max import predict
from pred_m2 import predict
# from pred_mov_avg import predict
import numpy as np

import datetime

dir = "../../pred_test_cases"

flavors = ["flavor{}".format(i) for i in range(1, 16)]


def get_t(l):
    fid, name, t = l.strip().split("\t")
    return datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")


def test_pred(ecs_lines, days=7):
    l = ecs_lines[-1]
    fid, name, t = l.strip().split("\t")
    pred_end = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    pred_end = datetime.datetime(pred_end.year, pred_end.month, pred_end.day) + datetime.timedelta(days=1)
    delta = datetime.timedelta(days=days)
    pred_start = pred_end - delta
    bln = 0
    for ln in range(len(ecs_lines) - 1, -1, -1):
        if get_t(ecs_lines[ln]) < pred_start:
            bln = ln + 1
            break
    train_data, test_data = ecs_lines[:bln], ecs_lines[bln:]
    real = count(flavors, train_data)
    pred = predict(train_data, pred_start, pred_end, flavors)
    print accuracy(pred, real)


def count(flavors, lines):
    d = dict()
    for f in flavors:
        d[f] = 0
    for l in lines:
        fid, name, t = l.split("\t")
        if name in d:
            d[name] += 1
    return d


def accuracy(d1, d2):
    a1 = np.array([d1[f] for f in flavors])
    a2 = np.array([d2[f] for f in flavors])
    print a1
    print a2
    f1 = np.sqrt(np.mean((a1 - a2) ** 2))
    f2 = np.sqrt(np.mean(a1 ** 2)) + np.sqrt(np.mean(a2 ** 2))
    return 1 - f1 / f2


# f_names = ["data_2015_2.txt", "data_2015_3.txt"]
f_names = ["data_2015_12.txt","data_2016_1.txt"]

lines = []
for f_name in f_names:
    with open(dir + "/" + f_name) as f:
        lines += f.readlines()
test_pred(lines, 7)
