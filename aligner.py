#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import random

import sys

def random_file(path):
    return random.choice(glob.glob(path))


def convert_to_gray(img):
    print("Converting to grayscale...")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return cv2.bitwise_not(gray)

def binarize(img):
    print("Binarizing...")
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def calculate_bbox(img):
    print("Calculating bounding box based on white pixels...")
    coords = np.column_stack(np.where(img> 0))
    return cv2.minAreaRect(coords)

def draw_bbox(img, rect):
    print("Drawing bounding box over the image...")
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    img2 = img.copy()
    cv2.drawContours(img2, [box], 0, (255, 255, 255), 2)
    plot(img2)

def calculate_angle(rect):
    print("Calculating rotation angle...")
    angle = rect[-1]
    return -(90 + angle) if angle < -45 else -angle

def align(image, angle):
    print("Aligning image with angle=[{}]".format(angle))
    (h, w) = image.shape[:2]
    # rotation center
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def plot(img):
    if img.ndim > 2:
        plt.imshow(img)
    else:
        plt.imshow(img, 'gray')
    plt.show()

def main():
    args = sys.argv[1:]
    if not args:
        print("Please supply image path as an argument.\nUsage: python align.py <image_path>")
    # filename = "images/misaligned_images/test.jpg"
    # filename = random_file('images/*')
    filename = args[0].strip()
    filename = random_file('images/*') if filename == 'random' else filename
    print(filename)

    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plot(image)

    gray = convert_to_gray(image)
    plot(gray)

    thresh = binarize(gray)
    plot(thresh)

    rect = calculate_bbox(thresh)
    draw_bbox(thresh, rect)

    angle = calculate_angle(rect)
    print(angle)
    if -0.2 < angle < 0.2:
        print("Already aligned. Aborting...")
        return

    final = align(image, angle)
    cv2.imwrite('res.jpg', final)
    plot(final)

if __name__ == "__main__":
    main()

