from ptcdt.converter import *
from ptcdt.thrift_parser import MappedAST
# from utils import test_resource_path dont do this, or else it gets executed as a test by pytest
import ptsd.ast
import pytest
import thriftpy
import utils

# struct Xtruct {
  # 1: string string_thing
  # 4: byte byte_thing
  # 9: i32 i32_thing
  # 11: i64 i64_thing
# }
class _Xtruct:
    def __init__(self, string_thing, byte_thing, i16_thing, i32_thing, i64_thing):
        self.string_thing = string_thing
        self.byte_thing = byte_thing
        self.i16_thing = i16_thing
        self.i32_thing = i32_thing
        self.i64_thing = i64_thing

@pytest.fixture
def mapped_ast():
    return MappedAST.from_file(utils.test_resource_path("thrifts/thrift_test.thrift"))

@pytest.fixture
def thriftpy_module():
    return thriftpy.load(utils.test_resource_path("thrifts/thrift_test.thrift"), 
            module_name="thrift_test_thrift")

@pytest.fixture
def converter(mapped_ast, thriftpy_module):
    return Converter(mapped_ast.structs, thriftpy_module)

def test_simple_to_dict(mapped_ast):
    xtruct = _Xtruct('string_thingy', 0, 16, 32, 64)
    converter = DictConverter(mapped_ast.structs)
    converted = converter.to_dict("Xtruct", xtruct)
    assert converted['string_thing'] == 'string_thingy'
    assert converted['byte_thing'] == 0
    assert converted['i16_thing'] == 16
    assert converted['i32_thing'] == 32
    assert converted['i64_thing'] == 64

def test_simple_from_dict(thriftpy_module):
    obj = ThriftpyConverter(thriftpy_module).to_thriftpy("Xtruct", 
            {"string_thing": "string_thingy", "byte_thing": 0, "i16_thing": 16, "i32_thing": 32, "i64_thing": 64})
    assert obj.string_thing == 'string_thingy'
    assert obj.byte_thing == 0
    assert obj.i16_thing == 16
    assert obj.i32_thing == 32
    assert obj.i64_thing == 64

def test_convert_to_basic_types(converter, mapped_ast):
    string_type = mapped_ast.structs['Xtruct'].fields[0].type # string_thing
    byte_type = mapped_ast.structs['Xtruct'].fields[1].type
    i16_type = mapped_ast.structs['Xtruct'].fields[2].type
    i32_type = mapped_ast.structs['Xtruct'].fields[3].type
    i64_type = mapped_ast.structs['Xtruct'].fields[4].type

    assert converter.from_thrift(string_type, "foo") == "foo"
    assert converter.from_thrift(i16_type, 16) == 16
    assert converter.from_thrift(i32_type, 32) == 32
    assert converter.from_thrift(i64_type, 64) == 64

def test_convert_from_basic_types(converter, mapped_ast):
    string_type = mapped_ast.structs['Xtruct'].fields[0].type # string_thing
    byte_type = mapped_ast.structs['Xtruct'].fields[1].type
    i16_type = mapped_ast.structs['Xtruct'].fields[2].type
    i32_type = mapped_ast.structs['Xtruct'].fields[3].type
    i64_type = mapped_ast.structs['Xtruct'].fields[4].type

    assert converter.to_thrift(string_type, "foo") == "foo"
    assert converter.to_thrift(i16_type, 16) == 16
    assert converter.to_thrift(i32_type, 32) == 32
    assert converter.to_thrift(i64_type, 64) == 64

def test_convert_from_thrift_complex(converter, mapped_ast):
    arg_type = mapped_ast.services["ThriftTest"].functions[6].arguments[0].type

    xtruct = _Xtruct('string_thingy', 0, 16, 32, 64)
    dictz = converter.from_thrift(arg_type, xtruct)

    assert dictz["string_thing"] == "string_thingy"
    assert dictz["i16_thing"] == 16
    assert dictz["i32_thing"] == 32
    assert dictz["i64_thing"] == 64


def test_convert_to_thrift_complex(converter, mapped_ast):
    arg_type = mapped_ast.services["ThriftTest"].functions[6].arguments[0].type
    dictz = {"string_thing": "string_thingy", "byte_thing": 0, 
            "i16_thing": 16, "i32_thing": 32, "i64_thing": 64}

    obj = converter.to_thrift(arg_type, dictz)

    assert obj.string_thing == 'string_thingy'
    assert obj.byte_thing == 0
    assert obj.i16_thing == 16
    assert obj.i32_thing == 32
    assert obj.i64_thing == 64


def test_convert_to_string(converter, mapped_ast):
    arg_type = mapped_ast.services["ThriftTest"].functions[1].arguments[0].type
    obj = converter.to_thrift(arg_type, 'string_thingy')
    assert obj == 'string_thingy'

