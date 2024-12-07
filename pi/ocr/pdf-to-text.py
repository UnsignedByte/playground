#!/usr/bin/env python3
from pdf2image import convert_from_path
import pytesseract
import cv2
import argparse
import os
import numpy as np
import wand.image

def rotate_image(img: cv2.typing.MatLike, degrees: int) -> cv2.typing.MatLike:
    w = img.shape[1]
    h = img.shape[0]

    rot_mat = cv2.getRotationMatrix2D((w / 2, h / 2), degrees, 1.0)

    # Find the size of the new image
    cos = np.abs(rot_mat[0, 0])
    sin = np.abs(rot_mat[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # offset the rotation matrix to take into account the translation
    rot_mat[0, 2] += (new_w / 2) - w / 2
    rot_mat[1, 2] += (new_h / 2) - h / 2

    return cv2.warpAffine(img, rot_mat, (new_w, new_h))

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", required=True, help="name of the input file (located in data/)")
args.add_argument("-r", "--rotation", type=int, default=0, help="rotation of the pages")
args.add_argument("-d", "--dual", action="store_true", help="use dual pages")

args = args.parse_args()

# Convert the pdf to images
root = os.path.dirname(os.path.abspath(__file__))
pdf = convert_from_path(f"{root}/data/{args.input}.pdf")

i = 0
with open(f"{root}/data/{args.input}.txt", "w") as f:
    for page in pdf:
        # Convert the page to a numpy array
        page = np.array(page)
        # Reverse the width and height to match opencv's format
        img = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)

        # Rotate the image
        img = rotate_image(img, args.rotation)

        # Perform processing and thresholding
        # Scale up the image to help with OCR
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.resize(img, (img.shape[1] * 5, img.shape[0] * 5))
        # Denoise using adaptive thresholding
        # cv2.imwrite("test/processed.png", img)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 2)

        # If the image is dual, split it into two and operate on each half
        if args.dual:
            h = img.shape[0]
            w = img.shape[1]
            img1 = img[:, :w // 2]
            img2 = img[:, w // 2:]
            images = [img1, img2]
        else:
            images = [img]

        # Deskew the image
        for img in images:
            i+=1
            img = wand.image.Image.from_array(img)
            img.deskew(0.1)

            img = np.array(img)

            # Convert to text
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            text = pytesseract.image_to_string(img)
            f.write(f"\n{'-' * 50}\n{text}\n")