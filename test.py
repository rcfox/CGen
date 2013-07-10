#!/usr/bin/env python
from cgen import *

src = SourceFile()
src.include('stdio.h', True)

with src.function('main', 'int', [('int', 'argc'), ('char**', 'argv')]) as main:
    with main.if_statement('1') as f1:
        f1('return 0')
    main('return 1')

print src
