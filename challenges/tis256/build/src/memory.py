import sys

memory_block_start = """
    mov UP, LEFT

    mov UP, ACC
    mov UP, LEFT

    jne 0, is_write
    mov LEFT, DOWN
    mov 0, DOWN
    mov UP, DOWN
    mov LEFT, NIL
    jmp wrap

is_write:
    mov LEFT, DOWN
    mov 1, DOWN
    mov UP, ACC
    xor LEFT
    mov ACC, DOWN
    swp

wrap:
    mov DOWN, ACC
    xor LEFT
    mov LEFT, RIGHT
    mov ${{addr}}, RIGHT
    mov ${OP_ACK}, RIGHT
    mov ACC, RIGHT
    mov ${OP_NIL}, RIGHT
"""

memory_block_start_left = """
    mov RIGHT, ACC
    swp
    mov RIGHT, ACC
    mov ACC, RIGHT
    mov ACC, RIGHT
    mov ACC, RIGHT
    swp
    mov ACC, RIGHT
"""

memory_block_start_right = """
    mov LEFT, UP
"""

code_memory_cell = """
    mov 0x{val:02x}, ACC
    sav
start:
    mov {inp}, ACC
    jne {idx}, fwd
    mov {inp}, ACC
    jne 0, WRITE
    mov {inp}, NIL
    swp
    mov ACC, {inp}
    sav
    jmp start
write:
    mov {inp}, ACC
    swp
    mov ACC, {inp}
    jmp start
fwd:
    mov ACC, {outp}
    mov {inp}, {outp}
    mov {inp}, {outp}
    mov {outp}, {inp}
    jmp start
"""

pattern = """
#                   
#                   
# ##################
# #                #
# ################ #
#                  #
####################

"""
assert(pattern.count("#") == 64)
pattern = pattern.strip("\n").split("\n")

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

x,y = (0, 0)
seen = set()
seen.add((x,y))
path = [(x,y),]
while True:
    npos = None
    for dx,dy in dirs:
        nx,ny = x+dx,y+dy
        if nx < 0 or nx >= len(pattern[0]): continue
        if ny < 0 or ny >= len(pattern): continue
        if pattern[ny][nx] == "#" and (nx,ny) not in seen:
            npos = (nx,ny)
            break
    if npos is None:
        break
    x,y = npos
    seen.add((x,y))
    path.append((x,y))

class BlockMap(dict):
    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise ValueError("Already exists")
        super().__setattr__(key, value)

def gen_memory(blocks, start, idx_offset, depth, contents, dtype):
    opposite = { "UP": "DOWN", "LEFT": "RIGHT", "RIGHT": "LEFT", "DOWN": "UP" }
    ports = { (-1, 0): "LEFT", (0, 1): "DOWN", (1, 0): "RIGHT", (0, -1): "UP" }
    sx,sy = start
    maxi = 2**depth-1
    for i in range(2**depth):
        fix = lambda x,y: (-x,y) if dtype == "left" else (x,y)
        x,y = fix(*path[i])
        px,py = (0,0) if i == 0 else fix(*path[i-1])
        nx,ny = (0,0) if i == maxi else fix(*path[i+1])
        pd = x-px,y-py
        nd = nx-x,ny-y
        inp = "UP" if i == 0 else opposite[ports[pd]]
        outp = opposite[inp] if i == maxi else ports[nd]
        addr = idx_offset + i
        cell = code_memory_cell.format(idx=addr,val=addr^contents[i],inp=inp,outp=outp)
        if dtype == "left":
            blocks[(sx+x,sy+y)] = cell
        elif dtype == "right":
            blocks[(sx+x,sy+y)] = cell
        else:
            assert(dtype == "straight")
            blocks[(sx,sy+i)] = cell

def write_blocks(blocks, filepath, addr_tmpl):
    with open(filepath, "w+") as f:
        for i,(x,y) in enumerate(blocks):
            f.write(f"tpu X{x} Y{y}\n")
            if i == 0:
                f.write("\t## ${" + addr_tmpl + "}\n")
            for l in blocks[(x,y)].strip("\n").split("\n"):
                f.write(f"{l}\n")
            f.write(f"end\n")
            f.write("\n")

if __name__ == "__main__":
    blocks = {}
    blocks[(0, 0)] = memory_block_start.replace("{addr}", sys.argv[5])
    blocks[(-1, 0)] = memory_block_start_left
    blocks[(1, 0)] = memory_block_start_right
    gen_memory(blocks, (0, 1), int(sys.argv[2]), int(sys.argv[3]),
        open(sys.argv[4], "rb").read().ljust(256, b"\x00"), sys.argv[6])
    write_blocks(blocks, sys.argv[1], sys.argv[5])
