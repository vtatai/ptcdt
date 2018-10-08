from ptcdt.contracts import *
from ptcdt.thrift_parser import *
from ptcdt.server import *
import ptcdt.matchers
import ptcdt.server
import thriftpy
import utils

def test_delegate_no_params():
    filename = utils.test_resource_path("thrifts/thrift_test.thrift")
    ast = MappedAST.from_file(filename)
    thriftpy_module = thriftpy.load(filename, module_name= "thrift_test_thrift")

    function_contracts = {"blahBlah": FunctionContract([ptcdt.matchers.build_function_call_single_exact_matcher([], None)])}
    service_contract = ServiceContract(function_contracts)

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(ast, thriftpy_module, service_contract, "SecondService"))
    Delegate().blahBlah()

def test_delegate_simple_param_return():
    filename = utils.test_resource_path("thrifts/echo.thrift")
    ast = MappedAST.from_file(filename)
    thriftpy_module = thriftpy.load(filename, module_name= "echo_thrift")

    function_contracts = {"echo": FunctionContract([ptcdt.matchers.build_function_call_single_exact_matcher(["hello"], "hello")])}
    service_contract = ServiceContract(function_contracts)

    Delegate = build_delegate(ptcdt.server._ServiceExecutionContext(ast, thriftpy_module, service_contract, "Echo"))
    assert Delegate().echo("hello") == "hello"

