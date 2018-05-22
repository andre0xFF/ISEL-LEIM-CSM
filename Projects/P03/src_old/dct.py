from cv2 import dct
from cv2 import idct

import numpy as np


def encode(block: np.array) -> np.array:
    return dct(block)


def decode(block: np.array) -> np.array:
    return idct(block)
