from numpy import ndarray


class Vectors:
    def __init__(self, vectors: ndarray):
        self.__vectors: ndarray = vectors

    @property
    def vectors(self):
        return self.__vectors

    @vectors.setter
    def vectors(self, value):
        self.__vectors = value

    def __getitem__(self, item):
        return self.__vectors[item]

    def __setitem__(self, key, value):
        self.__vectors[key] = value
