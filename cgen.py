class CodeBlock(object):
    def __init__(self, owner, text=None):
        self.owner = owner
        self.indent = 0
        self.indent_string = '    '
        self.code = []
        if text is not None:
            self.code.append(text)

    def __enter__(self):
        if self.owner is not None:
            self.indent = self.owner.indent + 1
        return self

    def __exit__(self, type, value, traceback):
        indent = self.indent_string * self.indent
        self.code.append('%s}' % indent)
        self.owner.code.append(str(self))

    def __call__(self, statement):
        indent = self.indent_string * (self.indent + 1)
        self.code.append('%s%s;' % (indent, statement))

    def __str__(self):
        indent = self.indent_string * self.indent
        return '%s%s' % (indent, '\n'.join(self.code))

    def include(self, filename, system_header=False):
        if system_header:
            include_chars = ('<', '>')
        else:
            include_chars = ('"', '"')
        self.code.append('#include %s%s%s' % (include_chars[0], filename, include_chars[1]))

    def function(self, name, return_type, arguments):
        return Function(self, name, return_type, arguments)

    def if_statement(self, condition):
        return IfStatement(self, condition)

class Function(CodeBlock):
    def __init__(self, owner, name, return_type, arguments):
        CodeBlock.__init__(self, owner)
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        args = ', '.join(['%s %s' % a for a in arguments])
        self.prototype = '%s %s(%s)' % (return_type, name, args)

    def __enter__(self):
        self.code.append('%s {' % self.prototype)
        return CodeBlock.__enter__(self)

class IfStatement(CodeBlock):
    def __init__(self, owner, condition):
        CodeBlock.__init__(self, owner)
        self.condition = condition

    def __enter__(self):
        self.code.append('if (%s) {' % self.condition)
        return CodeBlock.__enter__(self)

class SourceFile(CodeBlock):
    def __init__(self):
        CodeBlock.__init__(self, None)
        self.indent = -1
