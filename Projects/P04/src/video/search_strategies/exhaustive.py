from math import inf

from numpy import ndarray, array
from numpy import power, sqrt

from . import SearchStrategy
from ..frames import Block
from ..frames import Layer


class Exhaustive(SearchStrategy):
    SEARCH_WINDOW = 15

    def find_similar(self, block: Block, layer: Layer) -> (Block, float):
        # Original block coordinates
        r, c = block.origin[0]

        pixels: ndarray = layer.pixels
        block_size = layer.blocks[0, 0].size

        total_errors = power(2 * Exhaustive.SEARCH_WINDOW + 2, 2)
        errors = array([inf] * total_errors).reshape((int(sqrt(total_errors)), int(sqrt(total_errors))))

        blocks = array([Block] * total_errors).reshape((int(sqrt(total_errors)), int(sqrt(total_errors))))

        # Indexes for errors and blocks
        r2 = -1
        c2 = -1

        for r1 in range(r + -1 * Exhaustive.SEARCH_WINDOW, r + Exhaustive.SEARCH_WINDOW):
            r2 += 1

            if r1 < 0:
                continue

            r3 = r1 + block_size

            if r3 > pixels.shape[0]:
                continue

            for c1 in range(c + -1 * Exhaustive.SEARCH_WINDOW, c + Exhaustive.SEARCH_WINDOW):
                c2 += 1

                if c1 < 0:
                    continue

                c3 = c1 + block_size

                if c3 > pixels.shape[1]:
                    continue

                blocks[r2, c2] = Block(pixels[r1: r3, c1: c3], (r1, c1), (r2, c2), block_size)
                errors[r2, c2] = self.calculate_error(blocks[r2, c2], block)

            c2 = -1

        r, c, min_error = self._find_smallest_error(errors)
        return blocks[r, c], min_error
