# coding: utf-8
# Harry Snart Jan 2020

import io
import os
import re
from setuptools import setup, find_packages
import sys

# check minimum supported Python version
if sys.version_info[:2] < (3, 6):
    raise Exception("Python 3.6 or higher is required.")

requires = [
	"requests",
	"bs4",
	"pandas",
	"base64",
	"io",
	"xmltodict",
	"re"
]

setup(
    name="pyOTBI",
    version="0.0.1-beta",
    description="Simple Python library to connect to Fusion OTBI",
    author="Harry Snart",
    author_email="harry.snart@oracle.com",
    packages=['pyOTBI'],
    install_requires=requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: Universal Permissive License (UPL)",
        "Programming Language :: Python :: 3.7",
    ]
)