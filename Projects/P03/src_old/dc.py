import numpy as np


def get_sizes():
    # k3 is the luminance DC coefficients
    k3 = {
        0: "00",
        1: "010",
        2: "011",
        3: "100",
        4: "101",
        5: "110",
        6: "1110",
        7: "11110",
        8: "111110",
        9: "1111110",
        10: "11111110",
        11: "111111110",
    }

    return k3


def bits_to_size(bits: str) -> np.int:
    k3 = get_sizes()

    for size in range(len(k3)):
        if bits == k3[size]:
            return size

    return None


def encode(previous_block: np.array, block: np.array) -> (np.int, np.int):
    if previous_block is None:
        amplitude = block[0][0]
    else:
        amplitude = block[0][0] - previous_block[0][0]

    size = len(bin(np.abs(amplitude))) - 2

    return size, amplitude


def _test():
    block_0 = np.array([
        [80, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    block_1 = np.array([
        [80, 2, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    block_2 = np.array([
        [78, 1, 0, -1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    print("[INFO] Encoding block_0, block_1, block_2")
    dc_size = np.zeros(3)
    dc_amplitude = np.zeros(3)
    dc_size[0], dc_amplitude[0] = encode(None, block_0)
    dc_size[1], dc_amplitude[1] = encode(block_0, block_1)
    dc_size[2], dc_amplitude[2] = encode(block_1, block_2)

    print("[INFO] Encoded DC size: {}".format(dc_size))
    print("[INFO] Encoded DC amplitude: {}".format(dc_amplitude))

    # "11110 0 1010000 1100 1 1010 00"


if __name__ == "__main__":
    _test()

