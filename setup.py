#!/usr/bin/env python3

import setuptools

setuptools.setup(
    entry_points={
        "console_scripts": [
            "boxgen = boxgen:main",
        ],

        "distutils.commands": [
            "twineupload = distutils_twine:twineupload",
        ],
    },
)
