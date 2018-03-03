#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageOps

BASEWIDTH = 50

def resize(img):
    wpercent = ( BASEWIDTH / float(img.size[0]) )
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((BASEWIDTH,BASEWIDTH), Image.ANTIALIAS)

def binarize(img):
    return img.convert('L')

def load_image(filename):
    img = Image.open(filename)
    img = resize(img)
    img = binarize(img)
    data = np.copy(np.asarray(img))
    data[data<25] = 0
    return data

def calculate_dist(x1, x2):
    return np.average(x1 - x2)

def pixels_to_pil(pixels):
    return Image.fromarray(pixels)

def pil_to_pixels(img):
    return np.array(img)

def find_nearest_alignment(template, test):
    img = pixels_to_pil(test)
    res = []
    for degree in range(0, 360, 45):
        img_rot = img.rotate(degree)
        dist = calculate_dist(template, pil_to_pixels(img_rot))
        res.append( (degree, dist) )
    nearest = min(res, key = lambda t : t[1])
    return nearest

def main():
    template = load_image("data/template.jpeg")
    test = load_image("data/test.jpeg")
    alignment = find_nearest_alignment(template, test)
    img = pixels_to_pil(test)
    img_res = img.rotate(alignment[0])
    img_res.save("data/res.jpeg")


if __name__ == "__main__":
    main()

