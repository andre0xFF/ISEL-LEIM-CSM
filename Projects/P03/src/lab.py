import jpeg
import cv2
import numpy as np


def main(image: str):
    print("Reading image from file {}".format(image))
    raw_image = cv2.imread(image)
    raw_bit_stream = image_to_binary(raw_image)

    encoded_image = jpeg.encode(raw_image, 100)

    measure_rate(raw_bit_stream, encoded_image)

    # TODO: Write encoded_image to file
    # TODO: Read previous file

    decoded_image = jpeg.decode(encoded_image)

    analyze(raw_image, decoded_image)

    # TODO: Write decoded_image to file


def image_to_binary(image: np.array):
    bit_stream = ''
    for value in image:
        bit_stream += "{0:b}".format(value)

    return bit_stream


def measure_rate(original_stream, compressed_stream):
    size_original = len(original_stream)
    size_compressed = len(compressed_stream)
    print("Original Size: " + str(size_original/1000) + " Kb")
    print("Compressed Size: " + str(size_compressed/1000) + " Kb")
    print("Compression Rate: " + str(round( 1.* size_original / size_compressed, 2)))


def analyze(raw_image: np.array, decoded_image: np.array):
    # TODO: Compare both images and calculate metrics
    pass


if __name__ == "__main__":
    main(
        image="../data/raw/Lena.tif"
    )

