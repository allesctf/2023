import sys

from tpu import *

# connect up parts to a bus.. layouting not important

# we designate X0 Y0 as the input port from the bus
# we designate X1 Y0 as the output port to the bus

bus_upper_out_port = """
start:
    mov RIGHT, ACC
    jne {addr}, fwd
    mov {addr}, DOWN
    mov RIGHT, DOWN
    mov RIGHT, DOWN
    mov RIGHT, DOWN
    mov RIGHT, DOWN
    jmp start
fwd:
    mov ACC, LEFT
    mov RIGHT, LEFT
    mov RIGHT, LEFT
    mov RIGHT, LEFT
    mov RIGHT, LEFT
"""

bus_lower_out_port = """
start:
    mov ANY, ACC
    jne {addr}, fwd
    mov ANY, DOWN
    mov ANY, DOWN
    mov ANY, DOWN
    mov ANY, DOWN
    jmp start
fwd:
    mov ACC, RIGHT
    mov LEFT, RIGHT
    mov LEFT, RIGHT
    mov LEFT, RIGHT
    mov LEFT, RIGHT
"""

bus_lower_in_port = """
start:
    mov ANY, ACC
    sav
    mov ANY, ACC
    jne {addr}, fwd
    swp
    mov ACC, UP
    mov ACC, RIGHT
    mov {addr}, UP
    mov {addr}, RIGHT
    mov DOWN, ACC
    mov ACC, UP
    mov ACC, RIGHT
    mov DOWN, ACC
    mov ACC, UP
    mov ACC, RIGHT
    mov DOWN, ACC
    mov ACC, UP
    mov ACC, RIGHT
    jmp start
fwd:
    swp
    mov ACC, RIGHT
    swp
    mov ACC, RIGHT
    mov LEFT, RIGHT
    mov LEFT, RIGHT
    mov LEFT, RIGHT
"""

bus_lower_rail = """
mov ANY, RIGHT
"""

bus_upper_rail = """
mov ANY, LEFT
"""

bus_rail_end = """
mov ANY, NIL
"""

def does_collide(main, offx, part):
    for (x,y),_ in part["tpus"].items():
        if (x+offx,y) in main["tpus"]:
            return True
    dirs = {"UP": (0, -1), "RIGHT": (1, 0), "DOWN": (0, 1), "LEFT": (-1, 0)}
    for port in ("stdin", "stdout"):
        if port in part:
            x,y,d = part[port]
            dx,dy = dirs[d]
            if (x+offx+dx,y+dy) in main["tpus"]:
                return True
        if port in main:
            x,y,d = main[port]
            dx,dy = dirs[d]
            if (x+dx-offx,y+dy) in part["tpus"]:
                return True
    return False

def add_part(main, main_maxx, bus_ports, part):
    portx = main_maxx
    while portx in bus_ports or portx+1 in bus_ports or does_collide(main, portx, part):
        portx += 1
    bus_ports[portx] = ("in", part["addr"])
    bus_ports[portx+1] = ("out", part["addr"])
    for (x,y),ls in part["tpus"].items():
        main["tpus"][(x+portx,y)] = ls
    if "stdin" in part:
        assert("stdin" not in main)
        x,y,d = part["stdin"]
        main["stdin"] = (portx+x,y,d)
    if "stdout" in part:
        assert("stdout" not in main)
        x,y,d = part["stdout"]
        main["stdout"] = (portx+x,y,d)
    return portx + 4

def tolines(asm):
    return asm.strip("\n").split("\n")

def apply(part, transforms):
    old_tpus = part["tpus"]
    part["tpus"] = TPUDict({})
    for (x,y),ls in old_tpus.items():
        nx = transforms[0](x, y)
        ny = transforms[1](x, y)
        part["tpus"][(nx,ny)] = ls

def rotate(part, r90=0):
    dirs = ("UP", "RIGHT", "DOWN", "LEFT")
    transforms = (
        (lambda x,_: x, lambda _,y: y),
        (lambda _,y: -y, lambda x,_: x),
        (lambda x,_: -x, lambda _,y: -y),
        (lambda _,y: y, lambda x,_: -x),
    )
    apply(part, transforms[r90])
    for _,ls in part["tpus"].items():
        for li,l in enumerate(ls):
            for d in dirs:
                l = l.replace(d, d.upper())
            for i,d in enumerate(dirs):
                nd = dirs[(i+r90)%len(dirs)]
                l = l.replace(d, nd.lower())
            for d in dirs:
                l = l.replace(d.lower(), d)
            ls[li] = l

def add_ports(main, bus_ports):
    for x,(dir,addr) in bus_ports.items():
        dir,addr = bus_ports[x]
        if dir == "in":
            main["tpus"][(x,-2)] = tolines(bus_upper_out_port.format(addr=addr))
            main["tpus"][(x,-1)] = tolines(bus_lower_out_port.format(addr=addr))
        else:
            main["tpus"][(x,-2)] = tolines(bus_upper_rail)
            main["tpus"][(x,-1)] = tolines(bus_lower_in_port.format(addr=addr))

def add_rail(main, bus_ports):
    bus_start = min(bus_ports)
    bus_end = max(bus_ports) + 1
    for x in range(bus_start, bus_end + 1):
        if x not in bus_ports:
            main["tpus"][(x,-2)] = tolines(bus_upper_rail)
            main["tpus"][(x,-1)] = tolines(bus_lower_rail)
    main["tpus"][(bus_start-1,-1)] = tolines(bus_rail_end)
    main["tpus"][(bus_start-1,-2)] = tolines(bus_rail_end)
    main["tpus"][(bus_end+1,-1)] = tolines(bus_rail_end)
    main["tpus"][(bus_end+1,-2)] = tolines(bus_rail_end)

if __name__ == "__main__":
    main = { "tpus": TPUDict({}) }
    files = sys.argv[2:]
    if "--" in files:
        split = files.index("--")
    else:
        split = None

    bus_ports = {}
    main_maxx = 0
    for arg in files[:split]:
        main_maxx = add_part(main, main_maxx,
            bus_ports, parse(open(arg).read()))
    add_ports(main, bus_ports)

    if split is not None:
        rotate(main, 2)
        apply(main, (lambda x,_: x, lambda _,y: y-3))

        all_ports = {-k:v for k,v in bus_ports.items()}
        main_maxx = min(all_ports)
        for arg in files[split+1:]:
            main_maxx = add_part(main, main_maxx,
                all_ports, parse(open(arg).read()))
        add_ports(main, {k:v for k,v in all_ports.items() if -k not in bus_ports})
        add_rail(main, all_ports)
    else:
        add_rail(main, bus_ports)

    write(main, sys.argv[1])
