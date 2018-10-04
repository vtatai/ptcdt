from ptcdt.dict_converter import DictConverter
from ptcdt.thrift_parser import MappedAST
import utils

# struct Xtruct {
  # 1: string string_thing
  # 4: byte byte_thing
  # 9: i32 i32_thing
  # 11: i64 i64_thing
# }
class _Xtruct:
    def __init__(self, string_thing, byte_thing, i32_thing, i64_thing):
        self.string_thing = string_thing
        self.byte_thing = byte_thing
        self.i32_thing = i32_thing
        self.i64_thing = i64_thing

def test():
    xtruct = _Xtruct('string_thingy', 0, 32, 64)
    mapped_ast = MappedAST.from_file(utils.test_resource_path("thrifts/thrift_test.thrift"))
    converter = DictConverter(mapped_ast.structs)
    converted = converter.to_dict("Xtruct", xtruct)
    assert converted['string_thing'] == 'string_thingy'
    assert converted['byte_thing'] == 0
    assert converted['i32_thing'] == 32
    assert converted['i64_thing'] == 64

