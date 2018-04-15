# coding=utf-8
import datetime
import pred_m2
import pred_mov_avg
import pred_max
import pred_total_avg


def predict(ecs_lines, pred_start, pred_end, flavors):
    result_m2 = pred_m2.predict(ecs_lines, pred_start, pred_end, flavors)
    result_mov_avg = pred_mov_avg.predict(ecs_lines, pred_start, pred_end, flavors)
    result_max = pred_max.predict(ecs_lines, pred_start, pred_end, flavors)
    result_total_avg = pred_total_avg.predict(ecs_lines, pred_start, pred_end, flavors)
    result = dict()
    for f in flavors:
        # result[f] = int((result_m2[f] + result_mov_avg[f] + result_max[f]) / 3)
        result[f] = int((1.3 * result_mov_avg[f] + result_m2[f]) / 2)
    return result
