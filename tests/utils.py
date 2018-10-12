import os

def curr_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_resource_path(name):
    return curr_dir() + "/" + name

def build_xtruct(thriftpy_test_module, string, byte, i16, i32, i64):
    xtruct = thriftpy_test_module.Xtruct()
    xtruct.string_thing = string
    xtruct.byte_thing = byte
    xtruct.i16_thing = i16
    xtruct.i32_thing = i32
    xtruct.i64_thing = i64
    return xtruct
