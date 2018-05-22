from numpy import argwhere
from numpy import array
from numpy import int

from .dc import DC


def encode(previous_block, block) -> DC:
    if previous_block is None:
        return DC(block.elements[0, 0])

    return DC(block.elements[0, 0] - previous_block.elements[0, 0])


def decode(stream: str) -> (DC,  str):
    amplitude = 0
    amplitudes_bits = array(list(DC.k3.values()))

    # Decode DC
    for i in range(1, len(stream) + 1):
        size = argwhere(stream[0: i] == amplitudes_bits)

        # No size found, keep looking
        if size.shape[0] == 0:
            continue

        size = size[0, 0]

        # Size 0 has no signal bits nor amplitude bits
        if size == 0:
            stream = stream[i + size:]
            break

        # signal = 1 if int(stream[i: i + 1]) == 0 else -1
        signal = 1 if int(stream[i]) == 0 else -1
        amplitude = int(stream[i + 1: i + size + 1], 2) * signal
        stream = stream[i + size + 1:]
        break

    return DC(amplitude), amplitude, stream
