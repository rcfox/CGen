class Variable(object):
    def __init__(self, name, type, value=None, const=False, static=False, volatile=False, restrict=False, register=False, extern=False):
        self.name = name
        self._type = type
        self.value = value
        self.const = const
        self.static = static
        self.volatile = volatile
        self.restrict = restrict
        self.register = register

    def type(self):
        d = self._type
        if self.const:
            d = '%s %s' % ('const', d)
        if self.volatile:
            d = '%s %s' % ('volatile', d)
        if self.restrict:
            d = '%s %s' % ('restrict', d)
        if self.static:
            d = '%s %s' % ('static', d)
        if self.register:
            d = '%s %s' % ('register', d)
        return d

    def definition(self):
        if '(*)' in self.type():
            d = self.type().replace('(*)', '(*%s)' % self.name, 1)
        else:
            d = '%s %s' % (self.type(), self.name)
        return d

    def __str__(self):
        statement = self.definition()
        if self.value is not None:
            statement = '%s = %s' % (statement, self.value)
        return statement

    def __repr__(self):
        return '<Variable: %s = %s>' % (self.name, self.value)

class CodeBlock(object):
    def __init__(self, parent, text=None, variables=None):
        self.parent = parent
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
        if self.parent is not None:
            self.indent = self.parent.indent + 1
        return self

    def __exit__(self, type, value, traceback):
        self.parent.code.append(self)

    def append(self, statement):
        self.code.append(statement)

    def __str__(self):
        indent = self.indent_string * self.indent
        sep = '\n' + indent
        string = '\n' + indent + sep.join(map(str, self.code))
        if self.indent > 0:
            indent_close = self.indent_string * (self.indent-1)
            string += '\n%s}' % indent_close
        return string

    def include(self, filename, system_header=False):
        if system_header:
            include_chars = ('<', '>')
        else:
            include_chars = ('"', '"')
        self.code.append('#include %s%s%s' % (include_chars[0], filename, include_chars[1]))

    def variable(self, name, type, value=None, const=False, static=False, volatile=False, restrict=False, register=False):
        var = Variable(name, type, value, const=const, static=static, volatile=volatile, restrict=restrict, register=register)
        self.variables[name] = var
        self.append(var)
        return var

class FunctionContextCodeBlock(CodeBlock):
    def if_statement(self, condition):
        return IfStatement(self, condition, variables=self.variables)

    def while_statement(self, condition):
        return WhileStatement(self, condition, variables=self.variables)

    def for_statement(self, initial, condition, update):
        variables = self.variables
        if type(initial) == Variable:
            if initial.value is None:
                raise ValueError('%s: must initialize variable in for loop' % initial.name)
            variables[initial.name] = initial
        return ForStatement(self, initial, condition, update, variables=variables)

    def set(self, name, value, override_check=False):
        statement = '%s = %s' % (name, value)
        if name in self.variables or override_check:
            self.variables[name] = value
        else:
            raise KeyError(name, 'variable not defined')
        self.append(statement)

    def call(self, function_name, arguments, use_return=False):
        statement = '%s(%s)' % (function_name, ', '.join(arguments))
        if not use_return:
            self.append(statement)
        else:
            return statement

    def return_statement(self, value=None):
        if value is None:
            self.append('return')
        else:
            self.append('return %s' % str(value))

class Function(FunctionContextCodeBlock):
    def __init__(self, parent, name, return_type, arguments, variables=None):
        CodeBlock.__init__(self, parent, variables=variables)
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        for a in arguments:
            self.variables[a.name] = a

    def prototype(self, arg_names=True):
        if arg_names:
            args = ', '.join([str(arg) for arg in self.arguments])
        else:
            args = ', '.join([arg.type for arg in self.arguments])
        return '%s %s(%s)' % (self.return_type, self.name, args)

    def type(self):
        return '%s (*)(%s)' % (self.return_type, ', '.join([arg.type() for arg in self.arguments]))

    def __str__(self):
        string = '%s {' % self.prototype()
        string += CodeBlock.__str__(self)
        return string

class IfStatement(FunctionContextCodeBlock):
    def __init__(self, parent, condition, variables=None):
        CodeBlock.__init__(self, parent, variables=variables)
        self.condition = condition

    def __str__(self):
        string = 'if (%s) {' % self.condition
        string += CodeBlock.__str__(self)
        return string

class WhileStatement(FunctionContextCodeBlock):
    def __init__(self, parent, condition, variables=None):
        CodeBlock.__init__(self, parent, variables=variables)
        self.condition = condition

    def __str__(self):
        string = 'while (%s) {' % self.condition
        string += CodeBlock.__str__(self)
        return string

class ForStatement(FunctionContextCodeBlock):
    def __init__(self, parent, initial, condition, update, variables=None):
        CodeBlock.__init__(self, parent, variables=variables)
        self.initial = initial
        self.condition = condition
        self.update = update

    def __str__(self):
        string = 'for (%s; %s; %s) {' % (self.initial, self.condition, self.update)
        string += CodeBlock.__str__(self)
        return string

class SourceFile(CodeBlock):
    def __init__(self):
        CodeBlock.__init__(self, None)
        self.functions = {}

    def function(self, name, return_type, arguments):
        func = Function(self, name, return_type, arguments, variables=self.variables)
        if name not in self.functions:
            self.functions[name] = func
            return func
        else:
            raise KeyError(name, 'function already exists')

    def variable(self, name, type, value=None, const=False, static=True, volatile=False, restrict=False, register=False):
        return CodeBlock.variable(self, name, type, const=const, value=value, static=static, volatile=volatile, restrict=restrict, register=register)        
