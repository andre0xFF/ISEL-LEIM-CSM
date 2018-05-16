import ycc
import dct
import quantification
import dc
import ac
import numpy as np


# Encodes a raw image
# Returns: Encoded images and number of blocks per line
def encode(raw_image: np.array) -> (np.array, np.int):
    sampled_image = apply_subsample(raw_image, 4, 2, 0)
    ycc_image = ycc.encode(sampled_image)
    blocks = make_blocks(ycc_image)

    for block in blocks:
        block_dct = dct.encode(block)
        block_quantification = quantification.encode()

        block_dc = dc.encode(block_quantification)
        block_ac = ac.encode(block_quantification)

        entropic_encoding(block_dc, block_ac)

    return None


# Decodes a binary stream
# Returns: Decoded raw image
def decode(encoded_image: np.array) -> (np.array):
    return None


def apply_subsample(image: np.array, sample_size: int, horizontal_ratio: int, vertical_ratio: int) -> (np.array):
    pass


def make_blocks(image: np.array) -> (np.array, np.int):
    # TODO: Transform the image in multiple of 8
    # TODO: Slice the image into multiple bocks of 8x8
    pass


def entropic_encoding(block_dc: np.array, block_ac: np.array) -> (np.array):
    # Merges DC with AC and append's eob
    pass


# EOB: end of block
def append_eob(block: np.array) -> (np.array):
    # Appends the eob code to a single block
    pass


def make_image(blocks: np.array) -> (np.array):
    # Assemble an image from multiple bit streams (blocks)
    # EOB delimits each block
    pass


def entropic_decoding(bit_stream: np.array) -> (np.array):
    pass
