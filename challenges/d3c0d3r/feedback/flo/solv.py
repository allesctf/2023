import itertools
import base64
import string

m = {}
# alphabet = bytes(range(256))
alphabet = string.printable.encode()
print("churning...")
for s in itertools.product(alphabet, repeat=3):
    s = bytes(s)
    res = base64.b64encode(s).decode()
    if res.isupper():
        m[s.lower()] = res

for s in itertools.product(alphabet, repeat=3):
    s = bytes(s)
    if s in m:
        print(s, m[s])

payload = m[b"cat"]
# payload += m[b'  \t']
payload += m[b' /?']

target = b"LAG_327a6c4304ad5938eaf0efb6cc3e53dc"
for _ in range(len(target)):
    payload += m[b'``?']

print(payload)