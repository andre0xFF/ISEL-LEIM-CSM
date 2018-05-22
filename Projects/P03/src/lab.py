from cv2 import imread
from time import clock

from jpeg import JPEG


def analyze(image: str, output_path: str):
    print("Reading image from file {}".format(image))
    raw_image = imread(image)

    print("Encoding image with JPEG")
    encoded_image = JPEG(image=raw_image)

    t = clock()
    encoded_image.encode()

    elapsed_time = clock() - t
    print("Encoding time: {}".format(elapsed_time))

    print("Writing to file: {}".format(output_path))
    write_to_file(encoded_image.stream)

    print("Reading from file: {}".format(output_path))
    stream = read_from_file(output_path)

    print("Decoding stream")
    t = clock()
    decoded_image = JPEG.from_stream(stream)

    elapsed_time = clock() - t
    print("Decoding time: {}".format(elapsed_time))


# TODO: Write encoded_image to file
def write_to_file(stream: str):
    pass


# TODO: Read previous file
def read_from_file(filename: str):
    pass


if __name__ == "__main__":
    analyze(
        image="../data/raw/Lena.tif",
        output_path="../data/processed/Lena"
    )
