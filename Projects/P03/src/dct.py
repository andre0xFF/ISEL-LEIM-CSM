import numpy as np
from cv2 import dct
from cv2 import idct
from cv2 import imread
from cv2 import imwrite

def encode(block: np.array)  -> np.array:
    return dct(block)

def decode(block: np.array)  -> np.array:
    return idct(block)
