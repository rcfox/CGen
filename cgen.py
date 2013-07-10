class Variable(object):
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self.value = value

class CodeBlock(object):
    def __init__(self, owner, text=None, variables=None):
        self.owner = owner
        self.indent = 0
        self.indent_string = '    '
        self.code = []
        if variables is None:
            self.variables = {}
        else:
            self.variables = dict(variables)
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

    def variable(self, name, type, value=None):
        statement = '%s %s' % (type, name)
        if value is not None:
            statement = '%s = %s' % (statement, value)
        self.variables[name] = Variable(name, type, value)
        self(statement)

    def set(self, name, value):
        statement = '%s = %s' % (name, value)
        if name in self.variables:
            self.variables[name] = value
        else:
            raise KeyError(name, 'variable not defined')
        self(statement)

class Function(CodeBlock):
    def __init__(self, owner, name, return_type, arguments, variables=None):
        CodeBlock.__init__(self, owner, variables=variables)
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        args = ', '.join(['%s %s' % a for a in arguments])
        self.prototype = '%s %s(%s)' % (return_type, name, args)

    def __enter__(self):
        self.code.append('%s {' % self.prototype)
        return CodeBlock.__enter__(self)

    def if_statement(self, condition):
        return IfStatement(self, condition, variables=self.variables)

    def while_statement(self, condition):
        return WhileStatement(self, condition, variables=self.variables)

    def for_statement(self, initial, condition, update):
        return ForStatement(self, initial, condition, update, variables=self.variables)

class IfStatement(CodeBlock):
    def __init__(self, owner, condition, variables=None):
        CodeBlock.__init__(self, owner, variables=variables)
        self.condition = condition

    def __enter__(self):
        self.code.append('if (%s) {' % self.condition)
        return CodeBlock.__enter__(self)

class WhileStatement(CodeBlock):
    def __init__(self, owner, condition, variables=None):
        CodeBlock.__init__(self, owner, variables=variables)
        self.condition = condition

    def __enter__(self):
        self.code.append('while (%s) {' % self.condition)
        return CodeBlock.__enter__(self)

class ForStatement(CodeBlock):
    def __init__(self, owner, initial, condition, update, variables=None):
        CodeBlock.__init__(self, owner, variables=variables)
        self.initial = initial
        self.condition = condition
        self.update = update

    def __enter__(self):
        self.code.append('for (%s; %s; %s) {' % (self.initial, self.condition, self.update))
        return CodeBlock.__enter__(self)

class SourceFile(CodeBlock):
    def __init__(self):
        CodeBlock.__init__(self, None)
        self.indent = -1

    def function(self, name, return_type, arguments):
        return Function(self, name, return_type, arguments, variables=self.variables)
