def chacha20_init_state(key: bytes, counter: int, nonce: bytes) -> list[int]:
    assert len(key) == 32, f"Key must be 32 bytes, got {len(key)}"
    assert len(nonce) == 12, f"Nonce must be 12 bytes, got {len(nonce)}"

    MAGIC_CONSTANTS = [
        0x61707865,
        0x3320646E,
        0x79622D32,
        0x6B206574,
    ]

    state = [0] * 16
    state[0:4] = MAGIC_CONSTANTS

    for i in range(8):
        state[4 + i] = int.from_bytes(key[i * 4:(i + 1) * 4], "little")

    state[12] = counter & 0xFFFFFFFF

    for i in range(3):
        state[13 + i] = int.from_bytes(nonce[i * 4:(i + 1) * 4], "little")

    return state


def serialize_state(state: list[int]) -> bytes:
    assert len(state) == 16, f"State must have 16 words, got {len(state)}"
    return b"".join((word & 0xFFFFFFFF).to_bytes(4, "little") for word in state)

_test_key = bytes(range(32))  # 00 01 02 ... 1f
_test_nonce = bytes([0] * 12)
_test_state = chacha20_init_state(_test_key, 0, _test_nonce)

assert len(_test_state) == 16, "State must have exactly 16 words"
assert _test_state[0] == 0x61707865, "Constant word 0 wrong"
assert _test_state[1] == 0x3320646E, "Constant word 1 wrong"
assert _test_state[2] == 0x79622D32, "Constant word 2 wrong"
assert _test_state[3] == 0x6B206574, "Constant word 3 wrong"
# Key bytes 00 01 02 03 load as little-endian word 0x03020100
assert _test_state[4] == 0x03020100, "Key word 0 wrong (check endianness)"
assert _test_state[12] == 0, "Counter must be 0"

# serialize_state round-trip
_serialized = serialize_state(_test_state)
assert len(_serialized) == 64, "Serialized block must be 64 bytes"
assert int.from_bytes(_serialized[0:4], "little") == 0x61707865, (
    "First serialized word wrong"
)
assert int.from_bytes(_serialized[16:20], "little") == 0x03020100, (
    "Key word 0 wrong after serialize"
)

# RFC 8439 ss.2.3.2 -- nonce and counter placement
_key2 = bytes(range(32))
_nonce2 = bytes.fromhex("000000090000004a00000000")
_s2 = chacha20_init_state(_key2, 1, _nonce2)
assert _s2[12] == 1, "Counter word must equal the counter argument"
assert _s2[13] == 0x09000000, "Nonce word 0 wrong (little-endian!)"
assert _s2[14] == 0x4A000000, "Nonce word 1 wrong (little-endian!)"
assert _s2[15] == 0x00000000, "Nonce word 2 wrong"

print("Part A -- All tests passed.")