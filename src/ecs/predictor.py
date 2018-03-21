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


def direct_assign(physical, flavors):
    fs = [f for f in flavors if f[-1] > 0]
    fs = sorted(fs, key=lambda x: x[0],reverse=True)
    if len(fs) <= 0:
        return ["0"]
    n = 1
    CPU, MEM = physical[0], physical[1]
    cpu, mem = CPU, MEM
    plan = dict()
    plan[n] = dict()
    # for f in fs:
    #     for i in range(f[-1]):
    #         if f[-3] < cpu and f[-2] < mem:
    #             cpu -= f[-3]
    #             mem -= f[-2]
    #             if f[0] in plan[n]:
    #                 plan[n][f[0]] += 1
    #             else:
    #                 plan[n][f[0]] = 1
    #         else:
    #             n += 1
    #             plan[n] = dict()
    #             cpu, mem = CPU, MEM
    #             cpu -= f[-3]
    #             mem -= f[-2]
    #             plan[n][f[0]] += 1
    result = [len(plan)]
    for i in plan:
        tmp = "{} ".format(i)
        for k, v in sorted(plan[i].items()):
            tmp += "{} {} ".format(k, v)
        result.append(tmp)
    return result


def predict_vm_hehe(ecs_lines, input_lines):
    result = []
    s = datetime.datetime.strptime(ecs_lines[0].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    e = datetime.datetime.strptime(ecs_lines[-1].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    total_days = (e - s).days
    start = datetime.datetime.strptime(input_lines[-2].strip(), "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(input_lines[-1].strip(), "%Y-%m-%d %H:%M:%S")
    predict_days = (end - start).days
    physical = [int(i) for i in input_lines[0].strip().split()]
    physical[1] = physical[1]
    flavor_num = int(input_lines[2].strip())
    flavors = []
    fd = total_num(ecs_lines)
    predict_num = 0
    for l in input_lines[3:3 + flavor_num]:
        f, cpu, mem = l.strip().split()
        n = int(fd[f] * float(predict_days) / total_days)
        predict_num += n
        fn = int(f[6:])
        fn_c = fn % 3
        flavors.append([f, fn, fn_c, int(cpu), int(mem) / 1024, n])
    result.append(predict_num)
    for f in flavors:
        result.append("{} {}".format(f[0], f[-1]))
    result.append("")
    result += direct_assign(physical, flavors)
    return result


def predict_vm(ecs_lines, input_lines):
    result = []
    s = datetime.datetime.strptime(ecs_lines[0].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    e = datetime.datetime.strptime(ecs_lines[-1].strip().split("\t")[-1], "%Y-%m-%d %H:%M:%S")
    total_days = (e - s).days
    start = datetime.datetime.strptime(input_lines[-2].strip(), "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(input_lines[-1].strip(), "%Y-%m-%d %H:%M:%S")
    predict_days = (end - start).days
    physical = [int(i) for i in input_lines[0].strip().split()]
    physical[1] = physical[1]
    # print physical
    flavor_num = int(input_lines[2].strip())
    # print flavor_num
    flavors = []
    fd = total_num(ecs_lines)  # 统计
    predict_num = 0
    for l in input_lines[3:3 + flavor_num]:
        f, cpu, mem = l.strip().split()
        n = int(fd[f] * float(predict_days) / total_days)
        predict_num += n
        fn = int(f[6:])
        fn_c = fn % 3
        flavors.append([f, fn, fn_c, int(cpu), int(mem) / 1024, n])
    result.append(predict_num)
    for f in flavors:
        result.append("{} {}".format(f[0], f[-1]))
    result.append("")
    result += direct_assign(physical, flavors)
    return result
