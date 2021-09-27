#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="english-dictionary",
    packages=find_packages(
        include=[
            "english_dictionary",
            "english_dictionary.*",
        ]
    ),
    url="https://github.com/king-phyte/english-dictionary",
    author="King Phyte",
    author_email="kofiasante1400@gmail.com",
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=["pytest", "pytest-mock"],
)
