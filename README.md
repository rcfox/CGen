CGen
====

C Code Generation from Python

This is nowhere near done. Here's what it might look like to use it:

Input:
    src = SourceFile()
    with src.function('main', Type('int'), [Variable('argc', Type('int')), Variable('argv', Type('char').pointer().pointer())]) as f:
        f.variable('foo', Type('int'), value=42)
        f.call('printf', [r'"foo %d\n"', 'foo'])
        f.return_statement(0)
        
Output:
    int main(int argc, char** argv) {
        int foo = 42;
        printf("foo %d\n", foo);
        return 0;
    }

