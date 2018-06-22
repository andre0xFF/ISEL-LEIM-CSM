import os
import numpy as np


def compression_rate(original_file, encoded_file):
    original_size = os.path.getsize(original_file)
    encoded_size = os.path.getsize(encoded_file)
    rate = round(100 * (1 - encoded_size / original_size), 2)
    ratio = round(1. * original_size / encoded_size, 2)

    return ratio, rate


def snr(original_image: np.ndarray, encoded_image: np.ndarray) -> float:
    original_image = original_image.flatten()
    encoded_image = encoded_image.flatten()

    error = original_image - encoded_image

    original_power = np.sum(original_image ** 2.0) / len(original_image)
    error_power = np.sum(error ** 2.0) / len(error)
    snr = 10 * np.log10(original_power / error_power)

    return round(snr, 2)


def psnr(original_image: np.ndarray, encoded_image: np.ndarray):

    max_value = np.power(np.max(original_image), 2)
    mean_squared_error = (1 / (3 * encoded_image.shape[0] * encoded_image.shape[1])) * \
                         np.sum(np.power((original_image - encoded_image), 2))
    psnr = 10 * np.log10(max_value / mean_squared_error)
    return round(psnr, 2)


def energy(signal):
    return round(sum(signal**2.0)/len(signal),2)


def entropy(signal):

    lensig = signal.size
    symset = list(set(signal))
    propab = [np.size(signal[signal == i]) / (1.0 * lensig) for i in symset]
    ent = np.sum([p * np.log2(1.0 / p) for p in propab])
    return round(ent,2)
