import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="easystac",
    version="0.0.1",
    url="https://github.com/davemlz/easystac",
    license="MIT",
    author="David Montero Loaiza and Cesar Aybar Camacho",
    author_email="dml.mont@gmail.com",
    description="A Python package for simple STAC queries",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=["six", "stackstac", "termcolor"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
