#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(name='portify',
      version="0.1",
      description='spotify playlist creater',
      packages=find_packages(exclude=['*.tests']),
      install_requires=[
          "fuzzywuzzy",
          "python-levenshtein",
          "praw",
          "simplejson",
          "requests",
      ],
)
