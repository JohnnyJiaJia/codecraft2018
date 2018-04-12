# from alloc_dp import assign
# from alloc_direct import assign
from alloc_exhaustive import assign
import os
from head import Flavor

# 6 13 27 63 118 57

dir = "../../deploy_test_cases"


def get_flavor(s):
    name, n = s.strip().split(":")
    n = int(n)
    f_id = int(name[6:])
    cpu = 2 ** ((f_id-1) / 3)
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
    with open(dir + "/" + f_name) as f:
        ls = f.readlines()
        CPU, MEM, _ = ls[0].strip().split()
        CPU, MEM = int(CPU), int(MEM)
        opt_type = ls[2].strip()
        num = int(ls[4].strip())
        fs = [get_flavor(l) for l in ls[6:6 + num]]
        result = assign(opt_type, (CPU, MEM), fs)
        for i in result:
            print i
