from numpy import array

from . import Frame
from . import InterFrame
from . import IntraFrame
from . import Vector
from .search_strategies import ThreeSteps


class FrameEncoder:
    def __init__(self):
        search_strategy = ThreeSteps()

    def encode(self, intra_frame: IntraFrame, inter_frame: InterFrame) -> (Vector, array):
        pass

    def decode(self, vector: Vector, error: array) -> Frame:
        pass