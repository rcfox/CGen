from types import *
import statements

class CodeBlock(object):
    def __init__(self, parent, text=None, variables=None):
        self.parent = parent
        if parent is None:
            self.indent = 0
        else:
            self.indent = self.parent.indent + 1
        self.indent_string = '    '
        self.code = []
        if variables is None:
            self.variables = {}
        else:
            self.variables = dict(variables)
        if text is not None:
            self.code.append(text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.parent.code.append(self)

    def append(self, statement):
        self.code.append(statement)

    def output(self):
        indent = self.indent_string * self.indent
        sep = '\n' + indent
        string = ''
        if len(self.code) > 0:
            code_strings = ['']
            for c in self.code:
                if not isinstance(c, CodeBlock):
                    if type(c) == str and c.lstrip().startswith('#'):
                        code_strings.append(c)
                    else:
                        code_strings.append('%s;' % c.output())
                else:
                    code_strings.append(c.output())
            string = sep.join(code_strings)
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

    def variable(self, name, type, value=None):
        var = Variable(name, type, value)
        self.variables[name] = var
        self.append(var)
        return var

    def struct(self, name, variables=None):
        if variables is None:
            variables = []
        return Struct(name, variables, parent=self)

class FunctionContextCodeBlock(CodeBlock):
    def if_statement(self, condition):
        return If(self, condition, variables=self.variables)

    def while_statement(self, condition):
        return While(self, condition, variables=self.variables)

    def for_statement(self, initial, condition, update):
        variables = self.variables
        if type(initial) == Variable:
            if initial.value is None:
                raise ValueError('%s: must initialize variable in for loop' % initial.name)
            variables[initial.name] = initial
        return For(self, initial, condition, update, variables=variables)

    def set(self, name, value, override_check=False):
        if name in self.variables or override_check:
            self.append(statements.Set(self, self.variables[name], value))
        else:
            raise KeyError(name, 'variable not defined')

    def call(self, function_name, arguments):
        self.append(statements.Call(self, function_name, arguments))

    def return_statement(self, value=None):
        self.append(statements.Return(self, value))

class Function(FunctionContextCodeBlock):
    def __init__(self, parent, name, return_type, arguments, variables=None):
        super(self.__class__, self).__init__(parent, variables=variables)
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        for a in arguments:
            self.variables[a.name] = a

    def prototype(self, arg_names=True):
        if arg_names:
            args = ', '.join([arg.definition() for arg in self.arguments])
        else:
            args = ', '.join([arg.type for arg in self.arguments])
        return '%s %s(%s)' % (self.return_type.declaration(), self.name, args)

    def type(self):
        return '%s (*)(%s)' % (self.return_type, ', '.join([arg.type for arg in self.arguments]))

    def output(self):
        string = '%s {' % self.prototype()
        string += super(self.__class__, self).output()
        return string

class If(FunctionContextCodeBlock):
    def __init__(self, parent, condition, variables=None):
        super(self.__class__, self).__init__(parent, variables=variables)
        self.condition = condition

    def output(self):
        string = 'if (%s) {' % self.condition
        string += super(self.__class__, self).output()
        return string

class While(FunctionContextCodeBlock):
    def __init__(self, parent, condition, variables=None):
        super(self.__class__, self).__init__(parent, variables=variables)
        self.condition = condition

    def output(self):
        string = 'while (%s) {' % self.condition
        string += super(self.__class__, self).output()
        return string

class For(FunctionContextCodeBlock):
    def __init__(self, parent, initial, condition, update, variables=None):
        super(self.__class__, self).__init__(parent, variables=variables)
        self.initial = initial
        self.condition = condition
        self.update = update

    def output(self):
        if type(self.initial) == Variable:
            string = 'for (%s; %s; %s) {' % (self.initial.output(), self.condition, self.update)
        else:
            string = 'for (%s; %s; %s) {' % (self.initial, self.condition, self.update)
        string += super(self.__class__, self).output()
        return string

class SourceFile(CodeBlock):
    def __init__(self):
        super(self.__class__, self).__init__(None)
        self.functions = {}

    def function(self, name, return_type, arguments):
        func = Function(self, name, return_type, arguments, variables=self.variables)
        if name not in self.functions:
            self.functions[name] = func
            return func
        else:
            raise KeyError(name, 'function already exists')

    def variable(self, name, type, value=None, const=False, static=True, volatile=False, restrict=False, register=False):
        return super(self.__class__, self).variable(name, type, const=const, value=value, static=static, volatile=volatile, restrict=restrict, register=register)
