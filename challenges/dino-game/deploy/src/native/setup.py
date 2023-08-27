# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["native"]

package_data = {"": ["*"]}

install_requires = ["pybind11>=2.8.0,<3.0.0"]

setup_kwargs = {
    "name": "native",
    "version": "0.1.0",
    "description": "",
    "long_description": "None",
    "author": "Your Name",
    "author_email": "you@example.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "None",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
}
from build import *

build(setup_kwargs)

setup(**setup_kwargs)
