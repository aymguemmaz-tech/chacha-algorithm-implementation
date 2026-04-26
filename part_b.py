def rotate_left_32(value: int, n: int) -> int:
    return ((value << n) | (value >> (32 - n))) & 0xffffffff
 
def quarter_round(a: int, b: int, c: int, d: int) -> tuple[int, int, int, int]:
    a = (a + b) & 0xffffffff;  d = d ^ a;  d = rotate_left_32(d, 16)
    c = (c + d) & 0xffffffff;  b = b ^ c;  b = rotate_left_32(b, 12)
    a = (a + b) & 0xffffffff;  d = d ^ a;  d = rotate_left_32(d,  8)
    c = (c + d) & 0xffffffff;  b = b ^ c;  b = rotate_left_32(b,  7)
    return (a, b, c, d)