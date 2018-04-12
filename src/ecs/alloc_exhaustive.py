# coding=utf-8
import copy

def assign(opt_type, physical, flavors):
    fs = sorted(flavors, key=lambda x: x.id, reverse=True)
    totalcpu, totalmem = 0, 0
    for f in fs:
        totalcpu += f.num * f.cpu
        totalmem += f.num * f.mem
    minp = max(totalcpu/physical[0], totalmem/physical[1])+1

    f = []
    for ft in fs:
        f.append(ft.num)
    CPU = physical[0]
    MEM = physical[1]
    cur = [[0 for j in range(minp)] for i in range(len(fs))]
    res = copy.deepcopy(cur)
    flag = [0]

    def put(i, j):
        if flag[0] == 1:
            return
        if i == len(f):
            for i in range(len(fs)):
                for j in range(minp):
                    res[i][j] = cur[i][j]
            flag[0] = 1
            return
        if j+1 == minp:
            cur[i][j] = f[i]
            cpu = 0
            mem = 0
            for m in range(i + 1):
                cpu += cur[m][j] * fs[m].cpu
                mem += cur[m][j] * fs[m].mem
            if cpu <= CPU and mem <= MEM:
                temp = f[i]
                f[i] = 0
                put(i + 1, 0)
                f[i] = temp
            cur[i][j] = 0
        else:
            for k in range(0, f[i] + 1):
                cur[i][j] = k
                cpu = 0
                mem = 0
                for m in range(i + 1):
                    cpu += cur[m][j] * fs[m].cpu
                    mem += cur[m][j] * fs[m].mem
                if cpu <= CPU and mem <= MEM:
                    f[i] -= k
                    put(i, j + 1)
                    f[i] += k
                else:
                    cur[i][j] = 0
                    break
                cur[i][j] = 0
    put(0, 0)
    while flag[0] == 0:
        minp = minp + 1
        for i in range(len(cur)):
            cur[i].append(0)
            res[i].append(0)
        put(0, 0)

    result = [minp]
    for j in range(minp):
        tmp = "{} ".format(j+1)
        for i in range(len(f)):
            if res[i][j] != 0:
                tmp += "{} {} ".format(fs[i].name, res[i][j])
        result.append(tmp)
    return result