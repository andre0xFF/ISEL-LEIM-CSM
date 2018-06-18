from numpy import int
from numpy import ndarray


class Block:
    def __init__(self, pixels: ndarray, frame_origin: tuple, block_origin: tuple, size: int):
        self.__pixels: ndarray = pixels
        self.__frame_origin: tuple = frame_origin
        self.__frame_target: tuple = None
        self.__block_origin: tuple = block_origin
        self.__size: int = size

    def __sub__(self, other):
        return self.__pixels - other.__pixels

    def __str__(self):
        return "{}".format(self.__pixels)

    def __repr__(self):
        return "Origin: ({}), Target: ({})".format(self.__frame_origin, self.__frame_target)

    @property
    def origin(self):
        return self.__frame_origin, self.__block_origin

    @property
    def target(self):
        return self.__frame_target

    @target.setter
    def target(self, value):
        self.__frame_target = value

    @property
    def pixels(self):
        return self.__pixels.copy()

    @property
    def shape(self):
        return self.__pixels.shape

    @property
    def size(self):
        return self.__size
