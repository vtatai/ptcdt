from ptcdt.contracts import *
from ptcdt.thrift_parser import *
from ptcdt.server import *
import ptcdt.matchers
import ptcdt.server
import pytest
import thriftpy
import utils

def test_delegate_no_params(thriftpy_test_module, thrift_test_ast):
    function_contracts = {"blahBlah": FunctionContract([ptcdt.matchers.build_function_call_single_exact_matcher([], None)])}
    service_contract = ServiceContract(function_contracts)

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(thrift_test_ast, thriftpy_test_module, service_contract, "SecondService"))
    Delegate().blahBlah()

def test_delegate_simple_param_return():
    filename = utils.test_resource_path("thrifts/echo.thrift")
    ast = MappedAST.from_file(filename)
    thriftpy_module = thriftpy.load(filename, module_name= "echo_thrift")

    function_contracts = {"echo": FunctionContract([ptcdt.matchers.build_function_call_single_exact_matcher(["hello"], "hello")])}
    service_contract = ServiceContract(function_contracts)

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(ast, thriftpy_module, service_contract, "Echo"))
    assert Delegate().echo("hello") == "hello"

def test_delegate_struct(thriftpy_test_module, thrift_test_ast, xtruct):
    contract_param = {
            "string_thing": xtruct.string_thing, 
            "byte_thing": xtruct.byte_thing,
            "i16_thing": xtruct.i16_thing,
            "i32_thing": xtruct.i32_thing,
            "i64_thing": xtruct.i64_thing
            }

    xtruct_return = _build_xtruct(thriftpy_test_module, "foo", 1, 2, 3, 4)
    contract_return = {
            "string_thing": xtruct_return.string_thing, 
            "byte_thing": xtruct_return.byte_thing,
            "i16_thing": xtruct_return.i16_thing,
            "i32_thing": xtruct_return.i32_thing,
            "i64_thing": xtruct_return.i64_thing
            }
    function_contracts = {"testStruct": FunctionContract([ptcdt.matchers.build_function_call_single_exact_matcher([contract_param], contract_return)])}
    service_contract = ServiceContract(function_contracts)

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(thrift_test_ast, thriftpy_test_module, service_contract, "ThriftTest"))
    assert Delegate().testStruct(xtruct) == xtruct_return

@pytest.fixture
def thriftpy_test_module():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    return thriftpy.load(filename, module_name= "thrift_test_thrift")

@pytest.fixture
def xtruct(thriftpy_test_module):
    return _build_xtruct(thriftpy_test_module, "string_thingy", 0, 16, 32, 64)

def _build_xtruct(thriftpy_test_module, string, byte, i16, i32, i64):
    xtruct = thriftpy_test_module.Xtruct()
    xtruct.string_thing = string
    xtruct.byte_thing = byte
    xtruct.i16_thing = i16
    xtruct.i32_thing = i32
    xtruct.i64_thing = i64
    return xtruct

@pytest.fixture
def thrift_test_ast():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    return MappedAST.from_file(filename)

