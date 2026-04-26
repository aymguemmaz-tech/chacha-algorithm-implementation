from src.part_a import chacha20_init_state, serialize_state
from src.part_b import quarter_round
 
 
def double_round(state: list[int]) -> list[int]:
 
    # --- Column round ---
    state[0], state[4], state[8], state[12] = quarter_round(state[0], state[4], state[8], state[12])
    state[1], state[5], state[9], state[13] = quarter_round(state[1], state[5], state[9], state[13])
    state[2], state[6], state[10], state[14] = quarter_round(state[2], state[6], state[10], state[14])
    state[3], state[7], state[11], state[15] = quarter_round(state[3], state[7], state[11], state[15])
 
    # --- Diagonal round ---
    state[0], state[5], state[10], state[15] = quarter_round(state[0], state[5], state[10], state[15])
    state[1], state[6], state[11], state[12] = quarter_round(state[1], state[6], state[11], state[12])
    state[2], state[7], state[8], state[13] = quarter_round(state[2], state[7], state[8], state[13])
    state[3], state[4], state[9], state[14] = quarter_round(state[3], state[4], state[9], state[14])
 
    return state
 
 
def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
 
    # 1. initial state
    state = chacha20_init_state(key, counter, nonce)
 
    # 2. working copy
    working = state.copy()
 
    # 3. 20 rounds = 10 double rounds
    for _ in range(10):
        double_round(working)
 
    # 4. add original state
    for i in range(16):
        working[i] = (working[i] + state[i]) & 0xffffffff # 0xffffffff = mod 2^32 -1 --> overflow
 
    # 5. serialize
    return serialize_state(working)