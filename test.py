#!/usr/bin/env python
from cgen import *

src = SourceFile()
src.include('stdio.h', True)

with src.function('main', 'int', [('int', 'argc'), ('char**', 'argv')]) as main:
    main.variable('bar', 'int', 3)
    with main.for_statement('a','b','c') as f1:
        f1.variable('foo', 'double')
        f1.set('bar', 5)
        f1('return 0')
    main('return 1')
    main.set('bar',3)

print src
