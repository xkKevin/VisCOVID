import os
import pandas as pd
from pymongo import MongoClient
from functools import reduce
import numpy as np
from handleData.utils import save_data, load_config, find_population_by_chinese_name, save_world_map, build_time_range
from datetime import datetime, timedelta
import dateutil.parser
from handleData.format import format_data
import csv
from handleData.report import build_report
import re
client = MongoClient()
db = client['coronavirus_analysis']

# 072798
# Global Sequence
# 全球累计增长曲线 confirmed_seq
# 全球累计死亡增长曲线 death_seq
# 全球确诊率增长曲线 confirmed_per_million
# 全球病死率 death_rate_seq = 累计死亡/累计确诊




def extract_global_seq(records):
    found = list(records.find())
    found.sort(key=lambda x: x['日期'])
    truncated = list(filter(lambda x: not np.isnan(x['累计确诊']), found))
    def generate_default_seq():
        return {'x': [], 'y': []}
    def f_death(acc, current):
        acc['x'].append(current['日期'])
        acc['y'].append(current['累计死亡'])
        return acc

    def f_confirmed(acc, current):
        acc['x'].append(current['日期'])
        acc['y'].append(current['累计确诊'])
        return acc

    def f_confirmed_per_million(acc, current):
        acc['x'].append(current['日期'])
        acc['y'].append(current['百万人口确诊率'])
        return acc

    def f_death_rate(acc, current):
        acc['x'].append(current['日期'])
        if current['累计确诊'] == 0.:
            acc['y'].append(0.)
        else:
            acc['y'].append(current['累计死亡']/current['累计确诊'])
        return acc

    def f_newly_confirmed_death(acc, current):
        acc['x'].append(current['日期'])
        acc['y'].append([current['新增确诊'], current['新增死亡']])
        return acc
     
    confirmed_seq = reduce(f_confirmed, truncated, generate_default_seq())
    death_seq = reduce(f_death, truncated, generate_default_seq())
    confirmed_per_million_seq = reduce(f_confirmed_per_million, truncated, generate_default_seq())
    death_rate_seq = reduce(f_death_rate, truncated, generate_default_seq())
    confirmed_death_seq = reduce(f_newly_confirmed_death, truncated, generate_default_seq())
    return {
        "global_confirmed_seq": confirmed_seq,
        "global_death_seq": death_seq,
        "global_confirmed_per_million_seq": confirmed_per_million_seq,
        "global_death_rate_seq": death_rate_seq,
        'global_confirmed_death_seq': confirmed_death_seq,
        # "global_newly_confirmed_seq": ,
        # "global_newly_death_seq":
    }



# Extract country data which is accessible from the newest data
# 国家确诊数据 confirmed_data
# 国家死亡数据 death_data



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

def build_append_others_func(f, global_record):
    def append_others(data, context):
        print(data)
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
            global_record['国家地区'] = "全球" 
            average_values = f(global_record)
            data.insert(0, {"name": "全球平均", "values": average_values})
        if average == "global_custom":
            data.insert(0, {"name": "全球平均", "values":[f(global_record)]})
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

        




