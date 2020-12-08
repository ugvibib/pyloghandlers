# -------------------------------
# -*- coding: utf-8 -*-
# @Author：jianghan
# @Time：2020/12/7 19:12
# @File: setup.py
# Python版本：3.6.8
# -------------------------------

import io
import os
import setuptools

classifiers = """\

"""


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


package_keywords = 'logging pylog loghandlers'
base_dir = os.path.abspath(os.path.dirname(__file__))

info = {}
with io.open(os.path.join(
        base_dir, 'pyloghandlers', '__init__.py'), 'r', encoding='utf-8') as fh:
    exec(fh.read(), info)


setuptools.setup(
    name=info['__title__'],
    description=info['__description__'],
    version=info['__version__'],
    author=info['__author__'],
    author_email=info['__author_email__'],
    url=info['__url__'],
    license=info['__license__'],

    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=[
        'pyloghandlers'
    ],
    package_dir={
        'pyloghandlers': './pyloghandlers'
    },
    install_requires=[
        'portalocker>=2.0.0'
    ],
    classifiers=classifiers.splitlines(),
    keywords=package_keywords,
    zip_safe=True
)