from cv2 import imread
from time import clock

from jpeg import JPEG


def analyze(image: str, output_path: str):
    print("Reading image from file: {}".format(image))
    raw_image = imread(image)

    print("Encoding image with JPEG")
    t = clock()

    encoded_image = JPEG(image=raw_image)
    encoded_image.encode()

    elapsed_time = clock() - t
    print("Encoding time: {}".format(elapsed_time))

    print("Writing to file: {}".format(output_path))
    write_to_file(encoded_image.stream.regular, output_path)

    # print("Decoding stream")
    # t = clock()
    # decoded_image = JPEG.from_stream(encoded_image.stream)
    #
    # elapsed_time = clock() - t
    # print("Decoding time: {}".format(elapsed_time))


def write_to_file(stream: str, filename: str):
    with open(filename, "w") as file:
        file.write(stream)


if __name__ == "__main__":
    analyze(
        image="../data/raw/Lena.tif",
        output_path="../data/processed/Lena"
    )
