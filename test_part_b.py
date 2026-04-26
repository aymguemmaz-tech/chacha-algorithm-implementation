import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
 
from src.part_b import rotate_left_32, quarter_round
 
assert rotate_left_32(0x00000001, 1) == 0x00000002
assert rotate_left_32(0x80000000, 1) == 0x00000001, "MSB must wrap to bit 0"
assert rotate_left_32(0x12345678, 16) == 0x56781234
assert rotate_left_32(0xffffffff, 8) == 0xffffffff, "All-ones is rotation-invariant"
 
a, b, c, d = quarter_round(0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567)
assert a == 0xea2a92f4, f"a wrong: {hex(a)}"
assert b == 0xcb1cf8ce, f"b wrong: {hex(b)}"
assert c == 0x4581472e, f"c wrong: {hex(c)}"
assert d == 0x5881c4bb, f"d wrong: {hex(d)}"
 
print("Part B -- All tests passed.")