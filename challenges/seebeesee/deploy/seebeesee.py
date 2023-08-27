#!/usr/bin/env pypy3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys
import base64
import re

KEY = b'e87feb7704477bbc'

def repl():
    print("Welcome to SeeBeeSee")

    while True:
        print(" (1) run script")
        print(" (2) get source code of this program")
        print(" (3) get sample script")
        print(" (4) exit")
        choice = input(">")
        if choice == "1":
            print("Please provide your script! (format: base64(aes(script)) )")
            script = input(">")
            runscript(base64.b64decode(script))
        elif choice == "2":
            with open(__file__) as f:
                print(re.sub(r"KEY = b'[a-zA-Z0-9]+'","KEY\x20= b'redactedredacted'",f.read()))
        elif choice == "3":
            print(getsample())
        elif choice == "4":
            print("bye!")
            exit()


def runscript(data):
    try:
        global result
        result = b""
        decrypted = decrypt(data, KEY)
        print("---DEC---")
        print(decrypted)
        print("---EOF---")
        dec = decrypted.decode("utf-8", "replace")
        print(dec)
        print("---")
        exec(dec, globals())
        print("r:", result)
        return True
    except Exception as e:
        print("decryption error?")
        print(e)
        return False

def getsample():
    code = b"""
exit()
#AAAAAAAAA
#AAAAAAAAAAAAAAAA
a = r"0000000000000000000000000000"
if a!=r"0000000000000000000000000000":
    testok = True
if testok:
    result = b"See? " + KEY[:-4]
#reset 4 security
result = b"nope"
"""

    cipher = AES.new(KEY, AES.MODE_CBC,iv=b'\x00'*16)
    ciphertext = cipher.encrypt(pad(code, AES.block_size))
    return base64.b64encode(ciphertext)

def decrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC,iv=b'\x00'*16)
    dec = cipher.decrypt(data)
    try:
        return unpad(dec ,AES.block_size)
    except ValueError:
        if len(dec) % AES.block_size == 0:
            return dec
        else:
            raise ValueError


repl()
