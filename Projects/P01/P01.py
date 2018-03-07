import matplotlib.pyplot as plt
import numpy as np
import cv2
from lib import image_metrics as metrics


def main():
    img = cv2.imread('resources/lenac.tif')
    path = 'resources/lenac.tif'
    # ex1(img)
    ex2(img, path)
    ex3(img, path)
    ex4(img)
    ex5(img)
    ex6()
    ex7()
    ex8()
    ex9()


def ex1(img):
    cv2.imshow('Original image', img)

    print(img.dtype)
    print(img.shape)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ex2(img, path):
    path_80 = 'P01/resources/img_80.jpg'
    path_10 = 'P01/resources/img_10.jpg'

    cv2.imwrite(path_80, img, (cv2.IMWRITE_JPEG_QUALITY, 80))
    cv2.imwrite(path_10, img, (cv2.IMWRITE_JPEG_QUALITY, 10))

    img_80 = cv2.imread(path_80)
    img_100 = cv2.imread(path_10)

    compression_rate = metrics.compression_rate(path, path_80)[0]

    print('(2)')
    print('# JPEG Quality 80')
    print('Compression rate: {}'.format(compression_rate))
    print('SNR: {}'.format(metrics.snr_db(img, img_80)))
    print('PSNR: {}\n'.format(metrics.psnr(img, img_80)))

    compression_rate = metrics.compression_rate(path, path_10)[0]

    print('# JPEG Quality 10')
    print('Compression rate: {}'.format(compression_rate))
    print('SNR: {}'.format(metrics.snr_db(img, img_100)))
    print('PSNR: {}\n'.format(metrics.psnr(img, img_100)))


def ex3(img, path):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path_gray = 'P01/resources/img_gray.jpg'

    cv2.imwrite(path_gray, img_gray)

    compression_rate = metrics.compression_rate(path, path_gray)

    print('(3)')
    print('# Gray image')
    print('Compression rate: {}'.format(compression_rate[0]))
    print('Original image size: {} bytes'.format(compression_rate[1]))
    print('Gray image size: {} bytes'.format(compression_rate[2]))


def ex4(img):
    plt.hist(img.ravel(), 256, [0, 256])
    plt.title('Exercise 4 histogram')
    plt.show()


def ex5(img):
    y = img > 128
    cv2.imshow('BW', y * 1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ex6():
    pass


def ex7():
    pass


def ex8():
    pass


def ex9():
    pass


if __name__ == '__main__':
    main()
