class Set(object):
    def __init__(self, parent, variable, value):
        self.parent = parent
        self.variable = variable
        self.value = value

    def output(self):
        return '%s = %s' % (self.variable.name, self.value)

class Return(object):
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

    def output(self):
        if self.value is None:
            return 'return'
        else:
            return 'return %s' % self.value

class Call(object):
    def __init__(self, parent, function_name, arguments):
        self.parent = parent
        self.function_name = function_name
        self.arguments = arguments

    def output(self):
        return '%s(%s)' % (self.function_name, ', '.join(self.arguments))
