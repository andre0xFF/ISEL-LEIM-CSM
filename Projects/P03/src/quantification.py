import numpy as np


def quality_factor(q: float) -> float:
    if q <= 50:
        factor = 50.0 / q
    else:
        factor = 2.0 - (q * 2.0)/100.0
    return factor


def get_luminance_matrix() -> np.array:
    # tab_jpeg
    # table K1 - Luminance quantize Matrix
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
