from cgen.types import *

def test_variable():
    v = Variable('foo', Type('int'))
    assert v.definition() == 'int foo'

def test_static_variable():
    v = Variable('foo', Type('int', static=True))
    assert v.definition() == 'static int foo'

def test_variable_with_value():
    v = Variable('foo', Type('int'), value=42)
    assert v.code() == 'int foo = 42'

def test_variable_set_val():
    v = Variable('foo', Type('int'))
    v.set(42)
    v.set(4)
    v.set(13)
    assert v.value() == 13
    assert v.value() == 4
    assert v.value() == 42
    assert v.code() == 'int foo'

def test_variable_with_value_set_val():
    v = Variable('foo', Type('int'), value=500)
    v.set(42)
    v.set(4)
    v.set(13)
    assert v.value() == 13
    assert v.value() == 4
    assert v.value() == 42
    assert v.code() == 'int foo = 500'

def test_pointer_variable():
    v = Variable('foo', Type('int').pointer())
    assert v.code() == 'int* foo'

def test_struct_variable():
    v = Variable('foo', Struct('bar', []))
    assert v.code() == 'struct bar foo'
