from ptcdt.contracts import *
from ptcdt.thrift_parser import *
from ptcdt.server import *
import ptcdt.server
import pytest
import thriftpy
import utils

def test_delegate_no_params(thriftpy_test_module, thrift_test_ast):
    contract = Contract(Provider("provider"), Consumer("consumer"), [
        Interaction("provider state", "description", "SecondService", Request("blahBlah"), Response())])

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(thrift_test_ast, thriftpy_test_module, contract, "SecondService"))
    Delegate().blahBlah()

def test_delegate_simple_param_return():
    filename = utils.test_resource_path("thrifts/echo.thrift")
    ast = MappedAST.from_file(filename)
    thriftpy_module = thriftpy.load(filename, module_name= "echo_thrift")

    contract = Contract(Provider("provider"), Consumer("consumer"), [
        Interaction("provider state", "description", "Echo", Request("echo", ["hello"]), Response("hello"))])

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(ast, thriftpy_module, contract, "Echo"))
    assert Delegate().echo("hello") == "hello"

def test_delegate_struct(thriftpy_test_module, thrift_test_ast, xtruct):
    contract_param = {
            "string_thing": xtruct.string_thing, 
            "byte_thing": xtruct.byte_thing,
            "i16_thing": xtruct.i16_thing,
            "i32_thing": xtruct.i32_thing,
            "i64_thing": xtruct.i64_thing
            }

    xtruct_return = utils.build_xtruct(thriftpy_test_module, "foo", 1, 2, 3, 4)
    contract_return = {
            "string_thing": xtruct_return.string_thing, 
            "byte_thing": xtruct_return.byte_thing,
            "i16_thing": xtruct_return.i16_thing,
            "i32_thing": xtruct_return.i32_thing,
            "i64_thing": xtruct_return.i64_thing
            }

    contract = Contract(Provider("provider"), Consumer("consumer"), [
        Interaction("provider state", "description", "ThriftTest", Request("testStruct", [contract_param]), Response(contract_return))])
    
    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(thrift_test_ast, thriftpy_test_module, contract, "ThriftTest"))
    assert Delegate().testStruct(xtruct) == xtruct_return

@pytest.fixture
def thriftpy_test_module():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    return thriftpy.load(filename, module_name= "thrift_test_thrift")

@pytest.fixture
def xtruct(thriftpy_test_module):
    return utils.build_xtruct(thriftpy_test_module, "string_thingy", 0, 16, 32, 64)


@pytest.fixture
def thrift_test_ast():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    return MappedAST.from_file(filename)

