from .engine.lambda_engine import LambdaEngine
from .engine.component_engine import ComponentEngine
from .engine.dtype_engine import DTypeEngine
from ..interface.dtype import FuncType, StrType, IntType, FloatType
class Parser:
    def __init__(self, lambda_engine, component_engine, dtype_engine):
        self.component_engine = component_engine
        self.lambda_engine = lambda_engine
        self.dtype_engine = dtype_engine
    def parse_dtype(self, desc, parameter):
        if parameter.dtype == FuncType:
            return self.lambda_engine.parse(desc)
        else:
            return desc
    def parse_component(self, json_component):
        component_class = self.component_engine.parse(json_component['name'])
        args = {}

        for key, parameter in component_class.parameters.items():
            if key in json_component['args'].keys():
                value = json_component['args'][key]
                value = self.parse_dtype(value, parameter)
                value = parameter.dtype(value)
            else:
                value = parameter.default
            args[key] = value
        return component_class(**args).get_func()
    def parse_description(self, json_obj):
        operator = self.lambda_engine.parse(json_obj['operator'])
        preprocess = []
        postprocess = []
        for process_desc in json_obj['preprocess']:
            process_component = self.parse_component(process_desc)
            preprocess.append(process_component)

        for process_desc in json_obj['postprocess']:
            process_component = self.parse_component(process_desc)
            postprocess.append(process_component)
        parsed = {
            "id": json_obj['id'],
            "description": "Weekly confirmed data of each country",
            "process": "seq",
            "operator": operator,
            "preprocess": preprocess,
            "postprocess": postprocess
        }
        return parsed
    def parse_file(self, json_obj):
        descriptions = list(map(self.parse_description, json_obj['descriptions']))
        return {
            "name": json_obj['name'],
            "descriptions": descriptions
        }
    
    def jsonify_component_class(self, name, component_class):
        json_parameters = {}
        json_component_class = {}
        for key, parameter in component_class.parameters.items():
            json_parameters[key] = self.jsonify_parameter(key, parameter)
        json_component_class['parameters'] = json_parameters
        json_component_class['name'] = name
        return json_component_class

    def jsonify_parameter(self, name, parameter):
        json_obj = {
            "name": name,
            "dtype": self.dtype_engine.get_dtype_str(parameter.dtype),
            "default": parameter.default.value
        }
        return json_obj

    def jsonify_component_classes(self):
        json_component_classes = []
        for name, component_class in self.component_engine.get_component_classes():
            json_component_class = self.jsonify_component_class(name, component_class)
            json_component_classes.append(json_component_class)
        return json_component_classes


def get_parser():
    lambda_engine = LambdaEngine()
    component_engine = ComponentEngine()
    dtype_engine = DTypeEngine()
    parser = Parser(lambda_engine, component_engine, dtype_engine)
    return parser