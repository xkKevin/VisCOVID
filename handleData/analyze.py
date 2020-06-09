import os
import pandas as pd
from pymongo import MongoClient
from functools import reduce
import numpy as np
from .utils import save_data, load_config, find_population_by_chinese_name, save_world_map, build_time_range
from datetime import datetime, timedelta
import dateutil.parser
from .format import format_data
import csv
from .report import build_report
import re
from .process.builders import build_filter_nan, build_filter_records
from .process.descriptions import global_data_descriptions, country_data_descriptions, country_seq_descriptions, region_data_descriptions, stage_data_descriptions
client = MongoClient()
db = client['coronavirus_analysis']



class Compiler():
    def __init__(self, db, config):
        self.db = db
        self.config = config

    def compile(self, description):
        db = self.db
        config = self.config
        if description['process'] == "global":
            data = process_global_seq(description['operator'], description['preprocess'], description['postprocess'])(db, config)
        elif description['process'] == "last_day":
            data = process_country_record_last_day( description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "seq":
            data = process_country_seq(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "region":
            data = process_region_records(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        elif description['process'] == "stage":
            data = process_stage_records(description['operator'], preprocess=description['preprocess'],postprocess=description['postprocess'])(db, config)
        else:
            data = None
            print("Invalid process specified")
        return {
            "id": description['id'],
            "data": data
        }
    def get_compile_func(self):
        def compile(description):
            return self.compile(description)
        return compile
            




# 072798
# Global Sequence
# 全球累计增长曲线 confirmed_seq
# 全球累计死亡增长曲线 death_seq
# 全球确诊率增长曲线 confirmed_per_million
# 全球病死率 death_rate_seq = 累计死亡/累计确诊
# def build_filter_days(first_date):
#     def filter_days(records, context):
#         return list(filter(lambda x: x['日期'] > first_date), records), context
#     return 

def process_global_seq(operator, preprocess, postprocess):
    def build_final_seq(db, config):
        found = list(db.global_records.find())
        found.sort(key=lambda x: x['日期'])
        truncated = list(filter(lambda x: not np.isnan(x['累计确诊']), found))
        context = {}
        def generate_default_seq():
            return {'x': [], 'y': []}
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, found)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
    return build_final_seq



# Extract country data which is accessible from the newest data
# 国家确诊数据 confirmed_data
# 国家死亡数据 death_data






# TBD: Multi-column values support
# TBD: Better support for records filtering
        




def process_country_record_last_day(f, args=dict() , preprocess=[], postprocess=[]):

    # Query the MongoDB
    
        # Build the dataset table
    def filter_2000(x):
        # if x ['国家地区'] == "冰岛":
            # print(x)
        # print(x)
        if x['累计确诊'] >= 2000.:
            return True
        else:
            return False
    preprocess.insert(0,build_filter_records(filter_2000) )
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
            "global_record": global_record,
            "db": db,
        }
        def process(acc, c):
            return c(acc, context)[0]
        
        found = reduce(process, preprocess, found)
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
            values.insert(0, {"name": "各国平均", "value":average_value})
        if average == "global_custom":
            global_record = db.global_records.find_one({"日期": check_date})
            values.insert(0, {"name": "各国平均", "value":average_func(global_record)})
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



# Extract country data which can not be accessible from the newest data

def process_country_seq( operator, preprocess=[], postprocess=[]):
    def build_final_seq(db, config, with_others = False, period_start=-7, period_end=0, key="seq", top=-1, compare=lambda x: x['value'], sorted=False, post_filter=lambda x: True):
        countries = db.selected_countries.find({})
        check_date = dateutil.parser.parse(config['time']['end'])
        check_date -= timedelta(days=1)
        found = list(map(lambda x: list(db.country_records.find({"国家地区": x['chinese'], "日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}})), countries))


        def extract_weekly_global():
            global_records = list(db.global_records.find({"日期":{"$lte": check_date, "$gt": check_date - timedelta(days=14)}}))
            return global_records
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
        # global_weekly_confirmed, global_weekly_death, global_last_weekly_confirmed, global_last_weekly_death = extract_weekly_global()
        global_records = extract_weekly_global()
        context = {
            "records": found,
            "record": found,
            "global_record": global_records,
            "db": db,
        }
        def process(acc, c):
            return c(acc, context)[0]
        preprocess.insert(0,build_filter_records(lambda x: x[-1]['累计确诊']>=2000) )
        mfound = reduce(process, preprocess, found)
        # mfound = list(filter(filter_country, mfound))
        # Process on the records

        data = list(map(lambda x: {"name": x[0]['国家地区'], "values": operator(x)}, mfound))
        data = reduce(process, postprocess, data) 

        return data

    return build_final_seq



def process_region_records(operator, preprocess=[], postprocess=[]):
    def build_final_data(db, config):
        def generate_default_seq():
            return {'x': [], 'y': [[],[]]}
        records = db.region_records.find({})
        context = {}
        check_date = dateutil.parser.parse(config['time']['end'])
        # check_date -= timedelta(days=1)
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, records)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
        # mfound = list(filter(filter_country, mfound))
        # Process on the records

        # data = list(map(lambda x: {"name": x[0]['国家地区'], "values": operator(x)}, mfound))
        # data = reduce(process, postprocess, data) 
    return build_final_data



def process_stage_records(operator, preprocess=[], postprocess=[]):
    def build_final_data(db, config):
        def generate_default_seq():
            return {'x': [], 'y': [[],[]]}
        records = db.stage_records.find({})
        context = {}
        check_date = dateutil.parser.parse(config['time']['end'])
        # check_date -= timedelta(days=1)
        def process(acc, c):
            return c(acc, context)[0]
        data = reduce(process, preprocess, records)
        data = reduce(operator, data, generate_default_seq())
        data = reduce(process, postprocess, data)
        return data
        # mfound = list(filter(filter_country, mfound))
        # Process on the records

        # data = list(map(lambda x: {"name": x[0]['国家地区'], "values": operator(x)}, mfound))
        # data = reduce(process, postprocess, data) 
    return build_final_data


def extract_wxb_data(db, config):
    descriptions = []
    descriptions.extend(global_data_descriptions)
    descriptions.extend(country_data_descriptions)
    descriptions.extend(country_seq_descriptions)
    descriptions.extend(region_data_descriptions)
    descriptions.extend(stage_data_descriptions)
    compiler = Compiler(db, config)
    
    compile_func = compiler.get_compile_func()
    data = list(map(compile_func, descriptions))
    # confirmed_data = process_country_record_last_day(lambda x: [x["累计确诊"]], postprocess=[build_topk(), build_sort(), build_append_others_func(lambda x: [x["累计确诊"]], global_record)])(db, config)
    obj = {}
    for item in data:
        obj[item['id']] = item['data']
    return obj

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
    # confirmed_records = list(db.owd_all.find({"date": check_date, "location": {"$nin": exclude_entities}}))
    confirmed_records = list(db.owd_all.aggregate([{"$group": {
        "_id": "$location",
        "location": {"$last": "$location"},
        "total_cases": {"$last": "$total_cases"}
    }}]))
    confirmed_records = list(db.owd_all.aggregate([
        {
            "$group": {
                "_id": "$location",
                "location": {"$last": "$location"},
                "total_cases": {"$last": "$total_cases"},
                "total_deaths": {"$last": "$total_deaths"}
            }
        },
        {
            "$sort":{
                "location": 1,
            }

        }]))
    # death_records = list(db.owd_all.find({"date": check_date, "location": {"$nin": exclude_entities}}))
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
    death_data = list(map(lambda x: {"name": convert_name(get_map_name(x["location"])), "value": x["total_deaths"]}, confirmed_records))
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


    # list(map(lambda x: print(x), filter(lambda x: len(x['searched']) >= 0, r)))

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
    # a = extract_conutry_data(db, config)
    # # a = {}
    # b = {}
    # b = extract_global_seq(db, config)
    # c = extract_conutry_seq(db, config)
    # d = extract_region_data(db, config)
    # e = extract_stage_data(db, config)
    # # c = {}
    # r = merge_objs([a,b,c,d,e])
    r = extract_wxb_data(db, config)
    due = db.due.find_one()
    r['due'] = due
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


def analyze(export_dir, config_path = "./handleData/config.json"):
    config = load_config(config_path)
    # pa
    config['export']['root'] = export_dir
    build_not_world(db, config)
    # check_unmapped_countries(db, config)
    build_world_map(db, config)

def get_missing_countries():
    missing_countries = list(map(lambda x: x['chinese'], db.missing_countries.find()))
    return missing_countries


if __name__ == "__main__":
    analyze(export_dir="../main/static/export/run", config_path = "./config.json") 
    
    # docker  run  -v `pwd`:`pwd` -w `pwd` -t -p 8000:80 2a5f319370cb  