# check if the point is on the P-256(secp256r1) curve

x = 0x59fc5c8006ac52a39479c1aabacbbd1d56fcb98feeaa182334c45b3a7609029e
y = 0x3f501e5e20830c70b5a2ff3a0690a22e9782bb2c1a76fe798952daec599edd4d
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

print((x*x*x-3*x+b)%p)
print(y*y%p)
print((x*x*x-3*x+b)%p == y*y%p)