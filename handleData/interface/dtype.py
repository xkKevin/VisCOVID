import dateutil.parser

class DType:
    def __init__(self):
        pass

class FuncType(DType):
    def __init__(self, func):
        if isinstance(func, FuncType):
            self.value = func.value
        else:
            self.value = func
        if type(self.value) == str:
            self.value = eval(self.value)
        
class StrType(DType):
    def __init__(self, value):
        if isinstance(value, StrType):
            self.value = value.value
        else:
            self.value = value
    

class IntType(DType):
    def __init__(self, value):
        if isinstance(value, IntType):
            self.value = value.value
        else:
            self.value = value
    

class FloatType(DType):
    def __init__(self, value):
        if isinstance(value, FloatType):
            self.value = value.value
        else:
            self.value = value


class DateType(DType):
    def __init__(self, datestr):
        self.datestr = datestr
        self.value = dateutil.parser.parse(datestr)    