# from thriftpy.rpc import make_server

# from converter import DictConverter
# from thrift_parser import MappedAST

# import thriftpy
# import json
# import logging


# logging.basicConfig()

# # Server
# thrift_def = thriftpy.load("../tests/thrifts/complex_param.thrift", module_name="complex_param_thrift")
# mapped = MappedAST.from_file("../tests/thrifts/complex_param.thrift")
# dict_converter = DictConverter(mapped.structs)

# def testNest(self, *args):
    # # pass
    # # json.dumps(args[0])
    # print(dir(args[0]))
    # # print(args[0].thrift_spec)
    # # print(type(args[0].thrift_spec))
    # # print(args[0].default_spec)
    # # print(type(args[0].default_spec))
    # print(type(args[0].string_thing))
    # print(type(args[0].byte_thing))
    # print(type(args[0].i32_thing))
    # print(type(args[0].i64_thing))
    # print(dict_converter.to_dict("Xtruct", args[0]))


# Delegate = type('Delegate', (), dict(testNest=testNest))

# server = make_server(thrift_def.ThriftTest, Delegate(), '127.0.0.1', 6000)
# server.serve()

