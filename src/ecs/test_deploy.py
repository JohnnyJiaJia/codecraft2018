# coding=utf-8
# from alloc_direct import assign
from alloc_dp2 import assign
# from alloc_dp4 import assign
import os
import time
import math
from head import Flavor

# 论坛结果
# case1：7
# case2：20
# case3：40
# case4：77
# case5：174
# case6：127

# 9 7
# 23 20
# 48 40
# 94 77
# 191 156
# 111 105

dir = "../../deploy_test_cases"


def get_flavor(s):
    name, n = s.strip().split(":")
    n = int(n)
    f_id = int(name[6:])
    cpu = 2 ** ((f_id - 1) / 3)
    tmp = f_id % 3
    if tmp == 0:
        mem = cpu * 4
    elif tmp == 1:
        mem = cpu
    else:
        mem = cpu * 2
    return Flavor(name, cpu, mem, n)


# f_names = [i for i in os.listdir(dir) if "case" in i]

f_names = ["case1.txt"]

for f_name in sorted(f_names):
    start_t = time.time()
    with open(dir + "/" + f_name) as f:
        ls = f.readlines()
        CPU, MEM, _ = ls[0].strip().split()
        CPU, MEM = int(CPU), int(MEM)
        opt_type = ls[2].strip()
        num = int(ls[4].strip())
        fs = [get_flavor(l) for l in ls[6:6 + num]]
        total_cpu = sum([f.num * f.cpu for f in fs])
        total_mem = sum([f.num * f.mem for f in fs])
        # print sum([f.num for f in fs])
        print math.ceil(max(total_cpu * 1.0 / CPU, total_mem * 1.0 / MEM))
        result = assign(opt_type, (CPU, MEM), fs)
        for i in result:
            print i
    print "运行时间", time.time() - start_t
