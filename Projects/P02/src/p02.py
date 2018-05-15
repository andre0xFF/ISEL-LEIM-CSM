import huffman
import numpy as np


def main():
    path = "../data/raw/iliad.txt"
    ascii_content = np.fromfile(path, np.uint8)
    huffman.encode(ascii_content)


if __name__ == "__main__":
    main()
