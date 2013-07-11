#!/usr/bin/env python
from cgen import *
from math import pi

src = SourceFile()
src.include('stdio.h', True)

with src.struct('foo', 'bar') as struct:
    struct.variable('baz', 'int')
    struct.variable('qux', 'char*', const=True)

src.variable('foo', 'int', value=6, const=True)

with src.function('main', 'int', [Variable('argc', 'int'), Variable('argv', 'char**')]) as main:
    main.variable('bar', 'int', 3, register=True)
    main.variable('asdf', main.type(), value='&main')
    with main.if_statement('bar == 3') as f1:
        with f1.for_statement(Variable('i', 'size_t', value=0), 'i < 10', 'i++') as f2:
            f2.variable('foo', 'double', pi)
            f2.set('argc', f1.call('printf',[r'"Foo: %d %g\n"', 'bar', 'foo'], use_return=True))
    main.set('bar',8)
    main.return_statement('bar')

print src
