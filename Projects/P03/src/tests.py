import numpy as np

from jpeg import Block
from jpeg import quantification


def test_quantification():
    block = Block(np.array([
        [1337, 56, -27, 18, 78, -60, 27, -27],
        [-38, -27, 13, 44, 32, -1, -24, -10],
        [-20, -17, 10, 33, 21, -6, -16, -9],
        [-10, -8, 9, 17, 9, -10, -13, 1],
        [-6, 1, 6, 4, -3, -7, -5, 5],
        [2, 3, 0, -3, -7, -4, 0, 3],
        [4, 4, -1, -2, -9, 0, 2, 4],
        [3, 1, 0, -4, -2, -1, 3, 1]
    ]))

    print("[INFO] Encoding")
    encoded = quantification.encode(block, 50)

    print("Encoded block: \n{}".format(encoded))

    print("[INFO] Decoding")
    decoded = quantification.decode(encoded, 50)

    print("Decoded block: \n{}".format(decoded))


def test_dc_ac():
    block_0 = Block(np.array([
        [80, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    block_1 = Block(np.array([
        [80, 2, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    block_2 = Block(np.array([
        [78, 1, 0, -1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    print("[INFO] Encoding")
    block_0.dpcm_encode(None)
    block_1.dpcm_encode(block_0)
    block_2.dpcm_encode(block_1)

    block_0.rlc_encode()
    block_1.rlc_encode()
    block_2.rlc_encode()

    print("Block 0 Stream: {}".format(block_0.stream))
    print("Block 1 Stream: {}".format(block_1.stream))
    print("Block 2 Stream: {}".format(block_2.stream))

    print("[INFO] Decoding")
    dc_0, ac_0, elements = Block.decode(block_0.stream)
    dc_1, ac_1, elements = Block.decode(block_1.stream)
    dc_2, ac_2, elements = Block.decode(block_2.stream)

    print("Stream 0 DC: {}".format(dc_0))
    print("Stream 1 DC: {}".format(dc_1))
    print("Stream 2 DC: {}".format(dc_2))


if __name__ == "__main__":
    print("> Test quantification")
    test_quantification()

    print("\n> Test DC")
    test_dc_ac()
