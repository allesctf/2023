from tpu import *
import sys, string, random

random.seed(133713371337)

main = parse(open(sys.argv[1]).read())

def isint(op):
    try:
        int(op, 0)
        return True
    except:
        return False

main["stdin"] = [str(v).lower() for v in main["stdin"]]
main["stdout"] = [str(v).lower() for v in main["stdout"]]

for _,ls in main["tpus"].items():
    labelmap = {}
    for li,l in enumerate(ls):
        l = l.split("#",1)[0].strip().lower()
        if ":" in l:
            name = l.strip().split(":")[0]
            labelmap[name] = "".join([random.choice(string.ascii_lowercase) for _ in range(8)])
        ls[li] = l
    while "" in ls:
        ls.remove("")
    for li,l in enumerate(ls):
        if l == "": continue
        ops = l.replace(",", " ").split()
        cmd = ops[0]
        if len(ops) > 1:
            nops = []
            for op in ops[1:]:
                if op in labelmap:
                    nops.append(labelmap[op])
                elif isint(op):
                    nops.append(hex(int(op,0)))
                else:
                    nops.append(op)
            ls[li] = "\t" + cmd + " " + ",".join(nops)
        elif ":" in cmd:
            ls[li] = labelmap[cmd[:-1]] + ":"
        else:
            ls[li] = "\t" + cmd


write(main, sys.argv[2])
