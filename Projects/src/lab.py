from cv2 import imread, imwrite
import cv2
from time import clock
from numpy import ndarray
import matplotlib.pyplot as plt
from jpeg import JPEG
from jpeg import snr
from jpeg import comp_rate


def process(image: ndarray, quality: int = 50):

    print("Encoding image with JPEG")
    t = clock()

    image = JPEG(image, quality)
    image.encode()

    elapsed_time = clock() - t
    print("Encoding time: {}".format(elapsed_time))

    print("Decoding stream")
    t = clock()

    image.decode()

    elapsed_time = clock() - t
    print("Decoding time: {}".format(elapsed_time))

    return image


def write_to_file(stream: str, filename: str):
    with open(filename, "w") as file:
        file.write(stream)

