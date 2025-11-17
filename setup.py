#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="senior-care-plus-dataflow",
    version="1.0.0",
    author="Senior Care Plus Team",
    description="Apache Beam pipeline for IoT data transformation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "apache-beam[gcp]==2.53.0",
        "google-cloud-storage>=2.14.0",
        "google-cloud-bigquery>=3.14.1",
        "google-cloud-pubsub>=2.18.4",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
    ],
)

