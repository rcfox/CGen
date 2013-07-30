from cgen.types import Type

def test_basic_int():
    t = Type('int')
    assert t.declaration() == 'int'

def test_const_int():
    t = Type('int', const=True)
    tokens = t.declaration().split(' ')
    assert 'int' in tokens
    assert 'const' in tokens
    assert 'static' not in tokens
    assert tokens[-1] == 'int'

def test_static_const_int():
    t = Type('int', const=True, static=True)
    tokens = t.declaration().split(' ')
    assert 'int' in tokens
    assert 'const' in tokens
    assert 'static' in tokens
    assert tokens[-1] == 'int'

def test_int_pointer():
    t = Type('int').pointer()
    assert t.declaration() == 'int*'

def test_int_double_pointer():
    t = Type('int').pointer().pointer()
    assert t.declaration() == 'int**'
