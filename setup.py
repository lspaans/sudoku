# -*- coding: utf-8 -*-

"""Setup script for the "sudoku" project"""

from setuptools import setup

__author__ = "Léon Spaans"
__date__ = "2017-07-16"
__email__ = "leons{at}gridpoint[dot]nl"
__status__ = "Development"
__version__ = "0.1.0"

setup(
    name="sudoku",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=("A Python script for solving Sudokus"),
    keywords="sudoku solver",
    url="https://github.com/lspaans/sudoku.git",
    scripts=["solvesudoku"],
    packages=[
        "game",
        "setdict",
        "setmap",
        "sudoku"
    ],
    long_description=("For more information, please see \"README.rst\"."),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities"
    ],
    zip_safe=False
)
