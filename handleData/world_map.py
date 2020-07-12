import dateutil.parser
from datetime import datetime, timedelta
from .format import format_data
import os
import csv

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

