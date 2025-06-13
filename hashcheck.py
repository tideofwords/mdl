import hashlib, binascii

keys = [
    ("digestID", 1485031251),
    ("random", bytes.fromhex("51c630e012290244f0484af6878b5a58")),
    ("elementIdentifier", "hair_colour"),
    ("elementValue", "red"),
]
# encode manually
def encode_tstr(s):
    b = s.encode('utf-8')
    l = len(b)
    if l<24:
        return bytes([0x60+l]) + b
    raise ValueError
def encode_uint(n):
    if n<=0xffffffff:
        return bytes([0x1a]) + n.to_bytes(4,'big')
    # else bigger
def encode_bstr(b):
    l = len(b)
    if l<24:
        return bytes([0x40+l]) + b
    elif l<256:
        return bytes([0x58,l]) + b
    else:
        raise ValueError
def encode_value(v):
    if isinstance(v,int):
        return encode_uint(v)
    elif isinstance(v,bytes):
        return encode_bstr(v)
    elif isinstance(v,str):
        return encode_tstr(v)
    else:
        raise TypeError
# building map preserving order
encoded_items = b''
for k,v in keys:
    encoded_items += encode_tstr(k)
    encoded_items += encode_value(v)
map_bytes = bytes([0xa0+len(keys)]) + encoded_items
outer = bytes([0xd8,0x18]) + encode_bstr(map_bytes)
print(outer)
digest = hashlib.sha256(outer).hexdigest()
print(digest)