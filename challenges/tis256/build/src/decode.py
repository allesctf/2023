
mem = bytes()
for i in range(4):
    mem += open(f"build/memory{i+1}.bin", "rb").read()

offset = 0x80
lsfr = mem[0xff]
while True:
    bits = [int(v) for v in bin(lsfr)[2:].zfill(8)]
    bits = bits[7:] + bits[0:7]
    bits[0] ^= bits[7-2]
    bits[0] ^= bits[7-5]
    lsfr = sum([2**(7-i) if v else 0 for i,v in enumerate(bits)])
    b = mem[offset + (lsfr & (0xff >> 3))]
    fb = b ^ lsfr
    print(chr(fb), end="")
    if fb == 0:
        break
print()
