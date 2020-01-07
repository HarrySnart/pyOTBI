# coding: utf-8
# Harry Snart Jan 2020

import io
import os
import re
from setuptools import setup, find_packages
import sys

import pyOTBI

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
    py_modules=['pyOTBI'],
    install_requires=requires,
    classifiers=[
        "Development Status :: beta",
        "Intended Audience :: Developers",
		"Topic :: Oracle BI :: OTBI :: Analytics",
        "Programming Language :: Python :: 3.7",
    ]
)