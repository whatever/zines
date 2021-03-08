#!/usr/bin/env python3


import argparse
import io

from collections import namedtuple

import fitz

from PIL import Image, ImageDraw


WIDTH, HEIGHT = fitz.PaperSize("A4")


def page_image(num):
    """Return a PIL.Image representing that page"""
    w = HEIGHT//4 * 1
    h = WIDTH//2 * 1
    col = "white"
    img = Image.new("RGB", (w, h), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((w//8, h//2), f"page={num}...Fuck this", (0, 0, 0))
    return img


ZinePage = namedtuple("ZinePage", ["number", "image", "rotation"])


"""
Front                   Back
+---------+---------+   +---------+---------+
| <- 4    |    5 -> |   | <- 2    |    7 -> |
|         |         |   |         |         |
+---------+---------+   +---------+---------+
| <- 13   |   12 -> |   | <- 15   |   10 -> |
|         |         |   |         |         |
+---------+---------+   +---------+---------+
| <- 16   |    9 -> |   | <- 14   |   11 -> |
|         |         |   |         |         |
+---------+---------+   +---------+---------+
| <- 1    |    8 -> |   | <- 3    |    6 -> |
|         |         |   |         |         |
+---------+---------+   +---------+---------+
"""

LEFT = 270
RIGHT = 90

SEQUENCE = [
    4, 5, 13, 12, 16, 9, 1, 8,
    2, 7, 15, 10, 14, 11, 3, 6, 
]

PAGES = {
    i: ZinePage(
        num,
        page_image(num),
        (LEFT if i % 2 == 0 else RIGHT),
    )
    for i, num in enumerate(SEQUENCE)
}


def generate_pdf_doc(pages):

    assert isinstance(pages, list) and len(pages) == 16, "images must be a list of length 16"

    doc = fitz.open()

    for s in range(2):

        page = doc.newPage(width=WIDTH, height=HEIGHT)

        for j in range(4):
            for i in range(2):
                x = i*WIDTH/2 + WIDTH/4
                y = j*HEIGHT/4 + HEIGHT/8

                k = 8*s + 2*j + i

                zine = pages[k]

                if zine is None:
                    raise "This failed in a way that we did not expect."

                byte_arr = io.BytesIO()
                zine.image.save(byte_arr, format="JPEG")

                rect = fitz.Rect(
                    i * WIDTH/2.0,
                    j * HEIGHT/4.0,

                    i * WIDTH/2.0 + WIDTH/2.0,
                    j * HEIGHT/4.0 + HEIGHT/4,
                )

                page.insert_image(rect, stream=byte_arr, rotate=zine.rotation)
                page.draw_rect(rect)
    return doc




if __name__ == "__main__":

    images = [PAGES.get(i) for i in range(16)]

    doc = generate_pdf_doc(images)

    doc.save("sample.pdf")

    doc.close()