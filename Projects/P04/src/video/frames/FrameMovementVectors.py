from numpy import ndarray


class FrameMovementVectors:
    def __init__(self, block_size: int, vectors: ndarray):
        self.__vectors = vectors

    @property
    def vectors(self):
        return self.__vectors

    @vectors.setter
    def vectors(self, vectors: ndarray):
        self.__vectors = vectors
