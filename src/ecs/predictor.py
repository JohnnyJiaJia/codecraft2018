# coding=utf-8
import datetime
import alloc
import predict


class Flavor(object):
    def __init__(self, name, cpu, mem):
        self.name = name
        self.id = int(name[6:])
        self.cpu = int(cpu)
        self.mem = int(mem) / 1024
        self.num = 0


def predict_vm(ecs_lines, input_lines):
    start = datetime.datetime.strptime(input_lines[-2].strip(), "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(input_lines[-1].strip(), "%Y-%m-%d %H:%M:%S")
    flavor_num = int(input_lines[2].strip())
    # print flavor_num
    fs = []
    for l in input_lines[3:3 + flavor_num]:
        f, cpu, mem = l.strip().split()
        fl = Flavor(f, cpu, mem)
        fs.append(fl)

    # 预测函数需要返回包含各个flavor的字典
    fd = predict.predict(ecs_lines, start, end, [f.name for f in fs])

    print fd

    for f in fs:
        f.num = fd[f.name]

    result = [sum(fd.values())]
    for f in fs:
        result.append("{} {}".format(f.name, f.num))
    result.append("")
    opt_type = input_lines[-4].strip()
    physical = [int(i) for i in input_lines[0].strip().split()]

    result += alloc.direct_assign(physical, fs)
    # result += alloc.alloc(opt_type, physical, flavors)
    return result
