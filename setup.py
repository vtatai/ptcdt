from setuptools import setup

config = {
    'name': 'tpcdd',
    'version': 1.0,
    'description': 'Tool for Thrift contract-driven testing',
    'author': 'Victor Tatai',
    'packages': ['tpcdd'],
    'entry_points': {
        'console_scripts': ['tpcdd = tpcdd.tpcdd_cli:main']
    },
    'install_requires': ['thriftpy'],
}

setup(**config)
