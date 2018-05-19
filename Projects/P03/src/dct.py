import numpy as np
from cv2 import dct
from cv2 import idct


def encode(block: np.array) -> np.array:
    return dct(block)


def decode(block: np.array) -> np.array:
    return idct(block)
