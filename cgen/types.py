import copy
from collections import deque

class Type(object):
    def __init__(self, name, const=False, static=False, volatile=False, restrict=False, register=False, pointer_level=0):
        self.name = name
        self.const = const
        self.static = static
        self.volatile = volatile
        self.restrict = restrict
        self.register = register
        self.pointer_level = pointer_level

    def pointer(self):
        p = copy.copy(self)
        p.pointer_level += 1
        return p

    def declaration(self):
        d = self.name
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
        d += '*' * self.pointer_level
        return d

class Struct(Type):
    def __init__(self, name, variables, **kwargs):
        super(self.__class__, self).__init__(name, kwargs)
        self.variables = variables
        self.name = 'struct %s' % self.name

    def definition(self):
        d = ['%s {' % self.name]
        for v in self.variables:
            d.append('    %s;' % v.definition())
        d.append('};')
        return '\n'.join(d)

    # TODO: Look over this older code
    # def function(self, name, return_type, arguments, include_self=True):
    #     func_name = '%s_%s' % (self.name, name)
    #     if include_self:
    #         arguments.insert(0, Variable('self', 'struct %s*' % self.name))
    #     func = Function(self, func_name, return_type, arguments, variables=self.variables)
    #     func.indent -= 1
    #     if name not in self.functions:
    #         self.functions[name] = func
    #         return func
    #     else:
    #         raise KeyError(name, 'function already exists')

class Variable(object):
    def __init__(self, name, type, value=None):
        self.name = name
        self.type = type
        self._value = deque([value])

    def definition(self):
        return '%s %s' % (self.type.declaration(), self.name)

    def output(self):
        statement = self.definition()
        if len(self._value) > 0 and self._value[0] is not None:
            statement = '%s = %s' % (statement, self._value.popleft())
        return statement

    def set(self, value):
        self._value.append(value)

    def value(self):
        return self._value.pop()
