import thriftpy
import json
import logging
from thriftpy.rpc import make_server

logging.basicConfig()

# Server
thrift_def = thriftpy.load("../tests/complex_param.thrift", module_name="complex_param_thrift")


def testNest(self, *args):
    # pass
    json.dumps(args[0])

Delegate = type('Delegate', (), dict(testNest=testNest))

server = make_server(thrift_def.ThriftTest, Delegate(), '127.0.0.1', 6000)
server.serve()

import thrift_parser
import logging

def serve(filename, service_name):
    parsed = thrift_parser.parse(filename)
    service = parsed.services[service_name]
    service.functions
    
class FunctionDelegate:
    def __init__(self, function):
        self.function = function

    def delegate_function(self, *args):
        pass

    def convert_to_param_map(self, *args):
        param_names = map((lambda identifier: identifier.name.value), self.function.arguments)
        param_names_params = zip(param_names, args)
        param_map = reduce(self._proc_tuple, param_names_params, {})
        logging.debug("Param map: " + str(param_map))
        return param_map
    
    def _proc_tuple(self, acc, tupl):
        acc[tupl[0]] = tupl[1]
        return acc
