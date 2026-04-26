import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.part_c import double_round, chacha20_block

# double_round sanity: a non-trivial state must be altered
_nonzero = list(range(16))
_nonzero[0] = 0x61707865
double_round(_nonzero)
assert any(w != i for i, w in enumerate(_nonzero)), "double_round must alter the state"

# Full block test -- RFC 8439 ss.2.3.2
_key_block = bytes(range(32))
_nonce_block = bytes.fromhex("000000090000004a00000000")  # fmt:skip
_block = chacha20_block(_key_block, 1, _nonce_block)

assert len(_block) == 64, "Block must be exactly 64 bytes"

# Expected output words (little-endian) from RFC 8439 ss.2.3.2
# fmt:off
_expected_words = [
    0xe4e7f110, 0x15593bd1, 0x1fdd0f50, 0xc47120a3,
    0xc7f4d1c7, 0x0368c033, 0x9aaa2204, 0x4e6cd4c3,
    0x466482d2, 0x09aa9f07, 0x05d7c214, 0xa2028bd9,
    0xd19c12b5, 0xb94e16de, 0xe883d0cb, 0x4e3c50a2,
]
# fmt:on
_got_words = [int.from_bytes(_block[i * 4 : (i + 1) * 4], "little") for i in range(16)]
assert _got_words == _expected_words, "Block mismatch at word(s): " + str(
    [i for i in range(16) if _got_words[i] != _expected_words[i]]
)

print("Part C -- All tests passed.")