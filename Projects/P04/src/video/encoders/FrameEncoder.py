from numpy import array

from ..frames import Frame
from ..frames import FrameMovementVectors
from ..search_strategies import ThreeSteps


class FrameEncoder:
    def __init__(self):
        self.__search_strategy = ThreeSteps()

    def encode(self, previous_frame: Frame, frame: Frame) -> (Frame, Frame, FrameMovementVectors):
        frame.movement_vectors = self.__search_strategy.search(frame, previous_frame)
        predicted_frame = self.predict(frame, previous_frame)
        error_frame = Frame(frame - predicted_frame, frame.index)

        return frame, None, frame.movement_vectors

    # Applies the frame's movement vectors to the previous frame
    def predict(self, frame: Frame, previous_frame: Frame) -> Frame:
        return Frame(None, frame.index)

    def decode(self, frame: Frame, error: array) -> Frame:
        # TODO
        pass
