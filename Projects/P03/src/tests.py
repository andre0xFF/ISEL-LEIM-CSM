from cv2 import IMWRITE_JPEG_QUALITY
from cv2 import imread
from cv2 import imwrite

import numpy as np

from jpeg import Block, AC, DC, entropic_coding, ycc
from jpeg import quantification


def test_quantification():
    block = Block(np.array([
        [1337, 56, -27, 18, 78, -60, 27, -27],
        [-38, -27, 13, 44, 32, -1, -24, -10],
        [-20, -17, 10, 33, 21, -6, -16, -9],
        [-10, -8, 9, 17, 9, -10, -13, 1],
        [-6, 1, 6, 4, -3, -7, -5, 5],
        [2, 3, 0, -3, -7, -4, 0, 3],
        [4, 4, -1, -2, -9, 0, 2, 4],
        [3, 1, 0, -4, -2, -1, 3, 1]
    ]))

    print("\n[INFO] Encoding")
    encoded = quantification.encode(block, 50)

    print("Encoded block: \n{}".format(encoded))

    print("\n[INFO] Decoding")
    decoded = quantification.decode(encoded, 50)

    print("Decoded block: \n{}".format(decoded))


def test_block():
    block_0 = Block(np.array([
        [80, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    block_1 = Block(np.array([
        [80, 2, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    block_2 = Block(np.array([
        [78, 1, 0, -1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]))

    print("\n[INFO] Encoding blocks")
    stream_0 = block_0.encode(None)
    stream_1 = block_1.encode(block_0)
    stream_2 = block_2.encode(block_1)

    print("Stream 0: {}".format(stream_0))
    print("Stream 1: {}".format(stream_1))
    print("Stream 2: {}".format(stream_2))

    stream_0.join(stream_1).join(stream_2)

    print("\n[INFO] Decoding streams")

    while stream_0.regular != "":
        print("Current stream: {}".format(stream_0))
        dc, ac, stream_0 = entropic_coding.decode(stream_0, Block.size * Block.size)

        print("Decoded DC: {}".format(dc))
        print("Decoded AC: {}".format(ac))

    print("\n[INFO] Decoding blocks")
    stream_0 = block_0.encode(None)

    block_0, stream_0 = Block.decode(None, stream_0)
    block_1, stream_1 = Block.decode(block_0, stream_1)
    block_2, stream_2 = Block.decode(block_1, stream_2)

    print("Decoded Block 0: \n{}".format(block_0))
    print("Decoded Block 1: \n{}".format(block_1))
    print("Decoded Block 2: \n{}".format(block_2))


def test_ac():
    print("\n[INFO] Generating DC and AC")
    dc = DC(-2)
    ac = AC(np.array([0, 0, 3]), np.array([1, 1, -1]))

    print("Original DC: {}".format(dc))
    print("Original AC: {}".format(ac))

    print("\n[INFO] Encoding DC and AC")
    stream = entropic_coding.encode(dc, ac)

    print("Encoded stream: {}".format(stream))

    print("\n[INFO] Decoding steam")
    dc, ac, stream = entropic_coding.decode(stream, Block.size * Block.size)

    print("Decoded DC: {}".format(dc))
    print("Decoded AC: {}".format(ac))
    print("Decoded stream: {}".format(stream))


def test_ycc():
    print("[INFO] Running YCrCb tests")
    raw_data = "../data/raw"
    filename = "Lena.tif"

    print("[INFO] Reading image ")
    image = imread("{0}/{1}".format(raw_data, filename))

    print("[INFO] Encoding")
    encoded_image = ycc.encode(image)

    print("[INFO] Writing and reading encoded image")
    processed_data = "../data/intermediate"
    filename = "Lena.ycc.jpg"

    imwrite("{0}/{1}".format(processed_data, filename), encoded_image, (IMWRITE_JPEG_QUALITY, 100))
    image = imread("{0}/{1}".format(processed_data, filename))

    print("[INFO] Decoding")
    decoded_image = ycc.decode(encoded_image)

    print("[INFO] Writing decoded image")
    filename = "Lena.ycc.raw.jpg"
    imwrite("{0}/{1}".format(processed_data, filename), decoded_image, (IMWRITE_JPEG_QUALITY, 100))


if __name__ == "__main__":
    test_ycc()
    test_ac()
    test_block()

