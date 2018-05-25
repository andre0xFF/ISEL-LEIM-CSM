from cv2 import imread, imwrite
from time import clock
from numpy import ndarray

from jpeg import JPEG


def process(image: ndarray):
    print("Encoding image with JPEG")
    t = clock()

    image = JPEG(image=image)
    image.encode()

    elapsed_time = clock() - t
    print("Encoding time: {}".format(elapsed_time))

    print("Decoding stream")
    t = clock()

    image.decode()

    elapsed_time = clock() - t
    print("Decoding time: {}".format(elapsed_time))

    return image


def write_to_file(stream: str, filename: str):
    with open(filename, "w") as file:
        file.write(stream)


if __name__ == "__main__":
    input_path = "../data/raw/Lena.tif"
    output_path = "../data/processed/Lena"

    print("Reading from file: {}".format(input_path))
    image = imread(input_path)
    jpeg_image = process(image=image[:, :, :])

    print("Writing to file: {}".format(output_path))
    write_to_file(jpeg_image.stream, output_path)
