import runpy

print("Running tests...")
runpy.run_path("tests/test_part_a.py")
runpy.run_path("tests/test_part_b.py")
runpy.run_path("tests/test_part_c.py")
runpy.run_path("tests/test_part_d.py")

print()

from src.part_c import chacha20_block
from src.part_d import chacha20_encrypt, chacha20_decrypt

key     = bytes(range(32))
nonce   = bytes(range(12))
counter = 1

# --- Keystream ---
keystream = chacha20_block(key, counter, nonce)
print(f"Keystream:  {keystream.hex()}\n")

# --- Encryption / Decryption ---
message = b"cryptography assignment IT4SSM"
print(f"Plaintext:  {message.decode()}")

ct = chacha20_encrypt(message, key, nonce, counter)
print(f"Ciphertext: {ct.hex()}")

pt = chacha20_decrypt(ct, key, nonce, counter)
print(f"Decrypted:  {pt.decode()}")

assert pt == message
print("\nRound-trip successful!")