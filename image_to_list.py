from PIL import Image
from PIL import ImageOps

import numpy
import argparse


def image_to_list(filename):
    image = Image.open(filename)
    image = ImageOps.grayscale(image)
    array = numpy.asarray(image)

    # use array.tolist() to get gray scaled image as list of lists
    return array.tolist()
