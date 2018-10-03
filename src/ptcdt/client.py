import thriftpy
from thriftpy.rpc import make_client

# Client
# pingpong_thrift = thriftpy.load("pingpong.thrift", module_name="pingpong_thrift")
complex_param_thrift = thriftpy.load("../tests/complex_param.thrift", module_name="complex_param_thrift")

# pingpong_client = make_client(pingpong_thrift.PingPong, '127.0.0.1', 6000)
complex_param_client = make_client(complex_param_thrift.ThriftTest, '127.0.0.1', 6000)
# print(pingpong_client.ping())

xtruct = complex_param_thrift.Xtruct()
xtruct.string_thing = "xtruct.string_thing"

xtruct2 = complex_param_thrift.Xtruct2()
xtruct2.i32_thing = 32

print(complex_param_client.testNest(xtruct, xtruct2))
