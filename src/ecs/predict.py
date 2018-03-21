# coding=utf-8
import datetime


def total_num(ecs_lines):
    d = dict()
    for l in ecs_lines:
        id, k, t = l.split("\t")
        if k in d:
            d[k] += 1
        else:
            d[k] = 1
    return d


def predict(ecs_lines, pred_start, pred_end, flavors):
    result = dict()
    train_start = datetime.datetime.strptime(ecs_lines[0].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    train_end = datetime.datetime.strptime(ecs_lines[-1].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    total_days = (train_end - train_start).days
    predict_days = (pred_end - pred_start).days

    fd = total_num(ecs_lines)  # 统计
    for f in flavors:
        result[f] = int(fd[f] * float(predict_days) / total_days)
    return result
