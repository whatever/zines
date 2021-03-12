import random

import fitz

from PIL import Image, ImageDraw


WIDTH, HEIGHT = fitz.PaperSize("letter")


def page_image(num: int) -> Image:
    """Return a PIL.Image representing that page"""
    w = HEIGHT//4 * 1
    h = WIDTH//2 * 1

    print(f"w={w}, h={h}")

    col = "white"
    img = Image.new("RGB", (w, h), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((w//8, h//2), f"page={num}...Fuck this", (0, 0, 0))
    return img


def random_image(num: int) -> Image:
    s = 2
    w = HEIGHT//4 * s
    h = WIDTH//2 * s

    col = random.choice(["magenta", "gray", "yellow", "white"])
    img = Image.new("RGB", (w, h), color=col)
    draw = ImageDraw.Draw(img)
    draw.text((w//8, h//2), f"page={num}...Fuck this", (0, 0, 0))
    return img