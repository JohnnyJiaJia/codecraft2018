# coding=utf-8
import datetime


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


def ma_predict(ecs_lines, pred_start, pred_end, flavors):
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

    return result


def total_num(ecs_lines):
    d = dict()
    for l in ecs_lines:
        id, k, t = l.strip().split("\t")
        if k in d:
            d[k] += 1
        else:
            d[k] = 1
    return d


def ta_predict(ecs_lines, pred_start, pred_end, flavors):
    result = dict()
    train_start = datetime.datetime.strptime(ecs_lines[0].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    train_end = datetime.datetime.strptime(ecs_lines[-1].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    total_days = (train_end - train_start).days + 1
    predict_days = (pred_end - pred_start).days + 1

    d = total_num(ecs_lines)

    for f in flavors:
        result[f] = int(d[f] * 1.0 / total_days * predict_days)
    return result


def predict(ecs_lines, pred_start, pred_end, flavors):
    return ta_predict(ecs_lines, pred_start, pred_end, flavors)
