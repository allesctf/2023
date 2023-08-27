
class TPUDict(dict):
    def __setattr__(self, __name, __value):
        if __name in self.__dict__:
            raise ValueError("Duplicate tpu location")
        return super().__setattr__(__name, __value)

def parse(asm):
    part = { "tpus": TPUDict({}) }
    current = None
    lines = asm.strip().split("\n")
    getxy = lambda l: [int(v[1:]) for v in l.split()[1:3]]
    for l in lines:
        if l.startswith("stdin"):
            part["stdin"] = [*getxy(l.rsplit(" ", 1)[0]), l.split()[-1]]
        elif l.startswith("stdout"):
            part["stdout"] = [*getxy(l.rsplit(" ", 1)[0]), l.split()[-1]]
        elif l.startswith("tpu"):
            x,y = getxy(l)
            part["tpus"][(x, y)] = []
            current = part["tpus"][(x,y)]
        elif l.startswith("end"):
            if "addr" not in part:
                part["addr"] = int(current[0].strip().split()[-1], 0)
            continue
        elif l != "":
            assert(current is not None)
            current.append(l)
    return part

def write(part, filepath):
    with open(filepath, "w+") as f:
        if "stdin" in part:
            x,y,d = part["stdin"]
            f.write(f"stdin X{x} Y{y} {d}\n")
        if "stdout" in part:
            x,y,d = part["stdout"]
            f.write(f"stdout X{x} Y{y} {d}\n")
        f.write("\n")
        for (x,y),ls in part["tpus"].items():
            f.write(f"tpu X{x} Y{y}\n")
            for l in ls:
                f.write(f"{l}\n")
            f.write("end\n")
            f.write("\n")


