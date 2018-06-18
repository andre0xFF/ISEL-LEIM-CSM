from cv2 import imread

from numpy import array, ndarray

from video import ycc
from video.encoders import FrameEncoder
from video.frames import YCbCrFrame

DATA_PATH = "../data"
RAW_DATA = "{}/raw".format(DATA_PATH)
INTERMEDIATE_DATA_PATH = "{}/intermediate".format(DATA_PATH)
PROCESSED_DATA_PATH = "{}/processed".format(DATA_PATH)


def main(folder: str, filenames: list):
    intra_frames = exercise_01(folder, filenames)
    inter_frames = exercise_02(folder, intra_frames)
    exercise_03(folder, intra_frames[0], inter_frames)


def exercise_01(folder: str, filenames: list) -> ndarray:
    intra_frames = array([YCbCrFrame] * len(filenames))

    for i in range(len(filenames)):
        path = "{0}/{1}/{2}".format(RAW_DATA, folder, filenames[i])
        image = imread(path)
        image = ycc.encode(image)
        intra_frames[i] = YCbCrFrame(image, i)

        path = "{0}/exercise_01/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, intra_frames[i].index)
        print("[EX1] Writing to {}".format(path))
        intra_frames[i].write(path, 100)

    return intra_frames


def exercise_02(folder: str, intra_frames: ndarray) -> ndarray:
    inter_frames = array([YCbCrFrame] * (len(intra_frames) - 1))

    for i in range(1, len(intra_frames)):
        j = i - 1
        inter_frames[j] = YCbCrFrame(intra_frames[i] - intra_frames[0], i)

        path = "{0}/exercise_02/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, inter_frames[j].index)
        print("[EX2] Writing to {}".format(path))
        inter_frames[j].write(path, 100)

    return inter_frames


def exercise_03(folder: str, intra_frame: YCbCrFrame, inter_frames: ndarray):
    for l in range(intra_frame.layers.shape[0]):
        intra_frame.layers[l].make_blocks()
        inter_frames[0].layers[l].make_blocks()

    encoder = FrameEncoder()

    predicted_frame, vectors, error_frame = encoder.encode(intra_frame, inter_frames[0])

    path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, predicted_frame.index)
    print("[EX3] Writing to {}".format(path))
    predicted_frame.write(path, 100)

    path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, error_frame.index)
    print("[EX3] Writing to {}".format(path))
    error_frame.write(path, 100)


    # reconstructed_frame = encoder.decode(error, frame_vectors)
    # path = "{0}/exercise_03/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, inter_frames[0].index)
    # reconstructed_frame.write(path, 100)


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
