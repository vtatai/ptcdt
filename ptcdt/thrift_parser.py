from functools import reduce
from ptsd.parser import Parser
import logging
import os.path
import ptsd

logger = logging.getLogger(__name__)

class MappedAST:
    def __init__(self, includes=None, namespaces=None, services=None, structs=None, exceptions=None, 
            consts=None, enums=None, typedefs=None):
        self.includes = includes if includes is not None else []
        self.namespaces = namespaces if namespaces is not None else [] # Namespaces is a list since it can have repeat names
        self.services = services if services is not None else {}
        self.structs = structs if structs is not None else {}
        self.exceptions = exceptions if exceptions is not None else {}
        self.consts = consts if consts is not None else {}
        self.enums = enums if enums is not None else {}
        self.typedefs = typedefs if typedefs is not None else {}

    @classmethod
    def merge(cls, left, right):
        return MappedAST(
                left.includes + right.includes,
                left.namespaces + right.namespaces,
                cls._merge(left.services, right.services),
                cls._merge(left.structs, right.structs),
                cls._merge(left.exceptions, right.exceptions),
                cls._merge(left.consts, right.consts),
                cls._merge(left.enums, right.enums),
                cls._merge(left.typedefs, right.typedefs))

    @classmethod
    def _merge(cls, left, right):
        merged = left.copy()
        merged.update(right)
        return merged

    @classmethod
    def from_tree(cls, tree):
        return cls(tree.includes, tree.namespaces, cls._extract_map(tree.body, ptsd.ast.Service), 
                cls._extract_map(tree.body, ptsd.ast.Struct), cls._extract_map(tree.body, ptsd.ast.Exception_), 
                cls._extract_map(tree.body, ptsd.ast.Const), cls._extract_map(tree.body, ptsd.ast.Enum),
                cls._extract_map(tree.body, ptsd.ast.Typedef))

    @classmethod
    def _extract_map(cls, body, cl):
        object_list = filter(lambda x: isinstance(x, cl), body)
        return dict([(obj.name.value, obj) for obj in object_list])

    @classmethod
    def from_file(cls, filename, parsed_files=[]):
        logger.debug(f"Parsing from file {filename} {parsed_files}")
        with open(filename) as fp:
            path = cls._path(fp.name)
            mapped_ast = cls.from_tree(Parser().parse(fp.read()))
        filtered = map(lambda fname: cls.from_file(path + "/" + fname, parsed_files.append(fname)), 
                filter(lambda fname: fname not in parsed_files, 
                    map(lambda include: include.path.value, mapped_ast.includes)))
        return reduce(lambda left, right: cls.merge(left, right), filtered, mapped_ast)

    @classmethod
    def _path(cls, file):
        return os.path.dirname(file)

