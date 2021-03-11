#!/usr/bin/env python3


from zine import generate_pdf_doc, PAGES


if __name__ == "__main__":

    doc = generate_pdf_doc([
        PAGES.get(i)
        for i in range(16)
    ])

    doc.save("sample.pdf")

    doc.close()
