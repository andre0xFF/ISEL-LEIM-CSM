import numpy as np


def dc_keys():
    # k3 is the luminance DC coefficients
    k3 = dict()
    k3[0] = "00"
    k3[1] = "010"
    k3[2] = "011"
    k3[3] = "100"
    k3[4] = "101"
    k3[5] = "110"
    k3[6] = "1110"
    k3[7] = "11110"
    k3[8] = "111110"
    k3[9] = "1111110"
    k3[10] = "11111110"
    k3[11] = "111111110"

    return k3


def binary_dc(bits: str) -> np.int:
    k3 = dc_keys()

    for key in range(len(k3)):
        if bits == k3[key]:
            return key

    return None


def encode(previous_block: np.array, block: np.array) -> np.int:
    if previous_block is None:
        return block[0][0]

    return block[0][0] - previous_block[0][0]


def decode(bit_stream: str) -> (np.int, str):
    size_bits = bit_stream[0]
    size = 0
    index = 0

    # Find the DC size value
    for i in range(len(bit_stream)):
        size = binary_dc(size_bits)

        if size is not None:
            index = i
            break

        size_bits = "{}{}".format(size_bits, bit_stream[i])

    if index == 0:
        return None

    # Get and convert the signal
    signal_bits = bit_stream[index]
    signal = 1 if signal_bits == "0" else -1

    # Get and convert the DC value
    dc_bits = bit_stream[index + 1: index + size]
    dc = np.int(dc_bits, 2)

    # DC value may be negative or positive,
    # The rest of the bit_stream still needs to be decoded
    return (
        dc * signal,
        bit_stream[index + size:]
    )


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
    dc = np.zeros(3)
    dc[0] = encode(None, block_0)
    dc[1] = encode(block_0, block_1)
    dc[2] = encode(block_1, block_2)

    print("[INFO] DC encoding {}".format(dc))

    print("[INFO] Decoding '{}'".format("11110 0 1010000 1100 1 1010 00"))
    dc, bit_stream = decode("111100101000011001101000")

    print("[INFO] Decoded DC: {}".format(dc))
    print("[INFO] Rest of bit stream: {}".format(bit_stream))


if __name__ == "__main__":
    _test()

