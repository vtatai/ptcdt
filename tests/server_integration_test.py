from thriftpy.rpc import make_client
from ptcdt.server import *
import logging
import pytest
import threading
import time
import utils

def test(thrift_server, thriftpy_test_module, request_xtruct):
    client = make_client(thriftpy_test_module.ThriftTest, '127.0.0.1', 6000)
    response = client.testStruct(request_xtruct)
    assert response == utils.build_xtruct(thriftpy_test_module, "string_thingy2", 1, 17, 33, 65)

@pytest.fixture
def thrift_server():
    thread = threading.Thread(name="thrift-server-thread", 
            target=_start_server, 
            daemon=True
            )
    thread.start()
    time.sleep(1)
    return thread

def _start_server():
    logging.info("Starting server for tests")
    serve(utils.test_resource_path("thrifts/thrift_test.thrift"), "ThriftTest", 
            utils.test_resource_path("contracts/simple.tpact"))

@pytest.fixture
def thriftpy_test_module():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    return thriftpy.load(filename, module_name= "thrift_test_thrift")

@pytest.fixture
def request_xtruct(thriftpy_test_module):
    return utils.build_xtruct(thriftpy_test_module, "string_thingy", 0, 16, 32, 64)
