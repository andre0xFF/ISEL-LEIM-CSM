from numpy import array
from cv2 import cvtColor
from cv2 import imread
from cv2 import imwrite
from cv2 import IMWRITE_JPEG_QUALITY
from cv2 import COLOR_BGR2YCrCb
from cv2 import COLOR_YCrCb2BGR


def encode(image: array) -> array:
    return cvtColor(image, COLOR_BGR2YCrCb)


def decode(image: array) -> array:
    return cvtColor(image, COLOR_YCrCb2BGR)


def _test():
    print("[INFO] Running YCrCb tests")
    raw_data = "../data/raw"
    filename = "Lena.tif"

    print("[INFO] Reading image ")
    image = imread("{0}/{1}".format(raw_data, filename))

    print("[INFO] Encoding")
    encoded_image = encode(image)

    print("[INFO] Writing and reading encoded image")
    processed_data = "../data/processed"
    filename = "Lena.ycc.jpg"

    imwrite("{0}/{1}".format(processed_data, filename), encoded_image, (IMWRITE_JPEG_QUALITY, 100))
    image = imread("{0}/{1}".format(processed_data, filename))

    print("[INFO] Decoding")
    decoded_image = decode(encoded_image)

    print("[INFO] Writing decoded image")
    filename = "Lena.ycc.raw.jpg"
    imwrite("{0}/{1}".format(processed_data, filename), decoded_image, (IMWRITE_JPEG_QUALITY, 100))


if __name__ == "__main__":
    _test()
