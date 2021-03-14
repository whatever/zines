#!/usr/bin/env python3


import PIL
import os
import unittest


from io import BytesIO
from . import strip_prefix, url_to_bytes, data_url_to_image, generate_pages, generate_pdf_doc


class GenerateTest(unittest.TestCase):
    URLS_FILE = os.path.join(
        os.path.dirname(__file__),
        "urls.txt",
    )

    def test_data_image_to_url(self):

        with open(self.URLS_FILE, "r") as fi:
            decoded_images = [
                data_url_to_image(line.strip())
                for line in fi.readlines()
            ]


    def test_data_url_to_images(self):
        """Test whether we can generate a PDF from a list of data url's"""

        with open(self.URLS_FILE, "r") as fi:
            decoded_images = [
                url_to_bytes(line.strip())
                for line in fi.readlines()
            ]

        for line in decoded_images:
            self.assertFalse(line.startswith(b"data:image/png;base64,"))

        for decoded in decoded_images:
            buf = BytesIO(decoded)
            image = PIL.Image.open(buf)
            image.load()
            with open("file.png", "wb") as fi:
                fi.write(buf.getbuffer())

    def test_generate_pdf(self):

        with open(self.URLS_FILE, "r") as fi:
            images = [
                data_url_to_image(line.strip())
                for line in fi.readlines()
            ]

        pages = generate_pages(images)

        doc = generate_pdf_doc([
            pages.get(i)
            for i in range(16)
        ])

        doc.save("what.pdf")









if __name__ == "__main__":
    unittest.main()
