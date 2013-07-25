#!/usr/bin/env python
from cgen import *
from math import pi

src = SourceFile()
src.include('stdio.h', True)
src.include('stdlib.h', True)

with src.struct('foo') as struct:
    struct.variable('baz', 'int')
    struct.variable('qux', 'char*', const=True)
    with struct.function('new', 'struct %s*' % struct.name, [], include_self=False) as f:
        f.return_statement('NULL')
    with struct.function('test', struct.variables['baz'].type(), []) as f:
        f.return_statement('self->baz')
    with struct.function('test2', 'void', []) as f:
        f.call('printf', [r'"Foo!\n"'])

src.variable('foo', 'int', value=6, const=True)

with src.function('main', 'int', [Variable('argc', 'int'), Variable('argv', 'char**')]) as main:
    main.variable('blah', 'bar', register=True, const=True, volatile=True)
    main.variable('bar', 'int', 3, register=True)
    main.variable('asdf', main.type(), value='&main')
    with main.if_statement('bar == 3') as f1:
        with f1.for_statement(Variable('i', 'size_t', value=0), 'i < 10', 'i++') as f2:
            f2.variable('foo', 'double', pi)
            f2.set('bar', 123)
            f2.set('argc', f1.call('printf',[r'"Foo: %d %g\n"', 'bar', 'foo'], use_return=True))
    main.set('bar',8)
    main.set('bar',38)
    main.return_statement('bar')

print src
