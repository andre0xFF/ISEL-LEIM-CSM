import numpy as np
import os


def compression_rate(filepath1: str, filepath2: str):
    original_size = os.path.getsize(filepath1)
    compressed_size = os.path.getsize(filepath2)

    return (original_size / compressed_size, original_size, compressed_size)


def power(image: np.ndarray):
    return np.sum(np.power(image, 2)) / (len(image[0]) * len(image[1]))


def snr(image: np.ndarray, compressed: np.ndarray):
    return np.sum(np.power(compressed, 2)) / np.sum(np.power(compressed - image, 2))


def snr_db(image: np.ndarray, compressed: np.ndarray):
    return 10 * np.log10(snr(image, compressed))


def psnr(image: np.ndarray, compressed: np.ndarray):
    return 10 * np.log10(np.power(np.max(image), 2) / mean_squared_error(image, compressed))


def mean_squared_error(image: np.ndarray, compressed: np.ndarray):
    # 3 represents the RGB channel
    length = 3 * len(image[0]) * len(image[1])
    return (1 / length) * np.sum(np.power(compressed - image, 2))
