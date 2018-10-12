from thriftpy.rpc import make_server

import logging
import ptcdt.converter
import ptcdt.thrift_parser
import thriftpy

# Serves the service defined inside filename, using service_name as the key, and contract
# as a dict containing request response mappings.
# Contract is a map from function name to another dict, this one containing the actual 
# request responses. If contract for a function is not provided, an exception will'
# be throw by that function if ever it is called.
def serve(filename, service_name, contract):
    # Loads both the AST and the thriftpy dynamically generated data
    ast = thrift_parser.MappedAST.from_file(filename)
    thriftpy_module = thriftpy.load(filename, module_name= service_name + "_thrift")

    # Builds the delegate class which will have all the methods to handle the requests
    # The delegate will have the methods dynamically added into them, which actually point
    # to methods in a new instance of FunctionDelegate objects
    Delegate = build_delegate(_ServiceExecutionContext(ast, thriftpy_module, contract, service_name))

    # Builds the server and starts serving requests
    server = make_server(getattr(thriftpy_module, service_name), Delegate(), '127.0.0.1', 6000)
    server.serve()

def build_delegate(service_execution_context):
    return type('Delegate', (), _build_delegate_dict(service_execution_context))

def _build_delegate_dict(service_execution_context):
    functions = service_execution_context.ast_service.functions
    # Creates a map from function name -> delegate method
    return dict(zip(
        map(lambda f: f.name.value, functions),
        map(lambda f: FunctionDelegate(service_execution_context, f.name.value).delegate_function, functions)))

class _ServiceExecutionContext:
    def __init__(self, ast, thriftpy_module, contract, service_name):
        self.ast = ast
        self.thriftpy_module = thriftpy_module
        self.contract = contract
        self.service_name = service_name
        self.ast_service = ast.services[service_name]
        self.ast_functions_map = dict(map(lambda f: (f.name.value, f), self.ast_service.functions))

class FunctionDelegate:
    def __init__(self, service_execution_context, method_name):
        self.service_execution_context = service_execution_context
        self.method_name = method_name
        self.converter = ptcdt.converter.Converter(service_execution_context.ast.structs, service_execution_context.thriftpy_module)

    def delegate_function(self, *args):
        # convert all params
        converted_params = self._convert_params(list(args))
        # check contract
        result = self.service_execution_context.contract.match(self.service_execution_context.service_name,
                self.method_name, converted_params)
        # convert return object
        return self._convert_result(self.service_execution_context.ast_functions_map[self.method_name].type, result)
    
    def _convert_params(self, args):
        param_thrift_types = list(map(lambda field: field.type, self.service_execution_context.ast_functions_map[self.method_name].arguments))
        type_arg_tuples = list(zip(param_thrift_types, args))
        return list(map((lambda tpl: self.converter.from_thrift(tpl[0], tpl[1])), type_arg_tuples))

    def _convert_result(self, ast_type, result):
        return self.converter.to_thrift(ast_type, result)

