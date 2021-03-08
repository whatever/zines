#!/usr/bin/env python3


import argparse
import io

from PIL import Image, ImageDraw
from collections import namedtuple

import fitz


WIDTH, HEIGHT = fitz.PaperSize("A4")


def page_image(zine):
    num = zine.number
    w = HEIGHT//4 * 1
    h = WIDTH//2 * 1
    col = "white"
    img = Image.new("RGB", (w, h), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((w//8, h//2), f"page={num}...Fuck this", (0, 0, 0))
    return img


ZinePage = namedtuple("ZinePage", ["number", "rotation"])


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
        (LEFT if i % 2 == 0 else RIGHT),
    )
    for i, num in enumerate(SEQUENCE)
}


if __name__ == "__main__":

    with fitz.open() as doc:

        front = doc.newPage(width=WIDTH, height=HEIGHT)

        # First split
        front.draw_line((WIDTH/2, 0), (WIDTH/2, HEIGHT))

        # Across
        # front.draw_line((0, 1*HEIGHT/4), (WIDTH, 1*HEIGHT/4))
        # front.draw_line((0, 2*HEIGHT/4), (WIDTH, 2*HEIGHT/4))
        # front.draw_line((0, 3*HEIGHT/4), (WIDTH, 3*HEIGHT/4))

        for j in range(4):
            for i in range(2):
                x = i*WIDTH/2 + WIDTH/4
                y = j*HEIGHT/4 + HEIGHT/8

                zine = PAGES.get(2*j+i)

                # ...
                img = page_image(zine)
                byte_arr = io.BytesIO()
                img.save(byte_arr, format="JPEG")

                rect = fitz.Rect(
                    i * WIDTH/2.0,
                    j * HEIGHT/4.0,

                    i * WIDTH/2.0 + WIDTH/2.0,
                    j * HEIGHT/4.0 + HEIGHT/4,
                )

                front.insert_image(rect, stream=byte_arr, rotate=zine.rotation)
                front.draw_rect(rect)

        back = doc.newPage(width=WIDTH, height=HEIGHT)

        for j in range(4):
            for i in range(2):
                x = i*WIDTH/2 + WIDTH/4
                y = j*HEIGHT/4 + HEIGHT/8

                zine = PAGES.get(8 + 2*j+i)

                if zine is None:
                    raise "This failed in a way that we did not expect."

                # ...
                img = page_image(zine)
                byte_arr = io.BytesIO()
                img.save(byte_arr, format="JPEG")

                rect = fitz.Rect(
                    i * WIDTH/2.0,
                    j * HEIGHT/4.0,

                    i * WIDTH/2.0 + WIDTH/2.0,
                    j * HEIGHT/4.0 + HEIGHT/4,
                )

                back.insert_image(rect, stream=byte_arr, rotate=zine.rotation)
                back.draw_rect(rect)

        doc.save("sample.pdf")