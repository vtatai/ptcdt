from ptsd.parser import Parser

with open('thrift_test.thrift') as fp:
    tree = Parser().parse(fp.read())
    print(tree.body)
