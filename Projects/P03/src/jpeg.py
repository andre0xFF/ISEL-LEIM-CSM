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


def crop_image(image, factor):
    image = np.copy(image)
    total_lines, total_columns = image.shape

    excess_lines = total_lines % factor
    excess_columns = total_columns % factor

    image = image[0: total_lines - excess_lines, 0: total_columns - excess_columns]

    return image


def make_blocks(image: np.array, factor: np.int = 8) -> (np.array, np.int):
    image = crop_image(image, factor)
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


def make_image(blocks: np.array) -> np.array:
    # Assemble an image from multiple bit streams (blocks)
    # EOB delimits each block
    pass


def entropic_encoding(block_dc: np.array, block_ac: np.array) -> np.array:
    # Merges DC with AC and append's eob
    pass


def entropic_decoding(bit_stream: np.array) -> np.array:
    pass


def _test():
    image = np.reshape(np.arange(256), (16, 16))
    blocks = make_blocks(image)
    print(blocks)


if __name__ == "__main__":
    _test()