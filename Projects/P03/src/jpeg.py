import ycc
import dct
import quantification
import dc
import ac
import numpy as np


# Encodes a raw image
# Returns: Encoded images and number of blocks per line
def encode(raw_image: np.array, factor: float) -> (np.array, np.int):

    raw_image = crop_image(raw_image, factor)
    sampled_image = apply_subsample(raw_image, 4, 2, 0)
    ycc_image = ycc.encode(sampled_image)
    blocks, line_dim, col_dim = make_blocks(ycc_image)
    previous_quantified_block = None
    bit_stream = ''

    for i in range(len(blocks)):

        block_dct = dct.encode(blocks[i])
        block_quantification = quantification.encode(block_dct, factor)

        if i == 0:
            bit_stream += dc.encode(None, block_quantification)
        else:
            bit_stream += dc.encode(previous_quantified_block, block_quantification)

        bit_stream += ac.encode(block_quantification)

        previous_quantified_block = block_quantification.copy()

    return bit_stream


# Decodes a binary stream
# Returns: Decoded raw image
def decode(encoded_image: str) -> np.array:
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


def apply_subsample(image: np.array, horizontal_ratio: int, vertical_ratio: int, sample_size: int = 4) -> np.array:
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


def crop_image(image, factor):
    image = np.copy(image)
    total_lines, total_columns = image.shape

    excess_lines = total_lines % factor
    excess_columns = total_columns % factor

    image = image[0: total_lines - excess_lines, 0: total_columns - excess_columns]

    return image


def make_blocks(image: np.array, factor: np.int = 8) -> (np.array, np.int):

    total_lines, total_columns = image.shape
    total_blocks_h = np.int(total_columns / factor)
    total_blocks_v = np.int(total_lines / factor)
    total_blocks = total_blocks_h * total_blocks_v
    blocks = np.zeros((total_blocks, factor, factor))

    i = 0

    for row in range(total_blocks_v):
        for column in range(total_blocks_h):
            blocks[i] = make_block(image, row * factor, column * factor, factor)
            i = i + 1

    return blocks


def make_block(matrix, row, column, factor):
    return matrix[row: row + factor, column: column + factor]


def apply_block(matrix, block, line, col, dim):
    matrix[line: line + dim, col : col + dim] = block
    return matrix


def _test():
    image = np.reshape(np.arange(256), (16, 16))
    blocks = make_blocks(image)
    print(blocks)

    image = apply_subsample(image, 2, 2)
    print(image)


if __name__ == "__main__":
    _test()
