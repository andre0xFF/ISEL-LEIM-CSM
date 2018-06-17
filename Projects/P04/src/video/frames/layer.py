from numpy import array, ndarray
from numpy import int

from . import Block


class Layer:
    def __init__(self, pixels: ndarray, block_size: int):
        self.__pixels: ndarray = pixels.copy()
        self.__block_size: int = block_size
        self.__blocks: ndarray = None
        self.__trim_pixels()

    def __str__(self):
        return self.__pixels.__str__()

    def __sub__(self, other):
        if self.__blocks is not None:
            self.__blocks - other.__blocks

        return self.__pixels - other.__pixels

    @property
    def blocks(self):
        return self.__blocks.copy()

    @property
    def shape(self):
        return self.__pixels.shape

    @property
    def pixels(self):
        return self.__pixels.copy()

    def __trim_pixels(self):
        rows_value = self.__pixels.shape[0] % self.__block_size
        cols_value = self.__pixels.shape[1] % self.__block_size
        total_rows = self.__pixels.shape[0] - rows_value
        total_cols = self.__pixels.shape[1] - cols_value

        self.__pixels = self.__pixels[0: total_rows, 0: total_cols]

    def make_blocks(self):
        self.__blocks = array(
            [Block] * int((self.__pixels.shape[0] * self.__pixels.shape[1]) / (self.__block_size * self.__block_size))
        ).reshape(
            (int(self.__pixels.shape[0] / self.__block_size), int(self.__pixels.shape[1] / self.__block_size))
        )

        for r in range(self.__blocks.shape[0]):
            for c in range(self.__blocks.shape[1]):
                r1 = r * self.__block_size
                c1 = c * self.__block_size
                r2 = r * self.__block_size + self.__block_size
                c2 = c * self.__block_size + self.__block_size

                self.__blocks[r, c] = Block(self.__pixels[r1: r2, c1: c2], (r1, c1), (r, c), self.__block_size)

class LuminanceLayer(Layer):
    BLOCK_SIZE = 16

    def __init__(self, pixels: ndarray):
        super().__init__(pixels, LuminanceLayer.BLOCK_SIZE)

    def __repr__(self):
        return "Luminance"


class ChrominanceLayer(Layer):
    BLOCK_SIZE = 8

    def __init__(self, pixels: ndarray):
        super().__init__(pixels, ChrominanceLayer.BLOCK_SIZE)

    def __repr__(self):
        return "Chrominance"