from cv2 import imread
from numpy import array

from video import InterFrame
from video import IntraFrame
from video import FrameEncoder

DATA_PATH = "../data"
RAW_DATA = "{}/raw".format(DATA_PATH)
INTERMEDIATE_DATA_PATH = "{}/intermediate".format(DATA_PATH)
PROCESSED_DATA_PATH = "{}/processed".format(DATA_PATH)


def main(folder: str, filenames: list):
    intra_frames = exercise_01(folder, filenames)
    inter_frames = exercise_02(folder, intra_frames)
    exercise_03(intra_frames[0], inter_frames)


def exercise_01(folder: str, filenames: list) -> array:
    intra_frames = array([IntraFrame] * len(filenames))

    for i in range(len(filenames)):
        path = "{0}/{1}/{2}".format(RAW_DATA, folder, filenames[i])
        image = imread(path)
        intra_frames[i] = IntraFrame(image, i)

        path = "{0}/exercise_01/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, intra_frames[i])
        intra_frames[i].write(path, 100)

    return intra_frames


def exercise_02(folder: str, intra_frames: array) -> array:
    inter_frames = array([IntraFrame] * (len(intra_frames) - 1))

    for i in range(1, len(intra_frames)):
        j = i - 1
        inter_frames[j] = InterFrame(intra_frames[i], intra_frames[0], i)

        path = "{0}/exercise_02/{1}/{2}.jpg".format(PROCESSED_DATA_PATH, folder, inter_frames[j])
        inter_frames[j].write(path, 100)

    return inter_frames


def exercise_03(intra_frame: IntraFrame, inter_frames: array):
    encoder = FrameEncoder()

    encoder.encode(intra_frame, inter_frames[0])


if __name__ == "__main__":
    ball_path = "bola_seq"

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

    main(ball_path, ball_files)
