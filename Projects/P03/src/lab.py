from cv2 import imread

from jpeg import JPEG


def main(image: str):
    print("Reading image from file {}".format(image))
    raw_image = imread(image)

    print("Encoding image with JPEG")
    image = JPEG(image=raw_image)
    image.encode()

    # TODO: Write encoded_image to file
    # TODO: Read previous file
    # TODO: Decode
    # TODO: Analytics
    # TODO: Write decoded to file


if __name__ == "__main__":
    main(
        image="../data/raw/Lena.tif"
    )
