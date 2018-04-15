# coding=utf-8
import datetime
# import alloc_direct as alloc
import alloc_dp2 as alloc
# import pred_total_avg as pred
# import pred_mov_avg as pred
# import pred_m2 as pred
# import pred_max as pred
import pred_comb as pred

from head import Flavor


def predict_vm(ecs_lines, input_lines):
    # flavor种类数量
    flavor_num = int(input_lines[2].strip())

    fs = []
    for l in input_lines[3:3 + flavor_num]:
        f, cpu, mem = l.strip().split()
        fl = Flavor(f, cpu, int(mem) / 1024)
        fs.append(fl)

    start = datetime.datetime.strptime(input_lines[6 + flavor_num].strip(), "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(input_lines[7 + flavor_num].strip(), "%Y-%m-%d %H:%M:%S")

    opt_type = input_lines[4 + flavor_num].strip()

    # 替换预测方式，在import中修改
    fd = pred.predict(ecs_lines, start, end, [f.name for f in fs])

    for f in fs:
        f.num = fd[f.name]

    result = [sum(fd.values())]
    for f in fs:
        result.append("{} {}".format(f.name, f.num))
    result.append("")

    physical = [int(i) for i in input_lines[0].strip().split()]

    fs = [f for f in fs if f.num > 0]

    # 替换分配方式，在import中修改
    result += alloc.assign(opt_type, physical, fs)

    return result
