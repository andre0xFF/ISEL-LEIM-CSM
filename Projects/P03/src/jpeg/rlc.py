from numpy import argsort
from numpy import argwhere
from numpy import array, ndarray, zeros
from numpy import int
from numpy import sum

from .ac import AC


def encode(block) -> ndarray:
    zigzag = array([
        [0, 1, 5, 6, 14, 15, 27, 28],
        [2, 4, 7, 13, 16, 26, 29, 42],
        [3, 8, 12, 17, 25, 30, 41, 43],
        [9, 11, 18, 24, 31, 40, 44, 53],
        [10, 19, 23, 32, 39, 45, 52, 54],
        [20, 22, 33, 38, 46, 51, 55, 60],
        [21, 34, 37, 47, 50, 56, 59, 61],
        [35, 36, 48, 49, 57, 58, 62, 63],
    ])

    original_index = zigzag.reshape(64, order="F").astype("int")
    zigzag_index = argsort(original_index)
    elements = block.elements.copy().flatten(order="F")[zigzag_index]

    ac_elements = [AC] * (sum(elements != 0) - 1)

    zero_run_length = 0

    for i in range(1, len(elements)):
        if elements[i] == 0:
            zero_run_length += 1
        else:
            ac_elements[i - zero_run_length - 1] = AC(zero_run_length, elements[i])
            zero_run_length = 0

    return ac_elements


def decode(stream: str) -> (array, str):
    ac = []

    # Count the total amount of zeros in all ACs to build the elements
    # array
    total_zeros = 0

    # Index all possible AC values
    amplitudes_bits = array(list(AC.k5.values()))

    # In AC a key tuple pair is used as key of the dictionary so it is not
    # possible to use numpy array for linear comparison (like in DC). However,
    # finding a match between the stream and the dictionary's values as numpy
    # array is still useful to rule out the need to iterate all stream's bits.
    # If it is found then get the key tuple pair by iterating the k5
    # dictionary.
    j = 0
    i = 0

    while i < len(stream) + 1:
        i += 1
        match = argwhere(stream[j: i] == amplitudes_bits)

        if len(match) == 0:
            continue

        # Properties of AC
        amplitude = 0
        signal = 1 if int(stream[i]) == 0 else -1

        # A match was found. Now iterate k5 dictionary to find the key (tuple).
        # zrl stands for zero run length
        for zrl, size in AC.k5.keys():
            if stream[j: i] != AC.k5.get((zrl, size)):
                continue

            amplitude = int(stream[i + 1: i + 1 + size], 2) * signal
            ac.append(AC(zrl, amplitude))

            total_zeros += zrl
            i += 1 + size
            j = i
            break

    stream = stream[j:]

    # Build a linear array with AC elements, zeros and amplitudes
    amplitudes = zeros(total_zeros + len(ac))

    for i in range(len(ac)):
        amplitudes[i + ac[i].zero_run_length] = ac[i].amplitude

    return ac, amplitudes, stream
