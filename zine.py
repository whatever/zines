#!/usr/bin/env python3


import argparse
import io

from PIL import Image, ImageDraw
from collections import namedtuple

import fitz


WIDTH = 595
HEIGHT = 842


def page_image(zine):
    num = zine.number
    w = HEIGHT//4 * 1
    h = WIDTH//2 * 1
    col = "white"
    img = Image.new("RGB", (w, h), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((0//2, h//2), f"page={num}...Fuck this", (0, 0, 0))
    img.save("{:02d}.jpg".format(num))
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

PAGES = {
    0: ZinePage(4, LEFT),
    1: ZinePage(5, RIGHT),
    2: ZinePage(13, LEFT),
    3: ZinePage(12, RIGHT),
    4: ZinePage(16, LEFT),
    5: ZinePage(9, RIGHT),
    6: ZinePage(1, LEFT),
    7: ZinePage(8, RIGHT),

    8: ZinePage(2, LEFT),
    9: ZinePage(7, RIGHT),
    10: ZinePage(15, LEFT),
    11: ZinePage(10, RIGHT),
    12: ZinePage(14, LEFT),
    13: ZinePage(11, RIGHT),
    14: ZinePage(3, LEFT),
    15: ZinePage(6, RIGHT),
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
                # front.insert_text((x, y), f"({x}, {y}) @ {i} @ {j}")

        doc.save("sample.pdf")