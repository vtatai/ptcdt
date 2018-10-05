import ptsd.ast

class Converter:
    def __init__(self, struct_ast_defs, thriftpy_module):
        self.dict_converter = DictConverter(struct_ast_defs)
        self.thriftpy_converter = ThriftpyConverter(thriftpy_module)

    def from_thrift(self, ast_type, value):
        if type(ast_type) in [ptsd.ast.String, ptsd.ast.I16, ptsd.ast.I32, ptsd.ast.I64]:
            return value
        elif ptsd.ast.Identifier == type(ast_type):
            return self.dict_converter.to_dict(ast_type.value, value)
        else:
            raise UnsupportedConversion

    def to_thrift(self, ast_type, value):
        if type(ast_type) in [ptsd.ast.String, ptsd.ast.I16, ptsd.ast.I32, ptsd.ast.I64]:
            return value
        elif ptsd.ast.Identifier == type(ast_type):
            return self.thriftpy_converter.to_thriftpy(ast_type.value, value)
        else:
            raise UnsupportedConversion

class UnsupportedConversion(Exception):
    pass

class DictConverter:
    def __init__(self, struct_ast_defs):
        self.struct_ast_defs = struct_ast_defs
        
    def to_dict(self, struct_name, obj):
        struct_def = self.struct_ast_defs[struct_name]
        return reduce(lambda acc, field: self._convert_field(acc, field, obj), struct_def.fields, {})

    def _convert_field(self, acc, field, obj):
        acc[field.name.value] = self._convert_field_value(field.name.value, field.type, obj)
        return acc

    def _convert_field_value(self, name, field_type, obj):
        # TODO implemented nested struct support
        return getattr(obj, name)

class ThriftpyConverter:
    # Thrift def is thriftpy definition, it is used to create the object that Thriftpy understands
    def __init__(self, thrift_def):
        self.thrift_def = thrift_def

    def to_thriftpy(self, struct_name, dictz):
        clazz = getattr(self.thrift_def, struct_name)
        obj = clazz()
        return reduce(self._reduce_field, dictz.items(), obj)

    def _reduce_field(self, obj, tple):
        # TODO implement nested struct support
        setattr(obj, tple[0], tple[1])
        return obj
