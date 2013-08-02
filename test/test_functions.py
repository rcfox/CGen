from cgen.blocks import *

def test_basic_function():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        f.return_statement(0)
        assert f.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
    return 0;
}
'''.strip()

def test_function_if():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        with f.if_statement('foo == 42') as ifs:
            ifs.return_statement(0)
        f.return_statement(1)
    assert src.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
    if (foo == 42) {
        return 0;
    }
    return 1;
}'''

def test_function_while():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        with f.while_statement('foo == 42') as ifs:
            ifs.set('foo', 43)
        f.return_statement(1)
    assert src.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
    while (foo == 42) {
        foo = 43;
    }
    return 1;
}'''

def test_function_for():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        with f.for_statement('foo = 0', 'foo < 10', '++foo') as ifs:
            pass
        f.return_statement(0)
    assert src.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
    for (foo = 0; foo < 10; ++foo) {
    }
    return 0;
}'''

def test_function_def_var():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        with f.for_statement(Variable('bar', Type('int'), value=0), 'bar < foo', '++bar') as ifs:
            pass
        f.return_statement(0)
    assert src.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
    for (int bar = 0; bar < foo; ++bar) {
    }
    return 0;
}'''

def test_function_call_function():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        f.call('printf', [r'"foo %d\n"', 'foo'])
        f.return_statement(0)
    assert src.output() == \
r'''
int main(int argc, char** argv) {
    int foo = 42;
    printf("foo %d\n", foo);
    return 0;
}'''
