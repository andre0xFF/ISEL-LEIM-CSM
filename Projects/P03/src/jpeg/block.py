from numpy import copy, ones
from numpy import ndarray

from . import dpcm
from . import rlc


class Block:

    eob = "1010"
    size = 8

    def __init__(self, elements: ndarray):
        self.__raw_elements = copy(elements)
        self.__elements = copy(elements)
        self.__dc = None
        self.__ac_elements = None

    @classmethod
    def from_stream(cls, stream: str):
        cls.__dc, cls.__ac, cls.__raw_elements = cls.decode(stream)
        cls.__elements = copy(cls.__raw_elements)

        return cls

    @classmethod
    def from_dc_ac(cls, dc, ac_elements: ndarray):
        cls.__dc = dc
        cls.__ac_elements = ac_elements

        return cls

    @property
    def elements(self):
        return self.__elements

    @property
    def dc(self):
        return self.__dc

    @property
    def ac(self):
        return self.__ac_elements

    @elements.setter
    def elements(self, elements: ndarray):
        self.__elements = elements

    def __str__(self):
        return self.__elements.__str__()

    def dpcm_encode(self, previous_block):
        self.__dc = dpcm.encode(previous_block, self)

    def rlc_encode(self):
        self.__ac_elements = rlc.encode(self)

    @staticmethod
    def decode(stream: str):
        dc, dc_amplitudes, stream = dpcm.decode(stream)
        ac, ac_amplitudes, stream = rlc.decode(stream)

        if stream != Block.eob:
            return None

        elements = ones(1 + len(ac_amplitudes))
        elements[0] = dc_amplitudes
        elements[1:] = ac_amplitudes

        return dc, ac, elements

    @property
    def stream(self):
        ac_stream = ""

        for i in range(len(self.__ac_elements)):
            ac_stream = "{}{}".format(ac_stream, self.__ac_elements[i].stream)

        return "{dc_stream}{ac_stream}{eob}".format(
            dc_stream=self.__dc.stream,
            ac_stream=ac_stream,
            eob=Block.eob
        )
