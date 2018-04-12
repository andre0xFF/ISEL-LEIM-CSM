import cv2
import matplotlib.pyplot as plt
import numpy as np
import image_metrics as metrics


def main():
    path = "../resources/raw/lenac.tif"
    img = cv2.imread(path)
    ex1(img)
    ex2(img, path)
    img_gray = ex3(img, path)
    ex4(img_gray)
    ex5(img_gray)
    ex6(img_gray)
    ex7()
    ex8()
    ex9()


def ex1(img):
    print("(1)")
    print("Image dtype: {}".format(img.dtype))
    print("Image shape: {}\n".format(img.shape))

    # cv2.imshow("Original image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def ex2(img, path):
    path_80 = "../resources/processed/img_quality_80.jpg"
    path_10 = "../resources/processed/img_quality_10.jpg"

    cv2.imwrite(path_80, img, (cv2.IMWRITE_JPEG_QUALITY, 80))
    cv2.imwrite(path_10, img, (cv2.IMWRITE_JPEG_QUALITY, 10))

    img_80 = cv2.imread(path_80)
    img_100 = cv2.imread(path_10)

    compression_rate = metrics.compression_rate(path, path_80)[0]

    print("(2)")
    print("# JPEG Quality 80")
    print("Compression rate: {}".format(compression_rate))
    print("SNR: {}".format(metrics.snr_db(img, img_80)))
    print("PSNR: {}\n".format(metrics.psnr(img, img_80)))

    compression_rate = metrics.compression_rate(path, path_10)[0]

    print("# JPEG Quality 10")
    print("Compression rate: {}".format(compression_rate))
    print("SNR: {}".format(metrics.snr_db(img, img_100)))
    print("PSNR: {}\n".format(metrics.psnr(img, img_100)))


def ex3(img, path):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path_gray = "../resources/processed/img_gray.jpg"

    cv2.imwrite(path_gray, img_gray)

    compression_rate = metrics.compression_rate(path, path_gray)

    print("(3)")
    print("# Gray image")
    print("Compression rate: {}".format(compression_rate[0]))
    print("Original image size: {} bytes".format(compression_rate[1]))
    print("Gray image size: {} bytes".format(compression_rate[2]))

    return img_gray


def ex4(img):
    plt.hist(np.ravel(img), 256, [0, 256])
    plt.title("Exercise 4 histogram")
    plt.show()


def ex5(img):
    mask = 0b00000001
    path = "../resources/processed/img_shift_{}.jpg"

    for i in range(8):
        tmp = np.bitwise_and(img, mask)
        cv2.imwrite(path.format(i), tmp)
        mask = mask << 1


def ex6(img):
    path = "../resources/processed/img_most_significant_4.jpg"
    cv2.imwrite(path, np.bitwise_and(img, 0b11110000))


def ex7():
    size = 100
    # We need 8 bits to represent 255 and there are no negatives
    blank_img = np.ones(shape=(size, size, 3), dtype=np.uint8) * 255

    # cv2.fillPoly(blank_img, [(10, 10), (10, 100), (100, 10), (100, 100)], 0)
    #
    # step = 0.01
    #
    # for i in np.arange(0, np.pi / 4, step):
    #     points = np.array([(0, 0), (0, 0), (), ()])
    #     print(i)


def ex8():
    pass


def ex9():
    pass


if __name__ == "__main__":
    main()