def process_country_record_last_day(f, args=dict() , preprocess=[], postprocess=[]):

    # Query the MongoDB
    
        # Build the dataset table
    postprocess.insert(0, build_filter_nan())
    def build_final_data(db, config, with_others = True, top = -1, with_average=False, average=None, filter_country= lambda x: True, sorted=True, average_func=None):
        
        countries = db.selected_countries.find({})
        check_date = dateutil.parser.parse(config['time']['end'])
        check_date -= timedelta(days=1)
        global_record = db.global_records.find_one({"日期": check_date})
        found = list(map(lambda x: db.country_records.find_one({"国家地区": x['chinese'], "日期": check_date}), countries))
        # Pre-Processing
        context = {
            "records": found,
            "global_record": global_record
        }
        def process(acc, c):
            return c(acc, context)[0]
        mfound = reduce(process, preprocess, found)
        
        mfound = list(filter(filter_country, found))

        # Process on the records
        values = list(map(lambda x: {"name": x['国家地区'], "values": f(x)}, mfound))
        
        values = reduce(process, postprocess, values) 
        return values
        # Post-processing
        
        def filter_values(v):
            if isinstance(v, float) or isinstance(v, int):
                return not np.isnan(v)
            elif isinstance(v, list):
                return True
            else:
                return True
        
        filter_out = list(filter(lambda v: not filter_values(v['value']), values))
        filter_in = list(filter(lambda v: filter_values(v['value']), values))
        mfound = list(map(lambda x: x[1], filter(lambda item: filter_values(values[item[0]]['value']), enumerate(mfound))))
        values = filter_in
        


        
        if len(filter_out) > 0:
            print("Filter Out: ", filter_out)
        
        if sorted:
            values.sort(key=lambda x: x['value'], reverse=True)
        def f_sum(acc, c):
            if np.isnan(c['value']):
                return acc
            acc += c['value']
            return acc
        if top > 0:
            values = values[0: top] 
        if with_others:
            global_value = f(db.global_records.find_one({"日期": check_date}))
            sum_of_selected = reduce(f_sum, values, 0)
            values.append({"name": "其他", "value": global_value - sum_of_selected})
        if with_average:
            pass

        if average == "counted":
            counted_obj = {}
            for key, value in mfound[0].items():
                if isinstance(value, float) or isinstance(value, int) :
                    counted_obj[key] = 0.
            def f_count(acc, x):
                for key in acc.keys():
                    acc[key] += x[key]
                    # if np.isnan(x[key]):
                        # print(x)
                return acc
            counted_obj = reduce(f_count, mfound, counted_obj)
            average_value = f(counted_obj)
            values.insert(0, {"name": "各国平均", "value": average_value})
        if average == "population":
            populations = map(lambda x: find_population_by_chinese_name(db, x['name']), values)
            weighted_values = map(lambda x: x['value'] * find_population_by_chinese_name(db, x['name']) , values )
            sum_population = sum(populations)
            sum_weighted = sum(weighted_values)
            values.insert(0, {"name": "各国平均", "value":sum_weighted/sum_population})
        if average == "global":
            global_record = db.global_records.find_one({"日期": check_date})
            global_record['国家地区'] = "全球" 
            average_value = f(global_record)
            values.insert(0, {"name": "全球平均", "value":average_value})
        if average == "global_custom":
            global_record = db.global_records.find_one({"日期": check_date})
            values.insert(0, {"name": "全球平均", "value":average_func(global_record)})
        return values
    

    def build_combined_data(data1, data2, key1="key1", key2="key2",top = 5):
        data = map(lambda x: {'name': x['name'], key1: x['value']}, data1)
        def f(acc, c):
            def g(x):
                if c['name']==x['name']:
                    x[key2] = c['value']
                return x
            acc = map(g, acc)
            return acc
        data = reduce(f, data2, data)
        data = list(data)
        data.sort(key=lambda x: x[key1], reverse=True)
        data = data[:top]
        
        return list(data)


    def format_four_rates(four_rates):
        four_rates = map(lambda x: [x['name'], *x['value']], four_rates)
        t = pd.DataFrame(four_rates)
        t.columns = ['国家地区','检测率', '阳性率', '确诊率', '病死率']
        t = t.to_csv("./a.csv", encoding="utf_8_sig")
        return t

    return build_final_data

    

