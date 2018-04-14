# coding=utf-8
from head import Flavor


def dp_cpu(CPU, MEM, fs):
    n = len(fs)
    # 第一个值表示总体利用率，第二个值表示CPU用量
    dp = [[[0, 0] for k in range(n + 1)] for j in range(MEM + 1)]
    # print dp
    for j in range(1, MEM + 1):
        for k in range(1, n + 1):
            f = fs[k - 1]
            if j >= f.mem and CPU >= dp[j - f.mem][k - 1][1] + f.cpu and dp[j - f.mem][k - 1][0] + f.cpu * 1.0 / CPU + f.mem * 1.0 / MEM > dp[j][k - 1][0]:
                dp[j][k][0] = dp[j - f.mem][k - 1][0] + f.cpu * 1.0 / CPU + f.mem * 1.0 / MEM
                dp[j][k][1] = dp[j - f.mem][k - 1][1] + f.cpu
            else:
                dp[j][k][0] = dp[j][k - 1][0]
                dp[j][k][1] = dp[j][k - 1][1]
            if dp[j][k][0] == 2:
                return dp[j][k][1], j, k, dp
    return dp[MEM][n][1], MEM, n, dp


def dp_mem(CPU, MEM, fs):
    n = len(fs)
    # 第一个值表示总体利用率，第二个值表示MEM用量
    dp = [[[0,0] for k in range(n + 1)] for j in range(CPU + 1)]
    for j in range(1, CPU + 1):
        for k in range(1, n + 1):
            f = fs[k - 1]
            if j >= f.cpu and MEM >= dp[j - f.cpu][k - 1][1] + f.mem and dp[j - f.cpu][k - 1][0] + f.cpu * 1.0 / CPU + f.mem * 1.0 / MEM > dp[j][k - 1][0]:
                dp[j][k][0] = dp[j - f.cpu][k - 1][0] + f.cpu * 1.0 / CPU + f.mem * 1.0 / MEM
                dp[j][k][1] = dp[j - f.cpu][k - 1][1] + f.mem
            else:
                dp[j][k][0] = dp[j][k - 1][0]
                dp[j][k][1] = dp[j][k - 1][1]
            if dp[j][k][0] == 2:
                return j, MEM, k, dp
    return CPU, dp[CPU][n][1], n, dp


def assign(opt_type, physical, flavors):
    CPU, MEM = physical[0], physical[1]
    fs = []
    for f in flavors:
        for i in range(f.num):
            fs.append(Flavor(f.name, f.cpu, f.mem))
    if opt_type == "CPU":
        fs.sort(key=lambda x: (-x.cpu, -x.mem))
    else:
        fs.sort(key=lambda x: (-x.mem, -x.cpu))
    number = 0
    plan = dict()
    while fs:
        number += 1
        plan[number] = dict()
        n = len(fs)
        # print n
        label = [1] * n  # 表示某台虚拟机还未被分配
        if opt_type == "CPU":
            C, M, K, dp = dp_cpu(CPU, MEM, fs)
            # print dp[M][K][0]
            for k in range(K, 0, -1):
                if dp[M][k][0] != dp[M][k - 1][0]:
                    f = fs[k - 1]
                    label[k - 1] = 0
                    M -= f.mem
                    if f.name in plan[number]:
                        plan[number][f.name] += 1
                    else:
                        plan[number][f.name] = 1
            fs = [f for i, f in zip(label, fs) if i]
        else:
            C, M, K, dp = dp_mem(CPU, MEM, fs)
            # print dp[C][K][0]
            for k in range(K, 0, -1):
                if dp[C][k] != dp[C][k - 1]:
                    f = fs[k - 1]
                    label[k - 1] = 0
                    C -= f.cpu
                    if f.name in plan[number]:
                        plan[number][f.name] += 1
                    else:
                        plan[number][f.name] = 1
            fs = [f for i, f in zip(label, fs) if i]

    result = [number]
    for i in plan:
        tmp = "{} ".format(i)
        for k, v in sorted(plan[i].items()):
            tmp += "{} {} ".format(k, v)
        result.append(tmp)
    return result


if __name__ == "__main__":
    assign("CPU", (7, 16), [
        Flavor("flavor1", 1, 1, 1),
        Flavor("flavor2", 1, 2, 3),
        Flavor("flavor3", 1, 4, 4),
        Flavor("flavor4", 1, 2, 2),
        Flavor("flavor5", 1, 2, 4),
    ])
