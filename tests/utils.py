import os

def curr_dir():
    return os.path.dirname(os.path.abspath(__file__))

def test_resource_path(name):
    return curr_dir() + "/" + name
