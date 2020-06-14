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
from .process.descriptions import global_data_descriptions, country_data_descriptions, country_seq_descriptions, region_data_descriptions, stage_data_descriptions
from .compiler import Compiler
from .world_map import build_world_map
from .descriptions.default import get_default_descriptions
from .descriptions.mongo import load_descriptions
client = MongoClient()
db = client['coronavirus_analysis']

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


def extract_wxb_data(db, config, descsrc="default"):
    if descsrc == "default":
        descriptions = get_default_descriptions()
    else:
        descriptions = get_default_descriptions()
        ids = list(map(lambda x: x['id'], descriptions))
        _descriptions, _ids = load_descriptions(ids, db, config)
        # _ids = list(map(lambda x: x['id'], _descriptions))
        def update_description(description):
            if description['id'] in _ids:
                return _descriptions[description['id']]
            else:
                return description
        descriptions = list(map(update_description, descriptions))
        # descriptions = get_default_descriptions()
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


def build_not_world(db, config, descsrc="default"):
    export_path = config['export']['root']
    def get_export_path( name, ext='.json'):
        return os.path.join(export_path, name + ext)
    
    r = extract_wxb_data(db, config, descsrc)
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


def analyze(export_dir, config_path = "./handleData/config.json", descsrc="default"):
    config = load_config(config_path)
    # pa
    config['export']['root'] = export_dir
    build_not_world(db, config, descsrc)
    build_world_map(db, config)

def get_missing_countries():
    missing_countries = list(map(lambda x: x['chinese'], db.missing_countries.find()))
    return missing_countries

if __name__ == "__main__":
    analyze(export_dir="../main/static/export/run", config_path = "./config.json") 
    
    # docker  run  -v `pwd`:`pwd` -w `pwd` -t -p 8000:80 2a5f319370cb  