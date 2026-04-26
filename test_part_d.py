import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.part_c import chacha20_block
from src.part_d import chacha20_encrypt, chacha20_decrypt

# -- Tests (RFC 8439 ss.2.4.2) -------------------------------------------------

_key_s = b"\x00" * 32
_n_s = b"\x00" * 12
_ct_z = chacha20_encrypt(b"\x00" * 64, _key_s, _n_s, 0)
assert _ct_z == chacha20_block(_key_s, 0, _n_s), (
    "Encrypting zeros must equal the raw keystream block"
)

_msg = b"Hello, ChaCha20 from RFC 8439!"
_k_rt = bytes(range(32))
_n_rt = bytes(range(12))
assert (
    chacha20_decrypt(chacha20_encrypt(_msg, _k_rt, _n_rt, 0), _k_rt, _n_rt, 0) == _msg
), "Round-trip failed"

_key_tv = bytes(range(32))
_nonce_tv = bytes.fromhex("000000000000004a00000000")
_pt_tv = (
    b"Ladies and Gentlemen of the class of '99: If I could offer you "
    b"only one tip for the future, sunscreen would be it."
)
_ct_tv = chacha20_encrypt(_pt_tv, _key_tv, _nonce_tv, 1)

_expected_ct_hex = (
    "6e2e359a2568f98041ba0728dd0d6981"
    "e97e7aec1d4360c20a27afccfd9fae0b"
    "f91b65c5524733ab8f593dabcd62b357"
    "1639d624e65152ab8f530c359f0861d8"
    "07ca0dbf500d6a6156a38e088a22b65e"
    "52bc514d16ccf806818ce91ab7793736"
    "5af90bbf74a35be6b40b8eedf2785e42"
    "874d"
)

assert _ct_tv.hex() == _expected_ct_hex, (
    f"RFC 8439 ss.2.4.2 ciphertext mismatch\nGot:      {_ct_tv.hex()}\nExpected: {_expected_ct_hex}"
)

assert chacha20_decrypt(_ct_tv, _key_tv, _nonce_tv, 1) == _pt_tv, (
    "Decryption of RFC 8439 test vector failed"
)

print("Part D -- All tests passed.")
print("Full ChaCha20 implementation verified against RFC 8439!")