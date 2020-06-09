from .engine.lambda_engine import LambdaEngine
from .engine.component_engine import ComponentEngine
from ..interface.dtype import FuncType
class Parser:
    def __init__(self, lambda_engine, component_engine):
        self.component_engine = component_engine
        self.lambda_engine = lambda_engine

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
        return component_class(args).get_func()
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
def get_parser():
    lambda_engine = LambdaEngine()
    component_engine = ComponentEngine()
    parser = Parser(lambda_engine, component_engine)
    return parser