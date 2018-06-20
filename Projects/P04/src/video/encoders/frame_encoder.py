from numpy import array, zeros, int, ndarray

from . import Vectors
from ..frames import Block
from ..frames import YCbCrFrame
from ..search_strategies import Exhaustive


class FrameEncoder:
    def __init__(self):
        self.__search_strategy = Exhaustive()

    def encode(self, previous_frame: YCbCrFrame, frame: YCbCrFrame) -> (YCbCrFrame, ndarray, YCbCrFrame):
        layers = frame.layers
        previous_layers = previous_frame.layers
        predicted_image = zeros(frame.size, dtype=int).reshape(frame.shape)

        # List of origin and target vectors
        vectors = array([Vectors] * frame.layers.size)

        for l in range(previous_layers.shape[0]):
            vectors[l] = Vectors((
                zeros(2 * 2 * previous_layers[l].blocks.size, dtype=int)
            ).reshape(
                (previous_layers[l].blocks.size, 2 * 2)
            ))

            previous_blocks = previous_layers[l].blocks

            for r in range(previous_blocks.shape[0]):
                for c in range(previous_blocks.shape[1]):
                    similar_block: Block = self.__search_strategy.find_similar(previous_blocks[r, c], layers[l])[0]
                    r2, c2 = similar_block.origin[0]

                    # Predict the block
                    r3 = r2 + similar_block.size
                    c3 = c2 + similar_block.size

                    previous_blocks[r, c].target = r2, c2
                    predicted_image[r2: r3, c2: c3, l] = previous_blocks[r, c].pixels

                    # Collect origin and target vector
                    r4 = r * previous_blocks.shape[1] + c
                    vectors[l][r4, 0: 2] = previous_blocks[r, c].origin[0]
                    vectors[l][r4, 2: 4] = previous_blocks[r, c].target

        error_frame = YCbCrFrame(frame.pixels - predicted_image, -1 * frame.index)
        predicted_frame = YCbCrFrame(predicted_image, frame.index)

        return predicted_frame, vectors, error_frame

    def decode(self, previous_frame: YCbCrFrame, error_frame: YCbCrFrame, vectors: ndarray) -> YCbCrFrame:
        previous_layers = previous_frame.layers
        predicted_image = zeros(previous_frame.size, dtype=int).reshape(previous_frame.shape)

        for l in range(previous_layers.shape[0]):
            previous_blocks = previous_layers[l].blocks
            block_size = previous_layers[l].block_size

            for r in range(previous_blocks.shape[0]):
                for c in range(previous_blocks.shape[1]):
                    r2 = r / previous_blocks.shape[1] - c
                    r3, c3 = vectors[l][r2, 2: 4]
                    r4 = r3 + block_size
                    c4 = c3 + block_size
                    predicted_image[r3: r4, c3: c4, l] = previous_blocks[r, c].pixels

        predicted_frame = YCbCrFrame(error_frame.pixels + predicted_image, previous_frame.index + 1)

        return predicted_frame
