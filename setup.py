# -------------------------------
# -*- coding: utf-8 -*-
# @Author：jianghan
# @Time：2020/12/7 19:12
# @File: setup.py
# Python版本：3.6.8
# -------------------------------


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyloghandlers",
    version="0.0.1",
    author="ugvibib",
    author_email="ugvibib@163.com",
    description="A python log handler packages with supported Multi-process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ugvibib/pyloghandlers.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)