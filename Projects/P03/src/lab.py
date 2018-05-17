import jpeg
import cv2
import numpy as np


def main(image: str):
    print("Reading image from file {}".format(image))
    raw_image = cv2.imread(image)
    encoded_image = jpeg.encode(raw_image)

    # TODO: Write encoded_image to file
    # TODO: Read previous file

    decoded_image = jpeg.decode(encoded_image)

    analyze(raw_image, decoded_image)

    # TODO: Write decoded_image to file


def analyze(raw_image: np.array, decoded_image: np.array):
    # TODO: Compare both images and calculate metrics
    pass


if __name__ == "__main__":
    main(
        image="../data/raw/Lena.tif"
    )
