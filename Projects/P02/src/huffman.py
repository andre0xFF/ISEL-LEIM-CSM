import numpy as np


def encode(ascii_numbers: np.ndarray):
    uniques = np.unique(ascii_numbers)
    ascii_probs = calculate_probabilities(uniques, ascii_numbers)

    # Sort according to the probability in descending order
    uniques = uniques[np.argsort(ascii_probs)][::-1]
    ascii_probs = np.sort(ascii_probs)[::-1]

    # Array of arrays to store the binary number of each ascii number
    binaries = [np.ndarray([0], dtype=np.uint8), ] * len(uniques)

    # Moving array that will join the ascii's
    iterator = np.reshape(uniques, newshape=(len(uniques), 1))

    while len(iterator) > 2:
        pass

    # chars = ascii_to_char(ascii_numbers)
    # table = [np.ndarray([0], dtype=np.uint8), ] * len(repetitions)
    # indexes = np.arange(0, len(repetitions))
    #
    # while len(indexes) > 1:
    #     pass


def iterate(iterator: np.ndarray, probabilities: np.ndarray, binaries: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    aux_elements = [np.ndarray([0], dtype=np.uint8), ] * (len(iterator) - 1)
    aux_probabilities = np.zeros(len(probabilities) - 1)

    # New element of the last two elements
    # Each element can contain multiple elements
    element = np.ones(len(iterator[-1]) + len(iterator[-2]), dtype=np.int8)
    element[:len(iterator[-1])] = np.copy(iterator[-1])
    element[len(iterator[-1]):] = np.copy(iterator[-2])
    probability = probabilities[-1] + probabilities[-2]

    # Find the idx of the new element
    idx = np.argwhere((probability > probabilities) == 1)[0][0]

    # Add the new element
    aux_elements[:idx] = iterator[:idx]
    aux_elements[idx] = element
    aux_elements[idx + 1:] = iterator[idx:-2]

    aux_probabilities[:idx] = probabilities[:idx]
    aux_probabilities = property
    aux_probabilities[idx + 1:] = probabilities[idx:-2]

    for e in iterator[-1]:
        pass

    for e in iterator[-2]:
        pass

    return aux_elements, aux_elements, binaries

# Count how many times each ascii numbers repeats
def calculate_probabilities(probable_elements: np.ndarray, elements: np.ndarray) -> np.ndarray:
    denominator = len(elements)
    probabilities = np.zeros(len(probable_elements))

    for i in range(len(probable_elements)):
        probabilities[i] = np.sum(probable_elements[i] == elements) / denominator

    return probabilities


# Converts an array of ascii numbers to chars
def ascii_to_char(ascii_array: np.ndarray) -> np.ndarray:
    chars = np.empty(len(ascii_array), dtype="<U1")

    for i in range(len(ascii_array)):
        chars[i] = chr(ascii_array[i])

    return chars


def decode():
    pass
