import ptcdt.thrift_parser
import utils

def test_parse():
    treerep = ptcdt.thrift_parser.parse(utils.test_resource_path("thrift_test.thrift"))
    assert len(treerep.namespaces) == 17
    assert len(treerep.structs) == 23
    assert len(treerep.services) == 2
    assert len(treerep.enums) == 1
    assert len(treerep.typedefs) == 1
    assert len(treerep.consts) == 1
