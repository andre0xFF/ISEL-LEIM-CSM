import numpy as np


def quality_factor(q: float) -> float:
    if q >= 100:
        return 1

    if q <= 50:
        return 50 / q

    return 2 - (q * 2) / 100


def get_luminance_matrix() -> np.array:
    # k1 is the luminance matrix
    k1 = np.zeros((8, 8))
    k1[0] = [16, 11, 10, 16, 24, 40, 51, 61]
    k1[1] = [12, 12, 14, 19, 26, 58, 60, 55]
    k1[2] = [14, 13, 16, 24, 40, 57, 69, 56]
    k1[3] = [14, 17, 22, 29, 51, 87, 80, 62]
    k1[4] = [18, 22, 37, 56, 68, 109, 103, 77]
    k1[5] = [24, 35, 55, 64, 81, 104, 113, 92]
    k1[6] = [49, 64, 78, 87, 103, 121, 120, 101]
    k1[7] = [72, 92, 95, 98, 112, 100, 103, 99]

    return k1


def encode(block: np.array, factor: float) -> np.array:
    k = get_luminance_matrix()
    return np.round(block / (k * quality_factor(factor)))


def decode(block: np.array, factor: float) -> np.array:
    k = get_luminance_matrix()
    return block * (k * quality_factor(factor))


def _test():
    block = np.array([
        [ 1337,  56, -27,  18,  78, -60,  27, -27],
        [  -38, -27,  13,  44,  32,  -1, -24, -10],
        [  -20, -17,  10,  33,  21,  -6, -16,  -9],
        [  -10,  -8,   9,  17,   9, -10, -13,   1],
        [   -6,   1,   6,   4,  -3,  -7,  -5,   5],
        [    2,   3,   0,  -3,  -7,  -4,   0,   3],
        [    4,   4,  -1,  -2,  -9,   0,   2,   4],
        [    3,   1,   0,  -4,  -2,  -1,   3,   1]
    ])

    print("[INFO] Encoding")
    encoded = encode(block, 50)

    print("{}".format(encoded))

    print("[INFO] Decoding")
    decoded = decode(encoded, 50)

    print("{}".format(decoded))


if __name__ == "__main__":
    _test()
