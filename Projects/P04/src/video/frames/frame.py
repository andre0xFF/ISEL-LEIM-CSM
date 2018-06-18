from cv2 import imwrite, IMWRITE_JPEG_QUALITY

from numpy import arange, array, ndarray
from numpy import int

from . import ChrominanceLayer
from . import LuminanceLayer


class Frame:
    def __init__(self, pixels: ndarray, index: int):
        self.__index = index
        self.__pixels = pixels

    def __repr__(self):
        return "Frame({})".format(self.__index)

    def __sub__(self, other):
        return self.__pixels - other.__pixels

    def __getitem__(self, item):
        return self.__pixels[item]

    @property
    def index(self):
        return self.__index

    @property
    def shape(self):
        return self.__pixels.shape

    @property
    def size(self):
        return self.__pixels.size

    @property
    def pixels(self):
        return self.__pixels

    def write(self, path: str, quality: int):
        imwrite(path, self.__pixels, (IMWRITE_JPEG_QUALITY, quality))


class YCbCrFrame(Frame):
    def __init__(self, pixels: ndarray, index: int):
        super().__init__(pixels, index)

        self.__layers = array([
            LuminanceLayer(pixels[:, :, 0]),
            ChrominanceLayer(pixels[:, :, 1]),
            ChrominanceLayer(pixels[:, :, 2]),
        ])

    def __sub__(self, other):
        self.__layers - other.__layers
        return super().__sub__(other)

    def __str__(self):
        return "Luminance: {}\n\nChrominance B: {}\n\nChrominance R: {}".format(
            self.__layers[0].__str__(),
            self.__layers[1].__str__(),
            self.__layers[2].__str__(),
        )

    @property
    def layers(self):
        return self.__layers


if __name__ == "__main__":
    image = array(arange(17 * 2 * 16 * 2 * 3)).reshape((17 * 2, 16 * 2, 3))
    frame = YCbCrFrame(image, 0)
