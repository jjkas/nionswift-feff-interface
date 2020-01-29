# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os

setuptools.setup(
    name="nionswift-feff-interface",
    version="0.0.1",
    author="Nion Software",
    author_email="joshua.j.kas@gmail.com",
    description="Interface between feff atomic eels pacakage and nionswift-eels-analysis.",
    long_description=open("README.rst").read(),
    url="https://github.com/jjkas/nionswift-feff-interface",
    packages=["nion.feff-interface"],
    install_requires=["nionswift>=0.14.0"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="nion.feff-interface.test",
    python_requires='~=3.6',
)
