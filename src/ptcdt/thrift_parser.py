from ptsd.parser import Parser
import ptsd
import logging

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

def parse(filename):
    with open(filename) as fp:
        tree = Parser().parse(fp.read())
        logging.debug(tree.body)
        return MappedAST(tree.namespaces, _extract_map(tree.body, ptsd.ast.Service), 
                _extract_map(tree.body, ptsd.ast.Struct), _extract_map(tree.body, ptsd.ast.Exception_), 
                _extract_map(tree.body, ptsd.ast.Const), _extract_map(tree.body, ptsd.ast.Enum),
                _extract_map(tree.body, ptsd.ast.Typedef))

def _extract_map(body, cl):
    object_list = filter(lambda x: isinstance(x, cl), body)
    return dict([(obj.name.value, obj) for obj in object_list])

