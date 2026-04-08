# chacha-algorithm-implementation
In this repository i will implement chacha algorithm as a part of my course cryptographie.
1. Algorithm Overview
ChaCha20 is a stream cipher designed by Daniel J. Bernstein. Unlike DES/AES, it does not operate on fixed-size blocks of plaintext; instead, it generates a pseudorandom keystream of any length, which is then XOR-ed with the plaintext.

The cipher state is a 4x4 matrix of 32-bit words (512 bits total):


 Word index:  [ 0]  [ 1]  [ 2]  [ 3]
              [ 4]  [ 5]  [ 6]  [ 7]
              [ 8]  [ 9]  [10]  [11]
              [12]  [13]  [14]  [15]

 Semantics:   [C0]  [C1]  [C2]  [C3]   <- 128-bit constant ("expand 32-byte k")
              [K0]  [K1]  [K2]  [K3]   <- key words  0-3  (bits   0-127)
              [K4]  [K5]  [K6]  [K7]   <- key words  4-7  (bits 128-255)
              [CTR] [N0]  [N1]  [N2]   <- 32-bit counter + 96-bit nonce


The keystream generation for one 64-byte block:


  key (32 bytes) --+
nonce (12 bytes) --+--> chacha20_init_state()  -->  initial state (16 x u32)
   counter (u32) --+                                      |
                                                          |  working_state = copy(initial_state)
                                                          |
                                                          v
                                                 +------------------+
                                                 |  double_round()  | x 10
                                                 | (column + diag)  |
                                                 +--------+---------+
                                                          |
                                         working_state[i] += initial_state[i]  (mod 2^32)
                                                          |
                                                          v
                                              serialize to 64 bytes (little-endian)
                                                          |
                                                          v
                                         keystream[0:64]  XOR  plaintext[0:64]
The Quarter Round function: core primitive
The quarter round QR(a, b, c, d) operates on four 32-bit words and mixes them using four ARX steps. All additions are modulo 2^32. This is also called carryless addition on a 32-bit word:

a = a + b (mod 32);  d = d XOR a;  d = d ROTL 16
c = c + d (mod 32);  b = b XOR c;  b = b ROTL 12
a = a + b (mod 32);  d = d XOR a;  d = d ROTL 8
c = c + d (mod 32);  b = b XOR c;  b = b ROTL 7
Column and Diagonal Rounds
Each double round applies the quarter round to columns first, then to diagonals of the 4x4 state:

Round type	Applications
Column round	QR(s[0],s[4],s[8],s[12]) / QR(s[1],s[5],s[9],s[13]) / QR(s[2],s[6],s[10],s[14]) / QR(s[3],s[7],s[11],s[15])
Diagonal round	QR(s[0],s[5],s[10],s[15]) / QR(s[1],s[6],s[11],s[12]) / QR(s[2],s[7],s[8],s[13]) / QR(s[3],s[4],s[9],s[14])
ChaCha20 applies 10 double rounds (= 20 total quarter-round passes).

Constants
ChaCha20 has no secret tables. The only constants are the four 32-bit words that fill row 0 of the state matrix (the "nothing-up-my-sleeve" magic string). The come from the ASCII string expand 32-byte k decoded as four little-endian 32-bit words.

2. Implementation
Part A - State Initialization: chacha20_init_state and serialize_state
Before any mixing can take place, the 16-word state matrix must be constructed from the inputs:

  state[0..3]   = MAGIC_CONSTANTS         (4 words, fixed, see "Constants" in overview section)
  state[4..11]  = key                     (8 words, little-endian u32)
  state[12]     = counter                 (1 word,  32-bit integer)
  state[13..15] = nonce                   (3 words, little-endian u32)
chacha20_init_state packs the raw bytes inputs into a flat Python list of 16 integers.

serialize_state does the inverse after mixing: it converts each word back to 4 bytes (little-endian) and concatenates all 16 words into a 64-byte keystream block.
