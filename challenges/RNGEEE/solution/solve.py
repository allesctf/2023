from z3 import *
from main import ROTATIONS

PREFIX = "ALLES!{"
SUFFIX = "}"
BITS = 56
inputs = []
with open(f"msg{BITS}.txt", "rb") as f:
    data = f.read().decode()

for x in data.splitlines()[1:]:
    inputs.append(int(x.strip()))
s = Solver()
s.set("smtlib2_log", "log.smt2")
#s.set("timeout", 1)
state = [BitVec(f"s{i}", BITS) for i in range(len(inputs)+1)]

def rol(x, n, size): return (x << n) | ( LShR(x, size -n))
def ror(x, n, size): return ( LShR(x,n)) | (x << (size - n))

flag = [BitVec(f"flag{i}", 8) for i in range(len(inputs))]

for i in range(len(flag)):
    s.add(flag[i] >= 0x20)
    s.add(flag[i] <= 0x7f)

for i in range(len(PREFIX)):
    s.add(flag[i] == ord(PREFIX[i]))

for i in range(1,len(SUFFIX)+1):
    s.add(flag[-i] == ord(SUFFIX[::-1][i-1]))


for j in range(len(inputs)):
    v = state[j]
    for i in ROTATIONS:
        v |= rol(state[j], i, BITS)
        v ^= ror(v, i, BITS)
    s.add(state[j+1] == v)

for i in range(len(inputs)):
    s.add(Extract(7, 0, state[i]) ^ flag[i] == inputs[i])
assert s.check()

#
# import solve_model
# Boolector go brrr

m = s.model()
print("".join([chr(m[c].as_long()) for c in flag]))