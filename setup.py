from setuptools import setup

setup(
    name="zine",
    version="0.4.20",
    scripts=["bin/serve-zine"],
    install_requires=[
        "Pillow>=8.1.2",
        "PyMuPDF>=1.18.9",
    ],
)
