from setuptools import setup, find_packages

setup (
    name='ptcdt',
    version="1.0",
    description='Tool for Thrift contract-driven testing',
    author='Victor Tatai',
    license="Apache License, V.2",
    packages=find_packages,
    entry_points={
        'console_scripts': ['tpcdd = tpcdd.tpcdd_cli:main']
    },
    setup_requires=["pytest-runner"],
    install_requires=['thriftpy', 'ptsd'],
    tests_requires=['pytest>=3.8.1', 'ipython'],
)

setup(**config)
