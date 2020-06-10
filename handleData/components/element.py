from ..interface.component import Component
from ..interface.parameter import Parameter
from ..interface.dtype import FuncType, IntType, StrType
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



class AppendOthers(Component):
    parameters = {
        "f": Parameter(FuncType)
    }
    def run(self):
        build_append_others_func(**self.args)   
    
    def get_func(self):
        return build_append_others_func(self.args['f'])




def build_insert_average(average, f=None):
    def insert_average(data, context):
        db = context['db']
        records = context['records']
        global_record = context['global_record']
        if average == "counted":
            counted_obj = {}
            for key, value in records[0].items():
                if isinstance(value, float) or isinstance(value, int) :
                    counted_obj[key] = 0.
            counted_obj['人口'] = 0
            def f_count(acc, x):
                acc['人口'] += find_population_by_chinese_name(db, x['国家地区'])
                for key in acc.keys():
                    if key == "人口":
                        continue
                    acc[key] += x[key]
                return acc
            counted_obj = reduce(f_count, records, counted_obj)
            average_value = f(counted_obj)
            data.insert(0, {"name": "各国平均", "values": average_value})


            # TBD: Multi-column population average
        if average == "population":
            populations = map(lambda x: find_population_by_chinese_name(db, x['name']), data)
            weighted_values = map(lambda x: x['values'][0] * find_population_by_chinese_name(db, x['name']) , data )
            sum_population = sum(populations)
            sum_weighted = sum(weighted_values)
            data.insert(0, {"name": "各国平均", "values":[sum_weighted/sum_population]})
        if average == "global":
            if isinstance(global_record, dict):
                global_record['国家地区'] = "全球"
            else:
                pass 
            average_values = f(global_record)
            data.insert(0, {"name": "各国平均", "values": average_values})
        if average == "global_custom":
            data.insert(0, {"name": "各国平均", "values":[f(global_record)]})
        return data, context
    return insert_average

class InsertAverage(Component):
    parameters = {
        "average": Parameter(StrType),
        "f": Parameter(FuncType, None)
    }
    def get_func(self):
        return build_insert_average(self.args['average'], self.args['f'])


