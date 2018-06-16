from numpy import array
from cv2 import imwrite, IMWRITE_JPEG_QUALITY

from . import FrameMovementVectors


class Frame:
    FRAME_SYNTAX = "{:0>4}"

    def __init__(self, pixels: array, index: int):
        self.__movement_vectors = None
        self.__pixels = pixels
        self._index = index

    def __sub__(self, other):
        return self.__pixels - other.__pixels

    def __str__(self):
        return "{} Frame".format(self.__pixels.index_str)

    @property
    def shape(self):
        return self.__pixels.shape

    @property
    def movement_vectors(self) -> FrameMovementVectors:
        return self.__movement_vectors

    @movement_vectors.setter
    def movement_vectors(self, movement_vectors: FrameMovementVectors):
        self.__movement_vectors = movement_vectors

    @property
    def pixels(self):
        return self.__pixels


    @property
    def index(self):
        return self._index

    @property
    def index_str(self):
        return Frame.FRAME_SYNTAX.format(self.index)

    def write(self, path: str, quality: int):
        imwrite(path, self.__pixels, (IMWRITE_JPEG_QUALITY, quality))


class IntraFrame(Frame):
    def __str__(self):
        return "{} IntraFrame".format(super().index_str)


class InterFrame(Frame):
    @staticmethod
    def from_intra_frame(frame: IntraFrame, ref_frame: IntraFrame, index: int):
        return InterFrame(frame - ref_frame, index)

    def __str__(self):
        return "{} InterFrame".format(super().index_str)
