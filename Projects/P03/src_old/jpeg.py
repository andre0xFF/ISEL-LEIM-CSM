import ycc
import dct
import quantification
import dc
import ac
import numpy as np


# Encodes a raw image
# Returns: Encoded image and number of blocks
def encode(raw_image: np.ndarray, block_size: float = 8, quality: int = 50) -> str:
    stream = ""
    raw_image = crop_image(raw_image, block_size)

    # sampled_image = apply_subsample(raw_image, 4, 2, 0)
    sampled_image = np.copy(raw_image)

    ycc_image = ycc.encode(sampled_image)
    layers = ycc_image.shape[2]

    for i in layers:
        stream = "{}{}".format(stream, encode_layer(ycc_image[:, :, i]))

    return stream


def encode_layer(image_layer: np.ndarray, block_size: float = 8, quality: int = 50) -> str:
    blocks, total_blocks_h, total_blocks_v = make_blocks(image_layer)
    previous_block = None

    for i in range(len(blocks)):
        dct_block = dct.encode(blocks[i])
        quantified_block = quantification.encode(dct_block, quality)

        # The first block has no previous block
        dc_size, dc_amplitude = dc.encode(previous_block if i > 0 else None, quantified_block)
        # ac_value = dc.encode(previous_block, quantified_block)

        block_stream = entropic_coding(dc_size, dc_amplitude)
        stream = "{}{}".format(stream, block_stream)

        previous_block = quantified_block

    return stream


# Decodes a binary stream
# Returns: Decoded raw image
def decode(encoded_image: str) -> np.ndarray:
    m_size = 8
    n_lines = int(encoded_image[0: 10], 2)
    n_cols = int(encoded_image[10: 20], 2)
    reconstructed_image = np.zeros((1, n_lines * m_size, n_cols * m_size))
    i = 0
    row = 0
    col = 0

    while encoded_image != '':
        dc_value, encoded_image = dc.decode(encoded_image)
        block, encoded_image = ac.decode(encoded_image)
        block[0][0] = dc_value
        apply_block(reconstructed_image, block, row, col, m_size)

        col = ((col + 1) * m_size) % n_cols
        if col == 0:
            row = (row + 1) * m_size
        i += 1

    return reconstructed_image


# TODO: not working
def apply_subsample(image: np.ndarray, horizontal_ratio: int, vertical_ratio: int, sample_size: int = 4) -> np.ndarray:
    rows, columns = image.shape
    x = 0
    y = 0

    for row in range(rows):
        for col in range(columns):
            if x < rows and y < columns:
                sub_matrix = np.ones((1, horizontal_ratio, vertical_ratio)) * image[x][y]
                image = apply_block(image, sub_matrix, x, y, 2)
                y += vertical_ratio
        x += horizontal_ratio
        y = 0

    return image





def make_blocks(image: np.ndarray, size: np.int = 8) -> (np.ndarray, np.int):
    total_lines, total_columns = image.shape
    total_blocks_h = np.int(total_columns / size)
    total_blocks_v = np.int(total_lines / size)
    total_blocks = total_blocks_h * total_blocks_v
    blocks = np.zeros((total_blocks, size, size))

    i = 0

    for row in range(total_blocks_v):
        for column in range(total_blocks_h):
            blocks[i] = make_block(image, row * size, column * size, size)
            i = i + 1

    return blocks, total_blocks_h, total_blocks_v


def make_block(matrix, row, column, factor):
    return matrix[row: row + factor, column: column + factor]


def apply_block(matrix, block, line, col, dim):
    matrix[line: line + dim, col: col + dim] = block
    return matrix


def entropic_coding(dc_size: np.int, dc_amplitude: np.int) -> str:
    stream = ""

    stream = "{dc_size}{dc_signal}{dc_amplitude}".format(
        dc_size=dc.get_sizes()[dc_size],
        dc_signal=0 if dc_amplitude > 0 else 1,
        dc_amplitude=bin(dc_amplitude)[2:]
    )

    # for i in ac_value:
    #     stream = "{stream}{ac_value}".format(
    #         stream=stream,
    #         # TODO
    #         ac_value=ac_keys.ac_value[1]
    #     )

    return stream


def entropic_decoding(stream: str) -> (np.int, np.int):
    size_bits = stream[0]
    dc_size = 0
    index = 0

    # Find the DC size
    for i in range(len(stream)):
        dc_size = dc.bits_to_size(size_bits)

        if dc_size is not None:
            index = i
            break

        size_bits = "{}{}".format(size_bits, stream[i])

    if index == 0:
        return None

    # Get and convert the DC signal
    signal_bits = stream[index]
    dc_signal = 1 if signal_bits == "0" else -1

    # Get and convert the DC amplitude
    dc_amplitude_bits = stream[index + 1: index + dc_size]
    dc_amplitude = np.int(dc_amplitude_bits, 2) * dc_signal

    return dc_size, dc_amplitude


def _test():
    block_0 = np.array([
        [80, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    block_1 = np.array([
        [80, 2, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    dc_size, dc_amplitude = dc.encode(None, block_0)

    stream = entropic_coding(dc_size, dc_amplitude)
    dc_size, dc_amplitude = entropic_decoding(stream)


if __name__ == "__main__":
    _test()
