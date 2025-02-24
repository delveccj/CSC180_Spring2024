import struct;

print(struct.pack("<Q", 0x504f4e4d4c4b4a49)[::-1].decode("latin1"))
