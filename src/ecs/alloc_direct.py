# coding=utf-8


def assign(physical, flavors):
    fs = sorted(flavors, key=lambda x: x.id, reverse=True)
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
