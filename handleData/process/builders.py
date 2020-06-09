from functools import reduce
import numpy as np
from ..utils import find_population_by_chinese_name
def build_topk(k=15, compare=lambda x: x['values'][0]):
    def topk(data, context):
        data_sorted = sorted(data, key=compare, reverse = True)
        data_sorted = data_sorted[:k]
        topk_names = list(map(lambda x: x['name'], data_sorted))
        return list(filter(lambda x:x['name'] in topk_names, data)), context
    return topk

def build_sort(compare=lambda x: x['values'][0]):
    def sort(data, context):
        data_sorted = sorted(data, key=compare, reverse=True)
        return data_sorted, context
    return sort

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



# TBD: Multi-column values support
# TBD: Better support for records filtering
def build_filter_nan():
    def filter_nan(data, context):
        def filter_criterion(v):
            if isinstance(v, float) or isinstance(v, int):
                return not np.isnan(v)
            elif isinstance(v, list):
                return True
            else:
                return True
        records = context['records']
        filter_out = list(filter(lambda v: not filter_criterion(v['values'][0]), data))
        filter_in = list(filter(lambda v: filter_criterion(v['values'][0]), data))
        context['records'] = list(map(lambda x: x[1], filter(lambda item: filter_criterion(data[item[0]]['values'][0]), enumerate(records))))
        data = filter_in
        return data, context
    return filter_nan

        


def build_filter_records(f):
    def filter_records(records, context):
        # print(records)
        # for record in records:
            # if record['国家地区'] == "冰岛":
                # print(record)
        context_records = context['records']
        context['records'] = list(filter(f, context_records))
        return list(filter(f, records)), context
    return filter_records


def build_confirmed_condition(condition=10000):
    def confirmed_condition(records, context):
        return list(filter(lambda x: x[-1]["累计确诊"] > 10000, records)), context
    return confirmed_condition


def build_filter_weekly(period_start=-7, period_end=0):
    def filter_weekly(records, context):
        length = len(records)
        return list(map(lambda x: x[ len(x) + period_start: len(x) + period_end], records)), context
    return filter_weekly

# def build_filter_days(first_date):
#     def filter_days(records, context):
#         return list(filter(lambda x: x['日期'] > first_date), records), context
#     return 

def build_filter_seq(l):
    def filter_seq(records, context):
        filtered = {
            "x": records['x'][-l:],
            'y': list(map(lambda x:x[-l:], records['y']))
        }
        return filtered, context
    return filter_seq

def build_filter_seq(l):
    def filter_seq(records, context):
        filtered = {
            "x": records['x'][-l:],
            'y': list(map(lambda x:x[-l:], records['y']))
        }
        return filtered, context
    return filter_seq

# Used in region data
def build_filter_region(region):
    def filter_region(records, context):
        return list(filter(lambda x: x['地区']==region, records)), context
    return filter_region
def build_filter_stage(stage):
    def filter_stage(records, context):
        return list(filter(lambda x: x['阶段']==stage, records)), context
    return filter_stage

