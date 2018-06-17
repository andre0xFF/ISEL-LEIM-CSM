from numpy import array, zeros

from ..search_strategies import Iterative
from ..search_strategies import Exhaustive
from ..frames import YCbCrFrame


class FrameEncoder:
    def __init__(self):
        self.__search_strategy = Exhaustive()

    def encode(self, previous_frame: YCbCrFrame, frame: YCbCrFrame):
        layers = frame.layers
        previous_layers = previous_frame.layers
        predicted_image = zeros(frame.size).reshape(frame.shape)

        for l in range(layers.shape[0]):
            blocks = layers[l].blocks

            for r in range(blocks.shape[0]):
                for c in range(blocks.shape[1]):
                    previous_similar_block = self.__search_strategy.find_similar(previous_layers[l], blocks[r, c])[0]
                    blocks[r, c].target = previous_similar_block.origin[0]

                    # predicted_image[:, :, l]

    # Applies the frame's movement vectors to the previous frame
    def predict(self, frame: YCbCrFrame, previous_frame: YCbCrFrame) -> YCbCrFrame:
        return YCbCrFrame(None, frame.index)

    def decode(self, frame: YCbCrFrame, error: array) -> YCbCrFrame:
        # TODO
        pass
