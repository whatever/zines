from setuptools import setup

setup(
    name="zine",
    version="0.0.1",
    scripts=[
        "bin/serve-zine",
        "bin/gen-zine",
    ],
    install_requires=[
        "Pillow>=8.1.2",
        "PyMuPDF>=1.18.9",
    ],
)
