# coding=utf-8

def direct_assign(physical, flavors):
    fs = [f for f in flavors if f.num > 0]
    fs = sorted(fs, key=lambda x: x.id, reverse=True)
    if len(fs) <= 0:
        return ["0"]
    n = 1
    CPU, MEM = physical[0], physical[1]
    cpu, mem = CPU, MEM
    plan = dict()
    plan[n] = dict()
    for f in fs:
        for i in range(f.num):
            if f.cpu <= cpu and f.mem <= mem:
                cpu -= f.cpu
                mem -= f.mem
                if f.name in plan[n]:
                    plan[n][f.name] += 1
                else:
                    plan[n][f.name] = 1
            else:
                n += 1
                plan[n] = dict()
                cpu, mem = CPU, MEM
                cpu -= f.cpu
                mem -= f.mem
                plan[n][f.name] = 1
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
    fs = ff
    f_cpu = [f for f in fs if f[2] < R]
    f_mem = [f for f in fs if f[2] > R]
    f_cpu = sorted(f_cpu, key=lambda x: (x[2], -x[1]))  # 最极端、最大的优先
    f_mem = sorted(f_mem, key=lambda x: (-x[2], -x[1]))  #
    # print f_cpu
    # print f_mem
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
                fs.pop(i)
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
