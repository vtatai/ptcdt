#!/usr/bin/env python
from setuptools import setup, find_packages


install_requires = [
        "jsonschema==2.6.0",
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
        "setuptools-git-version",
        ]

# read README file, used by Pypi
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name='ptcdt',
    # version='0.0.3',
    version_format='0.0.3.dev{commitcount}',
    description='Tool for Thrift contract-consumer-driven testing',
    keywords="thrift python testing contract consumer",
    url="https://github.com/vtatai/ptcdt/",
    author='Victor Tatai',
    author_email='vtatai@gmail.com',
    license="Apache License, V.2",
    packages=find_packages(),
    python_requires='>=3.2.*',
    entry_points={
        'console_scripts': ['ptcdt=ptcdt.main:main']
    },
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        "dev": dev_requires,
        },
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True,
)
