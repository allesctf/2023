import random

random.seed(133713371337)

asm = """
    not r0
    mov r0, r2
    ldb r0, r3 # lsfr
    jnz chk_loop

lsfr_advance:
    # bit 0
    mov r3, r0
    shr r3, 1
    shl r0, 7
    xor r0, r3

    # bit 3
    mov r3, r0
    shr r0, 2
    shl r0, 7
    xor r0, r3

    # bit 6
    mov r3, r0
    shr r0, 5
    shl r0, 7
    xor r0, r3

    # if != 0, jmp, else
    # fallthrough to same location
    jnz lsfr_advance_ret

chk_loop:
    jnz lsfr_advance
lsfr_advance_ret:

    xor r0, r0
    not r0
    shr r0, 3
    and r3, r0

    xor r1, r1
    inc r1
    shl r1, 7
    add r1, r0
    ldb r0, r1

    jnz check_val
check_val_ret:

    mov r1, r0
    jnz chk_loop

    not r0
    jnz end1

check_val:
    inp r0
    xor r3, r1
    xor r0, r1
    not r1
    and r1, r2
    mov r0, r1

    xor r0, r0
    not r0
    jnz check_val2
check_val2_ret:
    jnz check_val_ret

end1:
    jnz end2

check_val2:
    xor r0, r0
    inc r0
    shl r0, 2
    inc r0
    shl r0, 1
    xor r0, r1

    jnz check_val2_ret

end2:
    mov r2, r0
    not r0
    jnz print_fail
    not r0
    jnz print_ok

print_fail:
    xor r2, r2
    not r2
    shl r2, 3
    jnz print

print_ok:
    xor r2, r2
    not r2
    shl r2, 4

print:
    xor r1, r1
    inc r1
print_loop:
    ldb r2, r0
    jnz print_cont
    hlt
print_cont:
    out r0
    add r1, r2
    jnz print_loop

"""

flag = b"ALLES!{T3553L4T3!}\x0a"

data = {}

# ensure lsfr hits different indexes
seed_ok = False
lsfr_init = None
for lsfr_init in range(0x6f, 256):
    reg = lsfr_init
    data.clear()
    seed_ok = True
    vals = []
    for i,c in enumerate(flag):
        b = (reg >> 6) & 0x01
        b ^= (reg >> 3) & 0x01
        b ^= (reg >> 0) & 0x01
        reg = (b << 7) | (reg >> 1)
        vals.append(reg)
        addr = 0x80 + (reg & 0x1f)
        vals.append(addr)
        if addr in data:
            seed_ok = False
        data[addr] = c ^ reg
    if seed_ok:
        print("vals", [hex(v) for v in vals])
        break
assert(seed_ok)

for i,b in enumerate(b"ok\n\x00"):
    data[0xf0+i] = b

for i,b in enumerate(b"fail\n\x00"):
    data[0xf8+i] = b

data[0xff] = lsfr_init

bytecode = []
labels = {}
for l in asm.split("\n"):
    l = l.replace(",", " ").strip().lower()
    if ":" in l:
        name = l.split(":")[0]
        labels[name] = len(bytecode)
        continue
    elif l == "" or l.strip().startswith("#"):
        continue
    cmd, ops = l.split()[0], l.split()[1:3]
    if cmd == "jnz":
        name, = ops
        bytecode.append(name)
    elif cmd == "shl":
        r1,sh = int(ops[0][1:]), int(ops[1])
        assert(r1 >= 0 and r1 < 4)
        assert(sh >= 0 and sh < 8)
        bytecode.append(0b01000000 | (r1 << 3) | sh)
    elif cmd == "shr":
        r1,sh = int(ops[0][1:]), int(ops[1])
        assert(r1 >= 0 and r1 < 4)
        assert(sh >= 0 and sh < 8)
        bytecode.append(0b01100000 | (r1 << 3) | sh)
    elif cmd == "mov":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b00100000 | (r1 << 2) | r2)
    elif cmd == "swp":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b00110000 | (r1 << 2) | r2)
    elif cmd == "add":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b10000000 | (r1 << 2) | r2)
    elif cmd == "sub":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b10010000 | (r1 << 2) | r2)
    elif cmd == "xor":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b10100000 | (r1 << 2) | r2)
    elif cmd == "and":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b10110000 | (r1 << 2) | r2)
    elif cmd == "ldb":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b11000000 | (r1 << 2) | r2)
    elif cmd == "stb":
        r1,r2 = [int(o[1:]) for o in ops]
        assert(r1 >= 0 and r1 < 4)
        assert(r2 >= 0 and r2 < 4)
        bytecode.append(0b11010000 | (r1 << 2) | r2)
    elif cmd == "inp":
        reg, = [int(o[1:]) for o in ops]
        assert(reg >= 0 and reg < 4)
        bytecode.append(0b11100000 | reg)
    elif cmd == "out":
        reg, = [int(o[1:]) for o in ops]
        assert(reg >= 0 and reg < 4)
        bytecode.append(0b11100100 | reg)
    elif cmd == "not":
        reg, = [int(o[1:]) for o in ops]
        assert(reg >= 0 and reg < 4)
        bytecode.append(0b11101000 | reg)
    elif cmd == "inc":
        reg, = [int(o[1:]) for o in ops]
        assert(reg >= 0 and reg < 4)
        bytecode.append(0b11110000 | reg)
    #elif cmd == "dec":
    #    reg, = [int(o[1:]) for o in ops]
    #    assert(reg >= 0 and reg < 4)
    #    bytecode.append(0b11110100 | reg)
    elif cmd == "hlt":
        bytecode.append(0b11111111)
    else:
        print(cmd)
        assert(False)

for i,b in enumerate(bytecode):
    if type(b) == str:
        off = labels[b] - (i + 1) + 16
        print(b, off)
        assert(off >= 0 and off < 32)
        bytecode[i] = 0b00000000 | off

print(len(bytecode), bytecode)
bytecode += random.randbytes(0x100 - len(bytecode))
for p,v in data.items():
    bytecode[p] = v

for i in range(4):
    with open(f"build/memory{i+1}.bin", "wb+") as f:
        f.write(bytes(bytecode[i*64:i*64+64]))

