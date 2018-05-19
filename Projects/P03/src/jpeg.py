import ycc
import dct
import quantification
import dc
import ac
import numpy as np


# Encodes a raw image
# Returns: Encoded images and number of blocks per line
def encode(raw_image: np.array, factor: float) -> (np.array, np.int):
    sampled_image = apply_subsample(raw_image, 4, 2, 0)
    ycc_image = ycc.encode(sampled_image)
    blocks = make_blocks(ycc_image)
    dc_elements = np.zeros(len(blocks))
    previous_quantified_block = None

    for i in range(len(blocks)):

        block_dct = dct.encode(blocks[i])
        block_quantification = quantification.encode(block_dct, factor)

        if i == 0:
            dc_elements[i] = dc.encode(None, block_quantification)
        else:
            dc_elements[i] = dc.encode(previous_quantified_block, block_quantification)

        block_ac = ac.encode(block_quantification)
        previous_quantified_block = block_quantification.copy()

        entropic_encoding(dc_elements, block_ac)

    return None


# Decodes a binary stream
# Returns: Decoded raw image
def decode(encoded_image: np.array) -> np.array:
    pass


def apply_subsample(image: np.array, sample_size: int, horizontal_ratio: int, vertical_ratio: int) -> np.array:
    pass


def __apply_image_croping(image, mod_factor):
    line_dim, col_dim = image.shape

    paddingLines = line_dim % mod_factor
    paddingCols = col_dim % mod_factor

    for i in range(paddingLines):
        image = np.delete(image, line_dim - 1, 0)
        line_dim -= 1

    for i in range(paddingCols):
        image = np.delete(image, col_dim - 1, 1)
        col_dim -= 1

    return image


def make_blocks(image: np.array) -> (np.array, np.int):

    m_size = 8
    image = __apply_image_croping(image, m_size) * 1.0

    line_dim, col_dim = image.shape
    number_of_blocks = int(line_dim / m_size) * int(col_dim / m_size)
    blocks = np.zeros((number_of_blocks, 8, 8))
    i = 0

    for line in range(int(line_dim / m_size)):
        for col in range(int(col_dim / m_size)):
            blocks[i] = __get_submatrix(image, line * m_size, col * m_size, m_size)
            i += 1

    return blocks


def __get_submatrix(matrix, line, col, dim):
    return matrix[line: line + dim, col: col + dim]

def entropic_encoding(block_dc: np.array, block_ac: np.array) -> np.array:
    # Merges DC with AC and append's eob
    pass


# EOB: end of block
def append_eob(block: np.array) -> np.array:
    # Appends the eob code to a single block
    pass


def make_image(blocks: np.array) -> np.array:
    # Assemble an image from multiple bit streams (blocks)
    # EOB delimits each block
    pass


def entropic_decoding(bit_stream: np.array) -> np.array:
    pass
