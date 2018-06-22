import time
from cv2 import imread
from numpy import array, ndarray
from src.video import ycc
from src.video.encoders import FrameEncoder
from src.video.frames import YCbCrFrame
from src.video import metrics as mesure


DATA_PATH = "../data"
RAW_DATA = "{}/raw".format(DATA_PATH)
INTERMEDIATE_DATA_PATH = "{}/intermediate".format(DATA_PATH)
PROCESSED_DATA_PATH = "{}/processed".format(DATA_PATH)


def millis():
    return time.time() * 1000


def main(folder: str, filenames: list):
    intra_frames, raw_paths = exercise_01(folder, filenames)
    inter_frames = exercise_02(raw_paths, folder, intra_frames)
    exercise_03(raw_paths, folder, intra_frames[0], inter_frames)


def exercise_01(folder: str, filenames: list):

    intra_frames = array([YCbCrFrame] * len(filenames))
    raw_paths = []
    for i in range(len(filenames)):
        raw_path = "{0}/{1}/{2}".format(RAW_DATA, folder, filenames[i])
        t0 = millis()
        original_image = imread(raw_path)
        image = ycc.encode(original_image)
        t1 = millis()
        intra_frames[i] = YCbCrFrame(image, i)

        raw_paths.append(raw_path)

        path = "{0}/exercise_01/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, intra_frames[i].index)
        print("[EX1] Writing to {}".format(path))
        intra_frames[i].write(path, 100)
        print("paths:::")
        print(raw_path)
        print(path)
        print("comp_rate:::")
        print(mesure.compression_rate(raw_path, path))
        print("SNR:::")
        print(mesure.psnr(original_image[:, :, 2], intra_frames[i].pixels[:, :, 2]))
        print("entropy:::")
        print(mesure.entropy(intra_frames[i].pixels.flatten()))
        print("energy:::")
        print(mesure.energy(intra_frames[i].pixels.flatten()))
        print("elapsed time:::")
        print(t1 - t0)
        print("")

    return intra_frames, raw_paths


def exercise_02(raw_paths: str, folder: str, intra_frames: ndarray) -> ndarray:
    inter_frames = array([YCbCrFrame] * (len(intra_frames) - 1))

    for i in range(1, len(intra_frames)):
        j = i - 1
        t0 = millis()
        inter_frames[j] = YCbCrFrame(intra_frames[i] - intra_frames[0], i)
        t1 = millis()
        path = "{0}/exercise_02/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, inter_frames[j].index)
        print("[EX2] Writing to {}".format(path))
        inter_frames[j].write(path, 100)
        print("paths:::")
        print(raw_paths[i-1])
        print(path)
        print("comp_rate:::")
        print(mesure.compression_rate(path, raw_paths[i-1]))
        print("SNR:::")
        print(mesure.psnr(intra_frames[i].pixels[:, :, 0],inter_frames[j].pixels[:, :, 0]))
        print("entropy:::")
        print(mesure.entropy(inter_frames[j].pixels.flatten()))
        print("energy:::")
        print(mesure.energy(inter_frames[j].pixels.flatten()))
        print("elapsed time:::")
        print(t1 - t0)
        print("")
    return inter_frames


def exercise_03(raw_paths: str, folder: str, intra_frame: YCbCrFrame, inter_frames: ndarray):

    for l in range(intra_frame.layers.shape[0]):
        intra_frame.layers[l].make_blocks()
        inter_frames[0].layers[l].make_blocks()

    enct0 = millis()
    encoder = FrameEncoder()
    enct1 = millis()

    predicted_frame, vectors, error_frame = encoder.encode(intra_frame, inter_frames[0])

    path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, predicted_frame.index)
    print("[EX3] Writing to {}".format(path))
    predicted_frame.write(path, 100)

    path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, error_frame.index)
    print("[EX3] Writing to {}".format(path))
    error_frame.write(path, 100)

    dect0 = millis()
    reconstructed_frame = encoder.decode(intra_frame, error_frame, vectors)
    dect1 = millis()

    path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, reconstructed_frame.index)
    print("[EX3] Writing to {}".format(path))
    reconstructed_frame.write(path, 100)
    print("paths:::")
    print(raw_paths[1])
    print(path)
    print("comp_rate:::")
    print(mesure.compression_rate(raw_paths[1], path))
    print("SNR:::")
    print(mesure.psnr(predicted_frame.pixels[:, :, 0], reconstructed_frame.pixels[:, :, 0]))
    print("entropy:::")
    print(mesure.entropy(reconstructed_frame.pixels.flatten()))
    print("energy:::")
    print(mesure.energy(reconstructed_frame.pixels.flatten()))
    print("encoding elapsed time:::")
    print(enct1 - enct0)
    print("decoding elapsed time:::")
    print(dect1 - dect0)
    print("")


if __name__ == "__main__":
    ball_folder = "bola_seq"

    ball_files = [
        "bola_1.tiff",
        "bola_2.tiff",
        "bola_3.tiff",
        "bola_4.tiff",
        "bola_5.tiff",
        "bola_6.tiff",
        "bola_7.tiff",
        "bola_8.tiff",
        "bola_9.tiff",
        "bola_10.tiff",
        "bola_11.tiff",
    ]

    car_path = "carro_seq"

    car_files = [
        "car1.bmp",
        "car2.bmp",
        "car3.bmp",
        "car4.bmp",
        "car5.bmp",
        "car6.bmp",
        "car7.bmp",
        "car8.bmp",
        "car9.bmp",
        "car10.bmp",
        "car11.bmp",
    ]

    main(ball_folder, ball_files)
