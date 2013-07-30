import copy

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
    def __init__(self, name, variables, const=False, static=False, volatile=False, restrict=False, register=False, pointer_level=0):
        super(self.__class__, self).__init__(name, const=const, static=static, volatile=volatile,
                                             restrict=restrict, register=register, pointer_level=pointer_level)
        self.variables = variables
        self.name = 'struct %s' % self.name

    def definition(self):
        d = ['%s {' % self.name]
        for v in self.variables:
            d.append('    %s;' % v.definition())
        d.append('};')
        return '\n'.join(d)
