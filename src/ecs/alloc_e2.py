# coding=utf-8
from head import Flavor

def assign(opt_type, physical, flavors):
    CPU, MEM = physical[0], physical[1]
    fs, plan= [], []
    totalCPU, totalMEM = 0, 0
    for f in flavors:
        for i in range(f.num):
            fs.append(Flavor(f.name, f.cpu, f.mem))
            plan.append(-1)
            totalCPU += f.cpu
            totalMEM += f.mem
    pnum = max((totalCPU+CPU-1)/CPU, (totalMEM+MEM-1)/MEM)
    pcpu = [CPU for j in range(pnum)]
    pmem = [MEM for j in range(pnum)]
    res = [[] for j in range(pnum)]

    def put(i):
        if i == len(fs):
            for k in range(len(plan)):
                res[plan[k]].append(fs[k].id)
            return True
        for j in range(pnum):
            if fs[i].cpu <= pcpu[j] and fs[i].mem <= pmem[j]:
                plan[i] = j
                pcpu[j] -= fs[i].cpu
                pmem[j] -= fs[i].mem
                if put(i+1):
                    return True
                pcpu[j] += fs[i].cpu
                pmem[j] += fs[i].mem
                plan[i] = -1
        return False

    put(0)
    while(len(res) == 0):
        pnum += 1
        pcpu.append(CPU)
        pmem.append(MEM)
        put(0)

    result = [pnum]
    for j in range(pnum):
        tmp = "{}".format(j + 1)
        rset = set(res[j])
        for item in rset:
            tmp += " flavor{} {}".format(item, res[j].count(item))
        result.append(tmp)
    return result