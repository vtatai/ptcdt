#!/usr/bin/env python
from setuptools import setup, find_packages


install_requires = [
        "ptsd==0.1.0",
        "thriftpy2==0.3.11",
        "click==7.0",
        "configparser==3.5.0"
        ]

dev_requires = [
        "cython>=0.28.5",
        "pytest>=3.8.2",
        "setuptools>=40.4.3",
        "ipython>=7.0.1",
        ]

setup (
    name='ptcdt',
    version="1.0",
    description='Tool for Thrift contract-consumer-driven testing',
    keywords="thrift python testing contract consumer",
    url="https://github.com/vtatai/ptcdt/",
    author='Victor Tatai',
    author_email='vtatai@gmail.com',
    license="Apache License, V.2",
    packages=find_packages(),
    python_requires='>=3.2.*',
    entry_points={
        'console_scripts': ['ptcdt = ptcdt.server.main']
    },
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        "dev": dev_requires,
        },
)
