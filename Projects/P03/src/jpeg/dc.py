from numpy import abs
from numpy import int


class DC:

    k3 = {
        0: "00",
        1: "010",
        2: "011",
        3: "100",
        4: "101",
        5: "110",
        6: "1110",
        7: "11110",
        8: "111110",
        9: "1111110",
        10: "11111110",
        11: "111111110",
    }

    def __init__(self, amplitude: int):
        self.__amplitude = amplitude
        self.__amplitude_bits = bin(abs(self.__amplitude))[2:]

        if self.__amplitude == 0:
            self.__size = 0
        else:
            self.__size = len(self.__amplitude_bits)

        self.__size_bits = DC.k3.get(self.__size)

        self.__signal = -1 if self.__amplitude < 0 else 1
        self.__signal_bits = 1 if self.__amplitude < 0 else 0

    @property
    def amplitude(self):
        return self.__amplitude

    @property
    def size(self):
        return self.__size

    @property
    def signal(self):
        return self.__signal

    @property
    def stream(self):
        if self.__amplitude == 0:
            return "{size_bits}".format(
                size_bits=self.__size_bits
            )

        return "{size_bits}{signal_bits}{amplitude_bits}".format(
            size_bits=self.__size_bits,
            signal_bits=self.__signal_bits,
            amplitude_bits=self.__amplitude_bits
        )

    def __str__(self):
        if self.__amplitude == 0:
            return "[{size_bits}]".format(
                size_bits=self.__size_bits
            )

        return "[{size_bits}, {signal_bits} {amplitude_bits}]".format(
            size_bits=self.__size_bits,
            signal_bits=self.__signal_bits,
            amplitude_bits=self.__amplitude_bits
        )
