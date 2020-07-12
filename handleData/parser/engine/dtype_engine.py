from ...interface.dtype import StrType, FuncType, IntType, FloatType
from .engine import Engine

class DTypeEngine(Engine):
    def __init__(self):
        self.index = {
            FuncType: "FuncType",
            IntType: "IntType",
            FloatType: "FloatType",
            StrType: "StrType"
        }

    def get_dtype_str(self, dtype_class):
        return self.index[dtype_class]