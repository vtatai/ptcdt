import ptcdt.server

class _Identifier:
    def __init__(self, name):
        self.value = name

class _Field:
    def __init__(self, name):
        self.name = _Identifier(name)

class _Function:
    def __init__(self, arg_names):
        self.arguments = map((lambda name: _Field(name)), arg_names)

def test():
    fun = _Function(["param1"])
    function_delegate = ptcdt.server.FunctionDelegate(fun)
    args_map = function_delegate.convert_to_param_map(1)
    assert args_map["param1"] == 1
