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


def opt_cpu(p, l0, l1, l2):
    result = []
    num = 0  # num of physical
    cpu_limit, mem_limit = p[0], p[1]
    cpu, mem = cpu_limit, mem_limit
    while l0 or l1 or l2:
        if mem / cpu > 2:
            while l0:
                pass
        while l2:
            pass
        while l1:
            pass
    return result


def opt_mem(p, l0, l1, l2):
    result = []
    return result


def assign(opt, p, fs):
    l0 = []
    l1 = []
    l2 = []
    for f in fs:
        f_name, fn, fn_c, cpu, mem, cnt = f
        if cnt:
            if fn_c == 0:
                l0.append([fn, cpu, mem, cnt])
            elif fn_c == 1:
                l1.append([fn, cpu, mem, cnt])
            else:
                l2.append([fn, cpu, mem, cnt])
    l0.sort(key=lambda x: -x[0])
    l1.sort(key=lambda x: -x[0])
    l2.sort(key=lambda x: -x[0])
    print l0
    print l1
    print l2
    if opt == "CPU":
        return opt_cpu(p, l0, l1, l2)
    else:
        return opt_mem(p, l0, l1, l2)


def direct_assign(physical, flavors):
    # 对结果直接分配
    fs = [f for f in flavors if f[-1] > 0]
    if len(fs) <= 0:
        return ["0"]
    n = 1
    CPU, MEM = physical[0], physical[1]
    cpu, mem = CPU, MEM
    plan = dict()
    plan[n] = dict()
    for f in fs:
        for i in range(f[-1]):
            if f[-3] < cpu and f[-2] < mem:
                cpu -= f[-3]
                mem -= f[-2]
                if f[0] in plan[n]:
                    plan[n][f[0]] += 1
                else:
                    plan[n][f[0]] = 1
            else:
                n += 1
                plan[n] = dict()
                cpu, mem = CPU, MEM
                cpu -= f[-3]
                mem -= f[-2]
                plan[n][f[0]] += 1
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
    # print physical
    flavor_num = int(input_lines[2].strip())
    # print flavor_num
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
    # print flavors
    # print predict_num
    result.append(predict_num)
    for f in flavors:
        result.append("{} {}".format(f[0], f[-1]))
    result.append("")
    optimal_type = input_lines[-4].strip()
    # print optimal_type
    # d = average_by_day(ecs_lines)
    # print input_lines
    # result += assign(optimal_type, physical, flavors)
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
    return result
