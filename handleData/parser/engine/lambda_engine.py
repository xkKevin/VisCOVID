from inspect import getmembers, isfunction
from functools import reduce
from ...process import calculations
from ...process import operators
from .engine import Engine
class LambdaEngine(Engine):
    def __init__(self):
        super(Engine, self).__init__()
        self.index = {}
        self.load_module(calculations)
        self.load_module(operators)

    def load_module(self, module):
        functions_list = [o for o in getmembers(module) if isfunction(o[1])]
        self.add_to_index(functions_list)

    def parse(self, funcstr, functype = None):
        if not functype:
            functype = LambdaEngine.extract_functype(funcstr)
        if functype == "lambda":
            value = eval(funcstr)
        elif functype == "predefined":
            value = self.index[funcstr]
        else:
            value = None
        return value

    def extract_functype(funcstr):
        if funcstr.startswith("lambda") and ":" in funcstr:
            return "lambda"
        else:
            return "predefined"