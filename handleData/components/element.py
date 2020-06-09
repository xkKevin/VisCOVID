from ..interface.component import Component
from ..interface.parameter import Parameter
from ..interface.dtype import FuncType, IntType
from functools import reduce
import numpy as np
from ..utils import find_population_by_chinese_name
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

def build_filter_weekly(period_start=-7, period_end=0):
    def filter_weekly(records, context):
        length = len(records)
        return list(map(lambda x: x[ len(x) + period_start: len(x) + period_end], records)), context
    return filter_weekly

class AppendOthers(Component):
    parameters = {
        "f": Parameter(FuncType)
    }
    def run(self):
        build_append_others_func(**self.args)   
    
    def get_func(self):
        return build_append_others_func(self.args['f'])

class WeeklyFilter(Component):
    parameters = {
        "daysTo": Parameter(IntType)
    }
    def get_func(self):
        return build_filter_weekly(-self.args['daysTo'])




