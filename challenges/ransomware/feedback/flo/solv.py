# from pwn import *


with open("flag.txt", "rb") as f:
    data = f.read()

#with open("/home/mrmaxmeier/_GitRepos/cscg22/challenges-finals/ransomware/build/flag.txt", "rb") as f:
#    data = f.read()


# from pwn import b64d
# data = b64d("OPqeiv4VkQbRZ/329F/Bsp9q4pESkr8mZ2U5USqjXyHigJ8jLiwHr8Q1LlmRkkoiR9VU2Dw+HORoJUkJAG8SIDSPMu/KaO05fK3XCF9J3oyYlJc=")

needle = list(b"ALLE")

RSP = 0x7fff37ba0630
STACK = RSP-0x500, RSP+0x500
M = (1<<64)-1

for key in range(STACK[0], STACK[1], 8):
    stack = key
    if key % 1024 == 0:
        print(f"{key = :#x}")
    block = list(data[:8])
    for i in range(8):
        seed = (key + 28411) & M
        for _ in range(8121):
            key = ((seed + key) & M) % 134456
        block[i] ^= key & 0xff
    if block[:len(needle)] == needle:
        print("found", key, block, bytes(block))
        break

def decrypt(data, key, rec_offset):
    if len(data) > 8:
        data[8:] = decrypt(data[8:], key+rec_offset, rec_offset)
    for i in range(len(data)):
        seed = (key + 28411) & M
        for _ in range(8121):
            key = ((seed + key) & M) % 134456
        data[i] ^= key & 0xff
    return data

print(f"{stack = :#x}")
for i in range(0, 0x200, 8):
    guess = bytes(decrypt(list(data), stack, rec_offset=-i))
    if all([x <= 0x7f for x in guess]):
        print(guess.decode().strip())
