from src.part_c import chacha20_block
 
 
def chacha20_encrypt(plaintext: bytes, key: bytes, nonce: bytes, counter: int) -> bytes:
    result = bytearray()
 
    for i in range(0, len(plaintext), 64):
        block_index = counter + (i // 64)
 
        keystream = chacha20_block(key, block_index, nonce)
 
        plaintext_chunk = plaintext[i : i + 64]
 
        encrypted_chunk = bytes(p ^ k for p, k in zip(plaintext_chunk, keystream))
 
        result.extend(encrypted_chunk)
 
    return bytes(result)
 
 
def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes, counter: int) -> bytes:
    return chacha20_encrypt(ciphertext, key, nonce, counter)