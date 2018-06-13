from numpy import array
from cv2 import imwrite, IMWRITE_JPEG_QUALITY


class Frame:
    def write(self, path: str, quality: int):
        raise NotImplemented

    def __sub__(self, other):
        raise NotImplemented

    def __str__(self):
        raise NotImplemented


class IFrame:
    FRAME_SYNTAX = "{:0>4}"

    def __init__(self, frame: array, index: int):
        self.__frame = frame
        self.__index = index

    @property
    def frame(self):
        return self.__frame

    @property
    def index(self):
        return self.__index

    @property
    def index_str(self):
        return IFrame.FRAME_SYNTAX.format(self.index)

    def write(self, path: str, quality: int):
        imwrite(path, self.__frame, (IMWRITE_JPEG_QUALITY, quality))

    def __sub__(self, other):
        return self.__frame - other.__frame


class IntraFrame(Frame):
    def __init__(self, frame: array, index: int):
        self.__frame = IFrame(frame, index)

    def write(self, path: str, quality: int):
        self.__frame.write(path, quality)

    def __sub__(self, other):
        return self.__frame.__sub__(other.__frame)

    def __str__(self):
        return "{} IntraFrame".format(self.__frame.index_str)


class InterFrame(Frame):
    def __init__(self, frame: IntraFrame, ref_frame: IntraFrame, index: int):
        frame = frame - ref_frame
        self.__frame = IFrame(frame, index)

    def write(self, path: str, quality: int):
        self.__frame.write(path, quality)

    def __sub__(self, other):
        return self.__frame.__sub__(other.__frame)

    def __str__(self):
        return "{} InterFrame".format(self.__frame.index_str)
