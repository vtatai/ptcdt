class DictConverter:
    def __init__(self, struct_defs):
        self.struct_defs = struct_defs
        
    def to_dict(self, struct_name, obj):
        struct_def = self.struct_defs[struct_name]
        return reduce(lambda acc, field: self._convert_field(acc, field, obj), struct_def.fields, {})

    def _convert_field(self, acc, field, obj):
        acc[field.name.value] = self._convert_field_value(field.name.value, field.type, obj)
        return acc

    def _convert_field_value(self, name, field_type, obj):
        return getattr(obj, name)
