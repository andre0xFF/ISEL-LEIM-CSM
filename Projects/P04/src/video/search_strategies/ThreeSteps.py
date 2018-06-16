from math import inf

from numpy import ndarray, reshape, floor

from . import SearchStrategy
from ..frames import Frame


class ThreeSteps(SearchStrategy):
    def search(self, previous_frame: Frame, frame: Frame):
        block_size = SearchStrategy.BLOCK_SIZES

        # Layers
        for l in range(frame.shape[2]):
            h_total_blocks = frame.shape[1] / block_size[l]
            v_total_blocks = frame.shape[0] / block_size[l]
            total_blocks = int(h_total_blocks * v_total_blocks)

            blocks = reshape(frame.pixels[:, :, l], (block_size[l], block_size[l], total_blocks))
            previous_blocks = reshape(previous_frame.pixels[:, :, l], (block_size[l], block_size[l], total_blocks))

            min_error = inf
            row = 0
            col = 0

            for i in range(blocks.shape[2]):
                for j in range(previous_blocks.shape[2]):
                    error = self._calculate_error(blocks[i], previous_blocks[j])

                    if error < min_error:
                        min_error = error
                        row = floor(j / v_total_blocks)
                        col = ((floor(j / v_total_blocks) + 1) - row) * v_total_blocks


    def __find_block(self, block: ndarray, pixels: ndarray):
        pass