import numpy as np


def get_dc_coefficient_table():
    # Table K3
    # Table for luminance DC coefficient differences
    k3 = dict()
    k3[0] = "00"
    k3[1] = "010"
    k3[2] = "011"
    k3[3] = "100"
    k3[4] = "101"
    k3[5] = "110"
    k3[6] = "1110"
    k3[7] = "11110"
    k3[8] = "111110"
    k3[9] = "1111110"
    k3[10] = "11111110"
    k3[11] = "111111110"

    return k3


def encode(previous_block: np.array, current_block: np.array) -> str:

    dct_current_value = current_block[0][0]
    k3 = get_dc_coefficient_table()

    signal_bit = '0'

    if previous_block is None:
        bit_repr = signal_bit + "{0:b}".format(dct_current_value)
        return k3[len(bit_repr)-1] + bit_repr

    dct_current_value = current_block[0][0] - previous_block[0][0]

    if dct_current_value < 0:
        signal_bit = '1'

    bit_repr = signal_bit + "{0:b}".format(np.abs(dct_current_value))

    return k3[len(bit_repr)-1] + bit_repr


def decode(bit_stream: str):

    k3 = get_dc_coefficient_table()

    bit_value = ''

    for i in range(len(bit_stream)):
        bit_value += bit_stream[i]
        for key, value in k3.items():
            if value == bit_value:
                bit_signal = bit_stream[i + 1]
                dc_value = int(bit_stream[i + 2: i + 2 + key], 2)
                dc_value = dc_value if bit_signal == '0' else -dc_value
                return dc_value, bit_stream[i + 2 + key: len(bit_stream)]

    return None


if __name__ == "__main__":

    bit_stream_test = '11110010100001110111'
    dc_val, ac_val = decode(bit_stream_test)
    print(dc_val)
    print("")
    print(ac_val)
