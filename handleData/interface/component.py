from .parameter import Parameter
from .dtype import FuncType
# class ParameterList(dict):
#     def __init__(self, obj):
#         self.parameters = obj
    
#     def get(self, name):


    
    

class NotImplementedException(Exception):
    def __init__(self):
        super(NotImplementedException).__init__(self)


class Component():
    parameters = {}
    def __init__(self, *args, **kwargs):
        i = 0
        _args = {}
        for key, parameter in self.parameters.items():
            if i == len(args):
                break
            _args[key] = args[i]
            i += 1
        for key, value in kwargs.items():
            _args[key] = value
        self.args = {}
        self.set_args(_args)
        
    def set_args(self, args):
        for key, parameter in self.parameters.items():
            if key in args.keys():
                value = args[key]
                value = parameter.dtype(value)
            else:
                value = parameter.default
            self.args[key] = value.value

    def run(self):
        raise NotImplementedException
    
        

class SortComponent(Component):
    parameters = {
        
    }
    def __init__(self):
        pass
    def run(self, data, context):
        data_sorted = sorted(data, key=compare, reverse=True)
        return data_sorted, context






def build_append_others_func(f):
    def append_others(data, context):
        global_record = context['global_record']
        acc = [0.] * len(data[0]['values'])
        def add_to_sum(acc, c):
            acc = list(map(lambda i: c['values'][i] + acc[i], range(len(list(acc)))))
            return acc
        sum_of_data = reduce(add_to_sum, data, acc)
        global_values = f(global_record)
        others = map(lambda i: global_values[i] - sum_of_data[i], range(len(global_values)))
        data.append( {"name": "其他", "values": list(others)})
        return data, context
    return append_others


class Interface:
    def __init__(self):
        self.a = Parameter()
    def convert(self):
        return None