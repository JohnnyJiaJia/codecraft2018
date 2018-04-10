class Flavor(object):
    def __init__(self, name, cpu, mem, num=0):
        self.name = name
        self.id = int(name[6:])
        self.cpu = int(cpu)
        self.mem = int(mem)
        self.num = num

    def __unicode__(self):
        return "{},{},{}".format(self.name, self.cpu, self.mem)

    def __repr__(self):
        return "{},{},{}".format(self.name, self.cpu, self.mem)
