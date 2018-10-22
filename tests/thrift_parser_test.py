from ptcdt.thrift_parser import MappedAST
import utils

def test_parse():
    mapped = MappedAST.from_file(utils.test_resource_path("thrifts/thrift_test.thrift"))
    assert len(mapped.namespaces) == 17
    assert len(mapped.structs) == 23
    assert len(mapped.services) == 2
    assert len(mapped.enums) == 1
    assert len(mapped.typedefs) == 1
    assert len(mapped.consts) == 1

def test_parse_with_includes():
    mapped = MappedAST.from_file(utils.test_resource_path("thrifts/include_simple_main.thrift"))
    assert len(mapped.structs) == 1
    assert mapped.structs['Xtruct'] != None
    assert len(mapped.services) == 1
    assert len(mapped.services['ThriftTest'].functions) == 1
