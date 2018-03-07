import matplotlib.pyplot as plt
import numpy as np
import cv2
from lib import image_metrics as metrics


def main():
    img = cv2.imread('resources/lenac.tif')
    # ex1(img)
    ex2(img)
    ex3()
    ex4()
    ex5()
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


def ex2(img):
    path1 = 'P01/resources/file1.jpg'
    path2 = 'P01/resources/file2.jpg'

    cv2.imwrite(path1, img, (cv2.IMWRITE_JPEG_QUALITY, 80))
    cv2.imwrite(path2, img, (cv2.IMWRITE_JPEG_QUALITY, 100))

    img_80 = cv2.imread(path1)
    img_100 = cv2.imread(path2)

    compression_rate = metrics.compression_rate('resources/lenac.tif', path1)

    print('# JPEG Quality 80')
    print('Compression rate: {}'.format(compression_rate))
    print('SNR: {}'.format(metrics.snr(img, img_80)))
    print('PSNR: {}\n'.format(metrics.psnr(img, img_80)))

    compression_rate = metrics.compression_rate('resources/lenac.tif', path2)

    print('# JPEG Quality 100')
    print('Compression rate: {}'.format(compression_rate))
    print('SNR: {}'.format(metrics.snr(img, img_100)))
    print('PSNR: {}\n'.format(metrics.psnr(img, img_100)))


def ex3():
    pass


def ex4():
    pass


def ex5():
    pass


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
