import jpeg
import cv2
import numpy as np


def main(image: str):

    print("Reading image from file {}".format(image))
    raw_image = cv2.imread(image)
    raw_bit_stream = image_to_binary(raw_image)

    encoded_image = jpeg.encode(raw_image, 100)

    compression_rate(raw_bit_stream, encoded_image)

    write_to_file(encoded_image, 'encoded_' + image)
    encoded_bit_stream = read_from_file('encoded_' + image)

    decoded_image = jpeg.decode(encoded_bit_stream)

    comp_rate, snr_value = analyze(raw_image, raw_bit_stream, encoded_image, decoded_image)

    # TODO: Write decoded_image to file !!! Talvez não seja necessario fazer


def image_to_binary(image: np.array):

    bit_stream = ''
    for value in image:
        bit_stream += "{0:b}".format(value)

    return bit_stream


def write_to_file(bit_stream, file_name):

    file = open(file_name, 'w')
    file.write(bit_stream)
    file.close()


def read_from_file(file_name):

    with open(file_name, 'r') as file_obj:
        return file_obj.read().replace('\n', '')


def compression_rate(original_stream, compressed_stream):

    size_original = len(original_stream)
    size_compressed = len(compressed_stream)
    return round( 1.* size_original / size_compressed, 2)


def calculate_snr(original_image, compressed_image):

    noise = original_image - compressed_image
    original_image_power = np.sum(original_image ** 2.0) / len(original_image)
    noise_power = np.sum(noise ** 2.0) / len(noise)
    snr = 10 * np.log10(original_image_power / noise_power)
    return snr


def analyze(raw_image: np.array, raw_bit_stream: np.array, encoded_image: np.array, decoded_image: np.array):
    
    comp_rate = compression_rate(raw_bit_stream, encoded_image)
    snr_value = calculate_snr(raw_image, decoded_image)
    return comp_rate, snr_value


if __name__ == "__main__":
    main(
        image="../data/raw/Lena.tif"
    )
