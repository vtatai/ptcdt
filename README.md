PTCDT
-----
This is a simple tool to enable Thrift contract-based testing. It enables one to spin up a Thrift server which mocks replies based on a JSON contract definition.

Still under development and DOES NOT WORK.

Development
-----------

To run tests just call:
```bash
export PYTHONTEST=src
pytest
```
I recomment using virtualenv + virtualenvwrapper for better env isolation.
