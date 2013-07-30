from cgen.blocks import *

def test_basic_function():
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        assert f.output() == \
'''
int main(int argc, char** argv) {
    int foo = 42;
}
'''.strip()
