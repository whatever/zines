"""
Functions to help generate 16-page PDF documents, used for making small zines.
"""

from base64 import b64decode

import io
import PIL

from collections import namedtuple

import fitz

from .samples import page_image


WIDTH, HEIGHT = fitz.PaperSize("letter")


ZinePage = namedtuple("ZinePage", ["number", "image", "rotation"])

LEFT = 270

RIGHT = 90

SEQUENCE = [
    4, 5, 13, 12, 16, 9, 1, 8,
    6, 3, 11, 14, 10, 15, 7, 2,
]
"""
Sequence of pages according to the below layout:

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

PAGES = {
    i: ZinePage(
        num,
        page_image(num),
        (LEFT if i % 2 == 0 else RIGHT),
    )
    for i, num in enumerate(SEQUENCE)
}
"""Mapping between cell-position on page to actual page number"""


def strip_prefix(encoded):
    """Return base64 png image"""
    return encoded.replace(b"data:image/png;base64,", b"")

def url_to_bytes(url: bytes):
    """Return bytes url to decoded bytes array"""
    return b64decode(strip_prefix(url))


def data_url_to_image(url: str) -> PIL.Image:
    """Return PIL.Image from Data URL"""
    decoded = url_to_bytes(url)
    image = PIL.Image.open(io.BytesIO(decoded))
    image.load()
    return image


def generate_pages(images):
    """Return a list of zine-pages with images"""
    return {
        i: ZinePage(
            num,
            images[num-1],
            (LEFT if i % 2 == 0 else RIGHT),
        )
        for i, num in enumerate(SEQUENCE)
    }


def generate_pdf_doc(pages: list, debug=True):
    """Return a PIL.Image from a ZinePage"""

    assert \
        isinstance(pages, list) and len(pages) == 16, \
        "images must be a list of length 16"

    doc = fitz.open()

    for side in range(2):

        page = doc.newPage(width=WIDTH, height=HEIGHT)

        for j in range(4):
            for i in range(2):

                k = 8*side + 2*j + i

                zine = pages[k]

                if zine is None:
                    raise "This failed in a way that we did not expect."

                byte_arr = io.BytesIO()
                zine.image.save(byte_arr, format="PNG")

                rect = fitz.Rect(
                    i * WIDTH/2.0,
                    j * HEIGHT/4.0,

                    i * WIDTH/2.0 + WIDTH/2.0,
                    j * HEIGHT/4.0 + HEIGHT/4,
                )

                page.insert_image(rect, stream=byte_arr, rotate=zine.rotation)
                page.draw_rect(rect)

        if debug:
            if side == 0:
                page.insert_text((3*WIDTH//8, 3*HEIGHT//8), "2")
                page.draw_line(
                    (3*WIDTH//8, 3*HEIGHT//8),
                    (5*WIDTH//8, 3*HEIGHT//8),
                )

                page.insert_text((5*WIDTH//8, 5*HEIGHT//8), "3")
                page.draw_line(
                    (5*WIDTH//8, 5*HEIGHT//8),
                    (5*WIDTH//8, 7*HEIGHT//8),
                )

            elif side == 1:
                page.insert_text((3*WIDTH//8, 5*HEIGHT//8), "1")
                page.draw_line(
                    (5*WIDTH//8, 3*HEIGHT//8),
                    (5*WIDTH//8, 5*HEIGHT//8),
                )

    return doc
