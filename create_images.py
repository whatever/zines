#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

from zine import WIDTH, HEIGHT

if __name__ == "__main__":
    for i in range(16):
        num = i+1

        img = Image.new("RGB", (WIDTH, HEIGHT), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((WIDTH/2, HEIGHT/2), f"page={num}...Fuck this", (0, 0, 0))
        img.save("{:02d}.jpg".format(num))