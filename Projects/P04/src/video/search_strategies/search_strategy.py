from math import inf

from numpy import argwhere, min
from numpy import array, ndarray
from sklearn.metrics import mean_squared_error as error

from ..frames import Block
from ..frames import Layer


class SearchStrategy:
    def find_similar(self, previous_layer: Layer, block: Block) -> (Block, float):
        raise NotImplementedError("Abstract")

    @staticmethod
    def calculate_error(previous_block: Block, block: Block) -> float:
        return error(previous_block.pixels, block.pixels)

    def _find_smallest_error(self, errors: ndarray):
        min_error = min(errors)
        r, c = argwhere(errors == min_error)[0]

        return r, c, min_error


class Iterative(SearchStrategy):
    def find_similar(self, previous_layer: Layer, block: Block) -> (Block, float):
        previous_blocks = previous_layer.blocks
        errors = array([inf] * previous_blocks.shape[0] * previous_blocks.shape[1]).reshape(previous_blocks.shape)

        for r in range(previous_blocks.shape[0]):
            for c in range(previous_blocks.shape[1]):
                errors[r, c] = self.calculate_error(previous_blocks[r, c], block)

        r, c, min_error = self._find_smallest_error(errors)

        return previous_blocks[r, c], min_error