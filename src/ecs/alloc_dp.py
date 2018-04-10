# coding=utf-8
from head import Flavor


def assign(opt_type, physical, flavors):
    CPU, MEM = physical[0], physical[1]
    fs = []
    for f in flavors:
        for i in range(f.num):
            fs.append(Flavor(f.name, f.cpu, f.mem))
    number = 0
    plan = dict()
    while fs:
        number += 1
        plan[number] = dict()
        n = len(fs)
        dp = [[[0 for k in range(n + 1)] for j in range(MEM + 1)] for i in range(CPU + 1)]
        # 可以修改成二维的
        for i in range(1, CPU + 1):
            for j in range(1, MEM + 1):
                for k in range(1, n + 1):
                    f = fs[k - 1]
                    v = f.cpu if opt_type == "CPU" else f.mem
                    if i >= f.cpu and j >= f.mem:
                        dp[i][j][k] = max(dp[i - f.cpu][j - f.mem][k - 1] + v, dp[i][j][k - 1])
                    else:
                        dp[i][j][k] = dp[i][j][k - 1]
        # 恢复选择项
        C, M = CPU, MEM
        for k in range(n, 0, -1):
            if dp[C][M][k] != dp[C][M][k - 1]:
                f = fs.pop(k - 1)
                C -= f.cpu
                M -= f.mem
                if f.name in plan[number]:
                    plan[number][f.name] += 1
                else:
                    plan[number][f.name] = 1
        pass
        # print (CPU - C) * 1.0 / CPU, (MEM - M) * 1.0 / MEM  # 打印利用率

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
