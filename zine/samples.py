"""
Generate PIL.Image types from various parameters.
"""


import random

import fitz

from PIL import Image, ImageDraw


WIDTH, HEIGHT = fitz.PaperSize("letter")


def page_image(num: int) -> Image:
    """Return a PIL.Image representing that page"""
    width = HEIGHT//4 * 1
    height = WIDTH//2 * 1

    col = "white"
    img = Image.new("RGB", (width, height), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((width//8, height//2), f"page={num}...Fuck this", (0, 0, 0))
    return img


def random_image(num: int) -> Image:
    """Return a PIL.Image with random content"""

    scale = 2
    width = HEIGHT//4 * scale
    height = WIDTH//2 * scale

    col = random.choice(["magenta", "gray", "yellow", "white"])
    img = Image.new("RGB", (width, height), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((width//8, height//2), f"page={num}...Fuck this", (0, 0, 0))
    return img
