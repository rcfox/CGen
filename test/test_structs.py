from cgen.types import *

def test_empty_struct_definition():
    t = Struct('foo', [])
    assert t.definition() == 'struct foo {\n};'

def test_empty_struct_declaration():
    t = Struct('foo', [])
    assert t.declaration() == 'struct foo'

def test_empty_const_struct_definition():
    t = Struct('foo', [], const=True)
    assert t.definition() == 'struct foo {\n};'

def test_empty_const_struct_declaration():
    t = Struct('foo', [], const=True)
    assert t.declaration() == 'const struct foo'

def test_basic_struct_definition():
    t = Struct('foo', [Variable('a', Type('int')),
                       Variable('b', Type('char').pointer())])
    assert t.definition() == \
'''
struct foo {
    int a;
    char* b;
};
'''.strip()