def extract_conutry_data(db, config):
    def calculate_test_rate(x):
        # return x['总检测数'] / float(find_population_by_chinese_name(db, x['国家地区']))
        return [x['百万人口检测率'] / 1000000]
    def calculate_confirmed_rate(x):
        # return x['累计确诊'] / float(find_population_by_chinese_name(db, x['国家地区']))
        return [x['百万人口确诊率'] / 1000000.]
    def calculate_death_rate(x):
        return [x['累计死亡']/x['累计确诊']]

    def calculate_positive_rate(x):
        return [x['累计确诊'] / x['总检测数']]

    def group_four_rates(x):
        return [calculate_test_rate(x), calculate_positive_rate(x), calculate_confirmed_rate(x), calculate_death_rate(x)]
    
    global_record = db.global_records.find_one({"日期": dateutil.parser.parse(config['time']['end']) - timedelta(days=1)})
    
    def extract_confirmed(record):
        return record['累计确诊']
    
    
    data_descriptions = [
        {
            "id": "confirmed_data",
            "description": "Confirmed data of each country",
            "process": "last_day",
            "operator": lambda x:  [x["累计确诊"]],
            "preprocess": [],
            "postprocess": [
                build_topk(),
                build_sort(),
                build_append_others_func(lambda x:  [x["累计确诊"]], global_record)
            ]
        },
        {
            "id": "death_data",
            "description": "Confirmed data of each country",
            "process": "last_day",
            "operator": lambda x:  [x["累计死亡"]],
            "preprocess": [],
            "postprocess": [
                build_topk(),
                build_sort(),
                build_append_others_func(lambda x:  [x["累计死亡"]], global_record)
            ]
        },
        {
            "id": "test_rate_data",
            "description": "Test rate data of each country",
            "process": "last_day",
            "operator": calculate_test_rate,
            "preprocess": [],
            "postprocess": [
                # build_topk(),
                build_sort(),
                build_insert_average("counted", lambda x: [x['总检测数']/ x['人口']])
            ]
        },
        {
            "id": "positive_rate_data",
            "description": "Positive rate data of each country",
            "process": "last_day",
            "operator": calculate_positive_rate,
            "preprocess": [],
            "postprocess": [
                # build_topk(),
                build_sort(),
                build_insert_average("counted", calculate_positive_rate)
            ]
        },
        {
            "id": "test_num_data",
            "description": "Test num data of each country",
            "process": "last_day",
            "operator": lambda x: [x['总检测数']],
            "preprocess": [],
            "postprocess": [
                # build_topk(),
                build_sort(),
                # build_insert_average("counted", calculate_positive_rate)
            ]
        },
        {
            "id": "confirmed_rate_data",
            "description": "Confirmed rate of each country",
            "process": "last_day",
            "operator": calculate_confirmed_rate,
            "preprocess": [],
            "postprocess": [
                # build_topk(),
                build_sort(),
                build_insert_average("global_custom", lambda g: g['百万人口确诊率']/1000000.)
            ]
        },
        {
            "id": "death_rate_data",
            "description": "Death rate of each country",
            "process": "last_day",
            "operator": calculate_death_rate,
            "preprocess": [],
            "postprocess": [
                # build_topk(),
                build_sort(),
                build_insert_average("global", calculate_death_rate)
            ]
        },
        
    ]
    
    def compile(description):
        return process_country_record_last_day( description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
    
    data = list(map(compile, data_descriptions))
    # confirmed_data = process_country_record_last_day(lambda x: [x["累计确诊"]], postprocess=[build_topk(), build_sort(), build_append_others_func(lambda x: [x["累计确诊"]], global_record)])(db, config)
    obj = {}
    for i in range(len(data)):
        obj[data_descriptions[i]['id']] = data[i]
    
    return obj
    # death_data = process_country_record_last_day(lambda x: x["累计死亡"], top=15)
    # newly_confirmed_data = process_country_record_last_day(lambda x: x['新增确诊'])
    # newly_death_data = process_country_record_last_day(lambda x: x['新增死亡'])
    
    
    # test_rate_data = process_country_record_last_day(calculate_test_rate, False, with_average=True, average="population", filter_country=lambda x: x['国家地区'] not in [])
    # positive_rate_data = process_country_record_last_day(calculate_positive_rate, False, with_average=True, average="counted",filter_country=lambda x: x['国家地区'] not in [])
    # confirmed_rate_data = process_country_record_last_day(calculate_confirmed_rate, False, average="global_custom", average_func=lambda g: g['百万人口确诊率']/1000000.)
    # death_rate_data = process_country_record_last_day(calculate_death_rate, False, average="global")
    # four_rates_data = process_country_record_last_day(group_four_rates, False, average=None, sorted=False) 
    # four_rates_data = process_country_record_last_day(four_rates_data)
    # top5_newly_confirmed_and_newly_death = (newly_confirmed_data, newly_death_data)
    # _confirmed_data = process_country_record_last_day(lambda x: x["累计确诊"], top=-1)
    # filter2000 = list(filter(lambda x: x['value']>20000, _confirmed_data))
    # t = map(lambda x: x['value'], filter2000)
    # t = sum(t)

    # test_num_data = (lambda x: x['总检测数'], False)


    # return {
    #     "confirmed_data": confirmed_data,
    #     "death_data": death_data,
    #     "newly_confirmed_data": newly_confirmed_data,
    #     "newly_death_data": newly_death_data,
    #     "test_rate_data": test_rate_data,
    #     "positive_rate_data": positive_rate_data,
    #     "confirmed_rate_data": confirmed_rate_data,
    #     "death_rate_data": death_rate_data,
    #     "test_num_data": test_num_data,
    # } 



# Extract country data which can not be accessible from the newest data

def extract_conutry_seq(db, config):
    countries = db.selected_countries.find({})
    check_date = dateutil.parser.parse(config['time']['end'])
    check_date -= timedelta(days=1)
    found = list(map(lambda x: list(db.country_records.find({"国家地区": x['chinese'], "日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}})), countries))

    def extract_weekly_global():
        global_records = list(db.global_records.find({"日期":{"$lte": check_date, "$gt": check_date - timedelta(days=7)}}))
        global_last_records = list(db.global_records.find({"日期":{"$lte": check_date - timedelta(days=7), "$gt": check_date - timedelta(days=14)}}))
        def build_sum_func(key):
            def f_global(acc, c):
                acc += c[key]
                return acc
            return f_global
        global_weekly_confirmed = reduce(build_sum_func("新增确诊"), global_records, 0)
        global_weekly_death = reduce(build_sum_func("新增死亡"), global_records, 0)
        global_last_weekly_confirmed = reduce(build_sum_func("新增确诊"), global_last_records, 0)
        global_last_weekly_death = reduce(build_sum_func("新增死亡"), global_last_records, 0)
        return global_weekly_confirmed, global_weekly_death, global_last_weekly_confirmed, global_last_weekly_death
    global_weekly_confirmed, global_weekly_death, global_last_weekly_confirmed, global_last_weekly_death = extract_weekly_global()

    def build_final_seq(f, with_others = False, period_start=-7, period_end=0, key="seq", top=-1, compare=lambda x: x['value'], sorted=False, post_filter=lambda x: True):
        seqs = list(map(lambda x: {"name": x[0]['国家地区'], key: f(x[len(x) + period_start:len(x) + period_end])}, found))
        seqs = list(filter(post_filter, seqs))
        if top > 0:
            seqs.sort(key=compare, reverse=True)
            seqs = seqs[0: top]
        if sorted:
            seqs.sort(key=compare, reverse=True)
        if with_others:
            def f_sum(acc, c):
                if np.isnan(compare(c)):
                    return acc
                acc += compare(c)
                return acc
            global_records = db.global_records.find({"日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}})
            global_records = list(global_records)
            t = list(global_records)[len(global_records) + period_start:len(global_records) + period_end]
            # print(t)
            global_value = f(t)
            sum_of_selected = reduce(f_sum, seqs, 0)
            seqs.append({"name": "其他", "value": global_value - sum_of_selected})
        return seqs
    def calculate_rate(a, b):
        if b == 0:
            return 0
        else:
            return a/b

    def build_combined_data(data1, data2, key1="key1", key2="key2",top = 5):
        data = map(lambda x: {'name': x['name'], key1: x['value']}, data1)
        def f(acc, c):
            def g(x):
                if c['name']==x['name']:
                    x[key2] = c['value']
                return x
            acc = map(g, acc)
            return acc
        data = reduce(f, data2, data)
        data = list(data)
        # data.sort(key=lambda x: x[key1], reverse=True)
        data = data[:top]
        
        return list(data)

    def build_growth_data(data1, data2, average=None, average_value = 0, filter_value=lambda x: True):
        data = map(lambda x: {'name': x['name'], "growth": x['value']}, data1)
        def f(acc, c):
            def g(x):
                if c['name']==x['name']:
                    # print(c['value'])
                    # print(x['growth'])
                    if x['growth'] == 0:
                        x['growth'] = 0
                    else:
                        x["growth"] = c['value']/x['growth'] - 1.
                return x
            # print("___________________________")
            # print(c)
            # acc = list(acc)
            # print(acc)
            acc = list(map(g, acc))
            # print(acc)
            return acc
        data = reduce(f, data2, data)
        data = list(data)
        data = list(filter(filter_value, data))

        data.sort(key=lambda x: x['growth'], reverse=True)
        
        if average == "global":
            data.insert(0, {'name': "全球平均", "growth": average_value})
        return list(data)
    
    def calculate_daily_growth(now_seq, last_seq):
        growth = map(lambda x:x, now_seq)
        def safe_divide(a,b):
            if b == 0:
                return 0
            else:
                return a/b
        def f(acc, c):
            def g(x):
                if x['name'] == c['name']:
                    x['seq'] = list(map(lambda i: safe_divide(x['seq'][i], c['seq'][i]) - 1, range(len(x['seq']))))
                return x
            acc = map(g, acc)
            return acc
        growth = reduce(f, last_seq, growth)
        return list(growth)

    newly_confirmed_seq = build_final_seq(lambda x: list(map(lambda y: y['新增确诊'], x)))
    last_newly_confirmed_seq = build_final_seq(lambda x: list(map(lambda y: y['新增确诊'], x)), period_start=-14, period_end=-7)
    

    newly_death_seq = build_final_seq(lambda x: list(map(lambda y: y['新增死亡'], x)))
    last_newly_death_seq = build_final_seq(lambda x: list(map(lambda y: y['新增死亡'], x)), period_start=-14, period_end=-7)
    
    newly_death_daily_growth_seq = calculate_daily_growth(newly_death_seq, last_newly_death_seq)
    newly_confirmed_daily_growth_seq = calculate_daily_growth(newly_confirmed_seq, last_newly_confirmed_seq)


    death_rate_seq = build_final_seq(lambda x: list(map(lambda y: calculate_rate(y['新增死亡'],y['新增确诊']), x)))
    test_rate_seq = build_final_seq(lambda x: list(map(lambda y: y['百万人口检测率']/1000000, x)),period_start=-45, period_end=0)
    confirmed_rate_seq = build_final_seq(lambda x: list(map(lambda y: calculate_rate(y['累计确诊'],float(find_population_by_chinese_name(db,y['国家地区']))), x)))
    weekly_confirmed_data = build_final_seq(lambda x: sum(y['新增确诊'] for y in x), key="value", top=15, with_others=True)
    weekly_death_data = build_final_seq(lambda x: sum(y['新增死亡'] for y in x),key="value", top=15, with_others=True)

    weekly_test_data = build_final_seq(lambda x: x[-1]['总检测数'], period_start=-8, key="value", sorted=True, post_filter=lambda x: not np.isnan(x['value']))
 
   
    
    def format_top5_combined(data):
        key1 = list(data[0].keys())[1]
        key2 = list(data[0].keys())[2]
        
        formatted = {
            "countries": [],
            key1: [],
            key2: []
        }
        def f(acc, c):
            acc["countries"].append(c['name'])
            acc[key1].append(c[key1])
            acc[key2].append(c[key2])
            return acc
        formatted = reduce(f, data, formatted)
        return formatted
    
    last_weekly_confirmed_data = build_final_seq(lambda x: sum(y['新增确诊'] for y in x), key="value", period_start=-14, period_end=-7)
    last_weekly_death_data = build_final_seq(lambda x: sum(y['新增死亡'] for y in x), key="value", period_start=-14, period_end=-7)
    

    _weekly_confirmed_data = build_final_seq(lambda x: sum(y['新增确诊'] for y in x), key="value", top=-1, with_others=True)
    _weekly_death_data = build_final_seq(lambda x: sum(y['新增死亡'] for y in x),key="value", top=-1, with_others=True)


    _last_weekly_confirmed_data = build_final_seq(lambda x: sum(y['新增确诊'] for y in x), key="value", period_start=-14, period_end=-7)
    _last_weekly_death_data = build_final_seq(lambda x: sum(y['新增死亡'] for y in x), key="value", period_start=-14, period_end=-7)
    weekly_top5_confirmed_and_death_data = build_combined_data(_weekly_confirmed_data, _weekly_death_data, key1="cases", key2="deaths")
    weekly_top5_confirmed_and_death_data = format_top5_combined(weekly_top5_confirmed_and_death_data)
    weekly_confirmed_growth = build_growth_data(_last_weekly_confirmed_data, _weekly_confirmed_data, average="global", average_value=global_weekly_confirmed/global_last_weekly_confirmed -1)
    weekly_death_growth = build_growth_data(_last_weekly_death_data, _weekly_death_data, average="global", average_value=global_weekly_death/global_last_weekly_death-1)



# Condition Total Cases > 10000
    country_total_confirmed = build_final_seq(lambda x: x[-1]['累计确诊'], key="value")
    condition_1_countries = list(map(lambda y: y['name'], filter( lambda x: x['value'] > 10000, country_total_confirmed)))
    weekly_confirmed_growth_condition_1 = build_growth_data(_last_weekly_confirmed_data, 
                            _weekly_confirmed_data, 
                            average="global", 
                            average_value=global_weekly_confirmed/global_last_weekly_confirmed-1,
                            filter_value=lambda x: x['name'] in condition_1_countries)
    weekly_death_growth_condition_1 = build_growth_data(_last_weekly_death_data, 
                            _weekly_death_data, 
                            average="global", 
                            average_value=global_weekly_death/global_last_weekly_death-1,
                            filter_value=lambda x: x['name'] in condition_1_countries)


    return {
        "newly_confirmed_seq": newly_confirmed_seq,
        "newly_death_seq": newly_death_seq,
        "death_rate_seq": death_rate_seq,
        'test_rate_seq': test_rate_seq,
        'confirmed_rate_seq': confirmed_rate_seq,
        "weekly_confirmed_data": weekly_confirmed_data,
        "weekly_death_data": weekly_death_data,
        "weekly_top5_confirmed_and_death_data": weekly_top5_confirmed_and_death_data,
        "weekly_confirmed_growth": weekly_confirmed_growth,
        "weekly_death_growth": weekly_death_growth,
        'newly_death_daily_growth_seq': newly_death_daily_growth_seq,
        'newly_confirmed_daily_growth_seq': newly_confirmed_daily_growth_seq,
        "weekly_confirmed_growth_condition_1": weekly_confirmed_growth_condition_1,
        "weekly_death_growth_condition_1": weekly_death_growth_condition_1,
        "weekly_test_data": weekly_test_data 
    }


def analyze_country(chinese, data,config):
    r = {
        "name": chinese
    }
    # r['x'] = build_time_range(config['time'])
    r['test_rate_seq'] = list(filter(lambda x: x['name']==chinese, data['test_rate_seq']))[0]['seq']
    r['death_rate_seq'] = list(filter(lambda x: x['name']==chinese, data['death_rate_seq']))[0]['seq']
    r['confirmed_rate_seq'] = list(filter(lambda x: x['name']==chinese, data['confirmed_rate_seq']))[0]['seq']
    r['newly_confirmed_daily_growth_seq'] = list(filter(lambda x: x['name']==chinese, data['newly_confirmed_daily_growth_seq']))[0]['seq']
    r['newly_death_daily_growth_seq'] = list(filter(lambda x: x['name']==chinese, data['newly_death_daily_growth_seq']))[0]['seq']
    return r




def build_name_conversion():
    data_country_name = ["United States","Democratic Republic of Congo", "The Islamic Republic of Mauritania", "Central African Republic","Somalia","Dominican Republic",
                    "刚果（布）", "格陵兰","South Sudan","赞比亚共和国","也门共和国","Burma"]
    map_country_name = ["United States","Dem. Rep. Congo", "Mauritania", "Central African Rep.","Somalia","Dominican Rep.","Congo", "Greenland","S. Sudan","Zambia", "Yemen","Myanmar"]
    country_name_conversion = {}
    def f(i):
        country_name_conversion[data_country_name[i]] = map_country_name[i]
    list(map(f, range(len(map_country_name))))
    def get_map_name(data_name):
        if data_name in country_name_conversion.keys():
            return country_name_conversion[data_name]
        else:
            return data_name
    return get_map_name


def extract_world_map_from_dxy(db, config):
    records = db.dxy.find()
    confirmed_data = list(map(lambda x: {"name": x['countryEnglishName'], "value": x['confirmedCount']}, records))
    death_data = list(map(lambda x: {"name": x['countryEnglishName'], "value": x['deathCount']}, records))
    return {
        "confirmed": confirmed_data,
        "death": death_data,
    }
def extract_world_map_from_owd(db, config):
    check_date = dateutil.parser.parse(config['time']['end']) - timedelta(days=2)
    regions = ['Africa', 'Asia', 'Asia excl. China', 'Europe', 'European Union', 'High income', 'Low income', 'Lower middle income', 'North America', 'Oceania', 'South America', 'Taiwan',  'Upper middle income', 'World']
    exclude_entities = ['International','World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore']
    exclude_entities.extend(regions)
    
    confirmed_records = list(db.owd_all.find({"date": check_date, "location": {"$nin": exclude_entities}}))
    death_records = list(db.owd_all.find({"date": check_date, "location": {"$nin": exclude_entities}}))
    
    get_map_name = build_name_conversion()
    
    conversion = {
            'United States Virgin Islands': 'U.S. Virgin Is.',
            'Northern Mariana Islands': 'N. Mariana Is.',
            'South Korea': 'Korea',
            'Czech Republic': 'Czech Rep.',
            'Cayman Islands': 'Cayman Is.',
            'Sao Tome and Principe': 'São Tomé and Principe',
            'Equatorial Guinea': 'Eq. Guinea',
            'Cote d\'Ivoire': 'Côte d\'Ivoire',
            'Falkland Islands': 'Falkland Is.',
            'Faeroe Islands': 'Faeroe Is.',
            # 'Cayman Is': 'Cayman Is.',
            'French Polynesia': 'Fr. Polynesia',
            'Bosnia and Herzegovina': 'Bosnia and Herz.',
            'Antigua and Barbuda': 'Antigua and Barb.',
            'Saint Vincent and the Grenadines': 'St. Vin. and Gren.',
            'Turks and Caicos Islands': 'Turks and Caicos Is.',
            "Curacao": "Curaçao",
            "Laos": "Lao PDR",
            'Timor': 'Timor-Leste',
            "Western Sahara": "W. Sahara"
        }
    def convert_name(name):
        if name in conversion.keys():
            return conversion[name]
        else:
            return name

    confirmed_data = list(map(lambda x: {"name": convert_name(get_map_name(x["location"])), "value": x["total_cases"]}, confirmed_records))
    death_data = list(map(lambda x: {"name": convert_name(get_map_name(x["location"])), "value": x["total_deaths"]}, death_records))
    unfound_samples = ['Aland', 'American Samoa', 'Br. Indian Ocean Ter.', 'Dem. Rep. Korea', 'Fr. S. Antarctic Lands', 'Heard I. and McDonald Is.', 'Kiribati', 'Lesotho', 'Micronesia', 'N. Cyprus', 'Niue', 'Palau', 'S. Geo. and S. Sandw. Is.', 'Saint Helena', 'Samoa', 'Siachen Glacier', 'Solomon Is.', 'St. Pierre and Miquelon', 'Timor-Leste', 'Tonga', 'Turkmenistan', 'Vanuatu']
    
    sample_zeros = list(map(lambda x: {'name': x, 'value':0 }, unfound_samples))
    confirmed_data.extend(sample_zeros)
    death_data.extend(sample_zeros)
    return {
        "confirmed": confirmed_data,
        "death": death_data,
    }


def build_world_map(db, config):
    export_path = config['export']['root']
    r = extract_world_map_from_owd(db, config)
    def get_export_path(name):
        return os.path.join(export_path, name )
    def process_map_data(item):
        data, filename = format_data(item[0] + "_map", item[1])
        if filename:
            path = get_export_path(filename)
            # data = data[:10]
            data.to_csv(path, index=False, quoting=csv.QUOTE_NONE)
    list(map(lambda item: process_map_data(item), r.items()))
    # list(map(lambda item: save_world_map(get_export_path(item[0]), item[1]), r.items()))
    # for key, value in r.items():
        # save_world_map(get_export_path(key), value)

def check_unmapped_countries(db, config):
    r = extract_world_map_from_owd(db, config)
    
    conversion = {
            'United States Virgin Islands': 'U.S. Virgin Is.',
            'Northern Mariana Islands': 'N. Mariana Is.',
            'South Korea': 'Korea',
            'Czech Republic': 'Czech Rep.',
            'Cayman Islands': 'Cayman Is.',
            'Sao Tome and Principe': 'São Tomé and Principe',
            'Equatorial Guinea': 'Eq. Guinea',
            'Cote d\'Ivoire': 'Côte d\'Ivoire',
            'Falkland Islands': 'Falkland Is.',
            'Faeroe Islands': 'Faeroe Is.',
            # 'Cayman Is': 'Cayman Is.',
            'French Polynesia': 'Fr. Polynesia',
            'Bosnia and Herzegovina': 'Bosnia and Herz.',
            'Antigua and Barbuda': 'Antigua and Barb.',
            'Saint Vincent and the Grenadines': 'St. Vin. and Gren.',
            'Turks and Caicos Islands': 'Turks and Caicos Is.',
            "Curacao": "Curaçao",
            "Laos": "Lao PDR",
            'Timor': 'Timor-Leste'
        }
    
    output_names = list(map(lambda x: conversion[x['name']] if x['name'] in conversion.keys() else x['name'], r['confirmed']))
    fp = open(config['path']['world_map_sample'], 'r')
    sample = pd.read_csv(fp)
    sample_names = list(sample['name'])
    print("output count: ", len(output_names))
    print("sample count: ", len(sample_names))
    def test_sample_name(name):

        def check_output(acc, c):
            if c == name:
                acc = 1
            return acc
        return {'sample_name': name, 'value': reduce(check_output, output_names, 0)}
    

    map_result = list(map(test_sample_name , sample_names))
    mapped_names = list(map(lambda x: x['sample_name'], filter(lambda x: x['value']==1, map_result)))
    unmapped = list(filter(lambda x: x['value']==0, map_result))
    
    unmapped_output_names = list(filter(lambda x: x not in mapped_names, output_names))
    print(unmapped_output_names)
    def search_name_in_outputs(sample):
        
        def check(acc, c):
            s = set(c)
            t = set(sample['sample_name'])
            mutual =  s & t
            sample_spilts = sample['sample_name'].split()
            output_splits = re.split(" ", c)
            if c in mapped_names:
                return acc

            abbreviations = {'S.': 'South', 'N.': 'North'}
            sample_spilts = list(map(lambda x: abbreviations[x] if x in abbreviations.keys() else x, sample_spilts))
            # Search by mutual words
            def f(counted, x):
                def g(z, y):
                    if y == x:
                        return z+1
                    return z
                return counted + reduce(g, output_splits,0) 
            r = reduce(f, sample_spilts, 0)
            if r >0:
                acc.append(c)

            # Search by abbreviation
            # if len(mutual) / len(s) > 0.7:
                # acc.append(c)
            return acc
        return {'sample_name': sample['sample_name'],'searched': reduce(check, output_names, [])}
    r = list(map(search_name_in_outputs, unmapped))


    list(map(lambda x: print(x), filter(lambda x: len(x['searched']) >= 0, r)))

def merge_objs(objs):
    r = {}
    def merge(acc, c):
        def f(key):
            acc[key] = c[key]
        list(map(f, c.keys()))
        return acc
    r = reduce(merge, objs, r)
    return r



    


def build_not_world(db, config):
    export_path = config['export']['root']
    def get_export_path( name, ext='.json'):
        return os.path.join(export_path, name + ext)
    # build_world_map(db, config)
    a = extract_conutry_data(db, config)
    # a = {}
    b = {}
    b = extract_global_seq(db.global_records)
    c = extract_conutry_seq(db, config)
    # c = {}
    r = merge_objs([a,b,c])
    report = build_report(r, config)
    report.to_csv(get_export_path("basic_info.csv", ""), quoting=csv.QUOTE_NONE, index=False)
    for key in r.keys():
        if key == "test_rate_seq":
            continue
        data, name = format_data(key, r[key])
        if name:
            path = get_export_path(name, '')
            data.to_csv(path, index=False, quoting=csv.QUOTE_NONE)
            # save_data(path, data)
    key_countries = ['西班牙', '美国', '意大利', '俄罗斯', '英国', '法国']
    def f(country):
        s = analyze_country(country, r, config)
        path = get_export_path(country)
        save_data(path, s)
    # list(map(f, key_countries))

def analyze():
    config = load_config()
    build_not_world(db, config)
    # check_unmapped_countries(db, config)
    build_world_map(db, config)

if __name__ == "__main__":
    analyze() 
    