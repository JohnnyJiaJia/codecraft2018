# coding=utf-8
import datetime
import alloc
import predict


def predict_vm(ecs_lines, input_lines):
    start = datetime.datetime.strptime(input_lines[-2].strip(), "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(input_lines[-1].strip(), "%Y-%m-%d %H:%M:%S")
    flavor_num = int(input_lines[2].strip())
    # print flavor_num
    fs = []
    for l in input_lines[3:3 + flavor_num]:
        f, cpu, mem = l.strip().split()
        cpu, mem = int(cpu), int(mem) / 1024
        fn = int(f[6:])
        fs.append([f, fn, mem / cpu, cpu, mem, 0])

    # 预测函数需要返回包含各个flavor的字典
    fd = predict.predict(ecs_lines, start, end, [f[0] for f in fs])

    for f in fs:
        f[-1] = fd[f[0]]
    result = [sum(fd.values())]
    for f in fs:
        result.append("{} {}".format(f[0], f[-1]))
    result.append("")
    opt_type = input_lines[-4].strip()
    physical = [int(i) for i in input_lines[0].strip().split()]

    result += alloc.direct_assign(physical, fs)
    # result += alloc.alloc(opt_type, physical, flavors)
    return result
