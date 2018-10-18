=====
PTCDT
=====

.. image:: https://travis-ci.com/vtatai/ptcdt.svg?branch=master
    :target: https://travis-ci.com/vtatai/ptcdt

PTCDT is a simple tool to enable Thrift contract/consumer-driven testing. It enables one to spin up a Thrift server which mocks replies based on a JSON contract definition.

Still under heavy development. Use it at your own risk. YMMV. If it doesn't work, fix it!

Usage
=====

Use pip:

.. code:: bash

    pip install ptcdt

then:

.. code:: bash

    ptcdt <CONFIG FILE>

The config file should have everything the server needs to run. For sample configurations check https://github.com/vtatai/ptcdt/tree/master/tests/configs

Development
===========

Install all development deps:

.. code:: bash

    pip install -e .[dev]

To run tests just call:

.. code:: bash

    export PYTHONTEST=src
    pytest
    pytest --pdb # Very handy

I recomment using virtualenv + virtualenvwrapper for better env isolation. Also recommend iPython for command line.


