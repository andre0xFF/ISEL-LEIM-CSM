import sklearn.metrics
from numpy import logical_not
from numpy import ndarray

from ..frames import Frame


class SearchStrategy:
    LUMINANCE_BLOCK_SIZE = 16
    CHROMINANCE_BLOCK_SIZE = 8

    BLOCK_SIZES = [
        LUMINANCE_BLOCK_SIZE,
        CHROMINANCE_BLOCK_SIZE,
        CHROMINANCE_BLOCK_SIZE
    ]

    def search(self, previous_frame: Frame, frame: Frame):
        raise NotImplemented("Abstract")

    def __trim_image(self, image: ndarray):
        rows = image.shape[0]
        rows_factor = logical_not(rows / 2)

        columns = image.shape[1]
        columns_factor = logical_not(columns / 2)

        return image[0: rows - columns_factor, 0: columns - columns_factor, :]

    def _calculate_error(self, block_1: ndarray, block_2: ndarray):
        return sklearn.metrics.mean_squared_error(block_1, block_2)
