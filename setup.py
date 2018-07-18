#!/usr/bin/env python3

import setuptools
from distutils_twine import UploadCommand

setuptools.setup(cmdclass={"release": UploadCommand})
