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
    fs = sorted(fs, key=lambda x: x[0], reverse=True)
    if len(fs) <= 0:
        return ["0"]
    n = 1
    CPU, MEM = physical[0], physical[1]
    cpu, mem = CPU, MEM
    plan = dict()
    plan[n] = dict()
    for f in fs:
        for i in range(f[-1]):
            if f[-3] <= cpu and f[-2] <= mem:
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
                plan[n][f[0]] = 1
    result = [len(plan)]
    for i in plan:
        tmp = "{} ".format(i)
        for k, v in sorted(plan[i].items()):
            tmp += "{} {} ".format(k, v)
        result.append(tmp)
    return result


def can_alloc(fs, cpu, mem):
    for i in range(len(fs)):
        if fs[i][3] < cpu and fs[i][4] < mem:
            return i
    return None


def alloc(opt_type, physical, flavors):
    CPU, MEM = physical[0], physical[1]
    R = MEM * 1.0 / CPU
    fs = [f for f in flavors if f[-1] > 0]
    ff = []
    for f in fs:
        ff += [f] * f[-1]
    print ff
    fs = ff
    f_cpu = [f for f in fs if f[2] < R]
    f_mem = [f for f in fs if f[2] > R]
    f_cpu = sorted(f_cpu, key=lambda x: (x[2], -x[1]))  # 最极端、最大的优先
    f_mem = sorted(f_mem, key=lambda x: (-x[2], -x[1]))  #
    print f_cpu
    print f_mem

    n = 1
    cpu, mem = CPU, MEM
    plan = dict()
    plan[1] = dict()
    while True:
        if f_mem and f_cpu:  # 两种都有，就要通过调节来放
            r = mem * 1.0 / cpu
            i = can_alloc(f_cpu, cpu, mem)
            j = can_alloc(f_mem, cpu, mem)
            if i is None and j is None:
                n += 1
                plan[n] = dict()
                cpu, mem = CPU, MEM
            elif i is None or j is None:
                fs, k = (f_mem, j) if (i is None) else (f_cpu, i)
                f = fs[k]
                cpu -= f[3]
                mem -= f[4]
                fs.pop(k)
                if f[0] in plan[n]:
                    plan[n][f[0]] += 1
                else:
                    plan[n][f[0]] = 1
            else:
                # 当两个都能分配时才有意义
                if r == R:
                    fs, k = (f_mem, j) if opt_type == "CPU" else (f_cpu, i)
                else:
                    # r <= R 说明cpu密集
                    fs, k = (f_mem, j) if r > R else (f_cpu, i)
                f = fs[k]
                cpu -= f[3]
                mem -= f[4]
                fs.pop(k)
                if f[0] in plan[n]:
                    plan[n][f[0]] += 1
                else:
                    plan[n][f[0]] = 1

        elif f_mem or f_cpu:
            fs = f_mem if f_mem else f_cpu
            i = can_alloc(fs, cpu, mem)
            if i is None:
                n += 1
                plan[n] = dict()
                cpu, mem = CPU, MEM
            else:
                f = fs[i]
                cpu -= f[3]
                mem -= f[4]
                fs.pop(0)
                if f[0] in plan[n]:
                    plan[n][f[0]] += 1
                else:
                    plan[n][f[0]] = 1
        else:
            # 都分配完了
            break

    result = [len(plan)]
    for i in plan:
        tmp = "{} ".format(i)
        for k, v in sorted(plan[i].items()):
            tmp += "{} {} ".format(k, v)
        result.append(tmp)
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
        cpu, mem = int(cpu), int(mem) / 1024
        n = int(fd[f] * float(predict_days) / total_days)
        predict_num += n
        fn = int(f[6:])
        flavors.append([f, fn, mem / cpu, cpu, mem, n])
    result.append(predict_num)
    for f in flavors:
        result.append("{} {}".format(f[0], f[-1]))
    result.append("")
    opt_type = input_lines[-4].strip()
    # result += direct_assign(physical, flavors)
    result += alloc(opt_type, physical, flavors)
    return result
