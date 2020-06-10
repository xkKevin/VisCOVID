from ... import components
from ...components import rearrange
from ...components import element
from ...components import filters
from ...interface.component import Component
from .engine import Engine
from inspect import getmembers, ismodule, isclass
from functools import reduce

class ComponentEngine(Engine):
    def __init__(self):
        super(Engine, self).__init__()
        self.index = {}
        self.load_components(components)

    def load_components(self, module):
        submodules = [o for o in getmembers(module) if ismodule(o[1])]
        for submodule in submodules:
            self.load_module(submodule[1])

    def load_module(self, module):
        classes = [o for o in getmembers(module) if isclass(o[1]) and issubclass(o[1], Component)]
        self.add_to_index(classes)

    def parse(self, componentstr):
        return self.index[componentstr]