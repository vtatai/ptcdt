from ptsd.parser import Parser
import ptsd

class MappedAST:
    def __init__(self, namespaces=None, services=None, structs=None, exceptions=None, consts=None, enums=None, 
            typedefs=None):
        self.namespaces = namespaces if namespaces is not None else [] # Namespaces is a list since it can have repeat names
        self.services = services if services is not None else {}
        self.structs = structs if structs is not None else {}
        self.exceptions = exceptions if exceptions is not None else {}
        self.consts = consts if consts is not None else {}
        self.enums = enums if enums is not None else {}
        self.typedefs = typedefs if typedefs is not None else {}

    @classmethod
    def from_tree(cls, tree):
        return cls(tree.namespaces, cls._extract_map(tree.body, ptsd.ast.Service), 
                cls._extract_map(tree.body, ptsd.ast.Struct), cls._extract_map(tree.body, ptsd.ast.Exception_), 
                cls._extract_map(tree.body, ptsd.ast.Const), cls._extract_map(tree.body, ptsd.ast.Enum),
                cls._extract_map(tree.body, ptsd.ast.Typedef))

    @classmethod
    def _extract_map(cls, body, cl):
        object_list = filter(lambda x: isinstance(x, cl), body)
        return dict([(obj.name.value, obj) for obj in object_list])

    @classmethod
    def from_file(cls, filename):
        with open(filename) as fp:
            return cls.from_tree(Parser().parse(fp.read()))

