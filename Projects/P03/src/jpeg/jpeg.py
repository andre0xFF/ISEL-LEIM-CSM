import numpy as np

from . import ycc
from . import quantification
from . import dct
from .block import Block


class JPEG:

    def __init__(self, image: np.ndarray, quality: int = 50):
        self.__raw_image = np.copy(image)
        self.__image = np.copy(image)
        self.__quality = quality
        self.__stream = ""

    def __crop_image(self):
        total_lines, total_columns, layers = self.__image.shape

        excess_lines = total_lines % Block.size
        excess_columns = total_columns % Block.size

        # Create a copy so that this is an atomic process
        image = np.copy(self.__image)

        for i in range(layers):
            image[:, :, i] = image[0: total_lines - excess_lines, 0: total_columns - excess_columns, i]

        self.__image = image

    # TODO
    def __make_subsample(self):
        self.__image = self.__image

    def encode(self):
        self.__crop_image()
        self.__make_subsample()
        self.__image = ycc.encode(self.__image)

        layers = self.__image.shape[2]

        for i in range(layers):
            blocks = self.__make_blocks(self.__image[:, :, i])
            previous_block = None

            for row in range(blocks.shape[0]):
                for column in range(blocks.shape[1]):
                    block = dct.encode(blocks[row, column])
                    block = quantification.encode(blocks[row, column])

                    block.dpcm_encode(previous_block)
                    block.rlc_encode()

                    previous_block = block

                    self.__stream = "{}{}".format(self.__stream, block.stream)

    def __make_blocks(self, image_layer: np.ndarray):
        # Calculate the total number of blocks
        rows = self.__image.shape[0]
        columns = self.__image.shape[1]

        total_blocks_horizontal = np.int(columns / Block.size)
        total_blocks_vertical = np.int(rows / Block.size)
        total_blocks = total_blocks_horizontal * total_blocks_vertical

        # Initialize a bi-dimensional array of blocks
        blocks = [Block] * total_blocks
        blocks = np.reshape(blocks, (total_blocks_horizontal, total_blocks_vertical))

        # Make each block
        for blocks_row in range(blocks.shape[0]):
            for blocks_column in range(blocks.shape[1]):
                elements_row = blocks_row * Block.size
                elements_column = blocks_column * Block.size
                elements = image_layer[
                               elements_row: elements_row + Block.size,
                               elements_column: elements_column + Block.size
                           ]

                blocks[blocks_row, blocks_column] = Block(elements)

        return blocks
