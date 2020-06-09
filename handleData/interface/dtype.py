import dateutil.parser

class DType:
    def __init__(self):
        pass

class FuncType(DType):
    def __init__(self, funcstr, functype="lambda"):
        self.funcstr = funcstr
        self.functype = functype

class StrType(DType):
    def __init__(self, value):
        self.value = value
    

class IntType(DType):
    def __init__(self, value):
        self.value = value
    

class FloatType(DType):
    def __init__(self, value):
        self.value = value


class DateType(DType):
    def __init__(self, datestr):
        self.datestr = datestr
        self.value = dateutil.parser.parse(datestr)    