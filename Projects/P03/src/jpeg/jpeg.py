import numpy as np

from .entropic_coding import Stream
from . import dct
from . import quantification
from . import ycc
from .block import Block


class JPEG:

    header_size = 16
    total_layers = 3

    def __init__(self, image: np.ndarray, quality: int = 50):
        self.__raw_image = np.copy(image)
        self.__image = np.copy(image)
        self.__quality = quality
        self.__stream = Stream()
        self.__header = Stream()

    @classmethod
    def from_stream(cls, stream: str):
        cls.__stream = np.copy(stream)
        cls.decode(stream)

        return cls

    def __crop_image(self):
        total_lines, total_columns, layers = self.__image.shape

        excess_lines = total_lines % Block.size
        excess_columns = total_columns % Block.size

        for i in range(layers):
            self.__image[:, :, i] = self.__image[
                                    0: total_lines - excess_lines,
                                    0: total_columns - excess_columns, i
                                ]

    # TODO
    def __make_subsample(self):
        self.__image = self.__image

    def encode(self):
        self.__crop_image()
        self.__make_subsample()
        self.__image = ycc.encode(self.__image)

        for i in range(JPEG.total_layers):
            blocks = self.__make_blocks(self.__image[:, :, i])
            previous_block = None

            if i == 0:
                self.__encode_header(blocks.shape[0], blocks.shape[1])

            for row in range(blocks.shape[0]):
                for column in range(blocks.shape[1]):
                    block = dct.encode(blocks[row, column])
                    block = quantification.encode(blocks[row, column])

                    block.encode(previous_block)
                    self.__stream.join(block.stream)

                    previous_block = block

    @classmethod
    def decode(cls, stream: str):
        header = stream[:JPEG.header_size * 2 + 1]
        stream = stream[JPEG.header_size * 2 + 1:]

        rows = np.int(header[JPEG.header_size + 1], 2)
        columns = np.int(header[JPEG.header_size: JPEG.header_size * 2 + 1], 2)

        total_blocks_horizontal = np.int(columns / Block.size)
        total_blocks_vertical = np.int(rows / Block.size)

        image = np.zeros((
            JPEG.total_layers,
            total_blocks_horizontal * Block.size,
            total_blocks_vertical * Block.size,
        ))

        for i in range(JPEG.total_layers):
            blocks = cls.__make_blocks(image[i])
            previous_block = None

            for blocks_row in range(blocks.shape[0]):
                for blocks_column in range(blocks.shape[1]):
                    block, stream = Block.decode(previous_block, stream)
                    blocks[blocks_row, blocks_column] = block
                    image[
                        i,
                        blocks_row * Block.size: blocks_row * Block.size + Block.size,
                        blocks_column * Block.size: blocks_column * Block.size + Block.size
                    ] = block.elements

                    previous_block = block

        return JPEG(image)

    def __encode_header(self, rows: int, columns: int):
        row_bits = np.binary_repr(rows).rjust(JPEG.header_size, "0")
        column_bits = np.binary_repr(columns).rjust(JPEG.header_size, "0")

        self.__header.join(Stream(row_bits))
        self.__header.join(Stream(column_bits))

    def __make_blocks(self, image_layer: np.ndarray):
        # Calculate the total number of blocks
        rows = image_layer.shape[0]
        columns = image_layer.shape[1]

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

    @property
    def stream(self):
        if self.__header is None or self.__stream is None:
            self.encode()

        final_stream = Stream()
        final_stream.join(self.__header).join(self.__stream)

        return final_stream
