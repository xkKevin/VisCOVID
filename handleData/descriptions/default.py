from functools import reduce
from ..components.element import InsertAverage, AppendOthers
from ..components.rearrange import Sort, TopK
from ..components.filters import StageFilter, RegionFilter, WeeklyFilter, SeqFilter, RecordsFilter, ConfirmedConditionFilter, NanFilter
from ..process.calculations import * 
from ..process.operators import *

global_data_descriptions = [
        {
            "id": "global_confirmed_seq",
            "description": "",
            "process": "global",
            "operator": f_confirmed,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_death_seq",
            "description": "",
            "process": "global",
            "operator": f_death,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_confirmed_per_million_seq",
            "description": "",
            "process": "global",
            "operator": f_confirmed_per_million,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_death_rate_seq",
            "description": "",
            "process": "global",
            "operator": f_death_rate,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_confirmed_weekly_seq",
            "description": "",
            "process": "global",
            "operator": f_newly_confirmed,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_confirmed_death_seq",
            "description": "",
            "process": "global",
            "operator": f_newly_confirmed_death,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_death_weekly_seq",
            "description": "",
            "process": "global",
            "operator": f_newly_death,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_newly_confirmed_seq",
            "description": "",
            "process": "global",
            "operator": f_newly_confirmed_death,
            "preprocess": [],
            "postprocess": [],
        },
        {
            "id": "global_newly_death_seq",
            "description": "",
            "process": "global",
            "operator": f_newly_confirmed_death,
            "preprocess": [],
            "postprocess": [],
        },
        
    ] 


country_data_descriptions = [
        {
            "id": "confirmed_data",
            "description": "Confirmed data of each country",
            "process": "last_day",
            "operator": "lambda x:  [x['累计确诊']]",
            "preprocess": [],
            "postprocess": [
                TopK(),
                Sort(), 
                AppendOthers("lambda x:  [x['累计确诊']]")
            ]
        },
        {
            "id": "death_data",
            "description": "Confirmed data of each country",
            "process": "last_day",
            "operator": "lambda x:  [x['累计死亡']]",
            "preprocess": [],
            "postprocess": [
                TopK(),
                Sort(),
                AppendOthers("lambda x:  [x['累计死亡']]")
            ]
        },
        {
            "id": "test_rate_data",
            "description": "Test rate data of each country",
            "process": "last_day",
            "operator": calculate_test_rate,
            "preprocess": [],
            "postprocess": [
                Sort(),
                InsertAverage("counted", "lambda x: [x['总检测数']/ x['人口']]")
            ]
        },
        {
            "id": "positive_rate_data",
            "description": "Positive rate data of each country",
            "process": "last_day",
            "operator": calculate_positive_rate,
            "preprocess": [
                RecordsFilter("lambda x: '总检测数' in x.keys() and x['总检测数'] > x['累计确诊']")
            ],
            "postprocess": [
                Sort(),
                InsertAverage("counted", calculate_positive_rate)
            ]
        },
        {
            "id": "test_num_data",
            "description": "Test num data of each country",
            "process": "last_day",
            "operator": "lambda x: [x['总检测数']]",
            "preprocess": [],
            "postprocess": [
                Sort(),
            ]
        },
        {
            "id": "confirmed_rate_data",
            "description": "Confirmed rate of each country",
            "process": "last_day",
            "operator": calculate_confirmed_rate,
            "preprocess": [],
            "postprocess": [
                Sort(),
                InsertAverage("global_custom", "lambda g: g['百万人口确诊率']/1000000.")
            ]
        },
        {
            "id": "death_rate_data",
            "description": "Death rate of each country",
            "process": "last_day",
            "operator": calculate_death_rate,
            "preprocess": [],
            "postprocess": [
                Sort(),
                InsertAverage("global", calculate_death_rate)
            ]
        },
        {
            "id": "recovery_rate_data",
            "description": "Recovery rate of each country",
            "process": "last_day",
            "operator": calculate_recovery_rate,
            "preprocess": [
                RecordsFilter("lambda x: x['累计确诊'] > 2000")
            ],
            "postprocess": [
                Sort(),
                InsertAverage("global_custom", "lambda x: x['累计治愈']/x['累计确诊']")
            ]
        },
        
    ]

country_seq_descriptions = [
        {
            "id": "weekly_confirmed_data",
            "description": "Weekly confirmed data of each country",
            "process": "seq",
            "operator": "lambda x: [x[-1]['累计确诊'] -  x[-8]['累计确诊']]",
            "preprocess": [
                WeeklyFilter(10)
            ],
            "postprocess": [
                Sort(),
                TopK(),
                AppendOthers("lambda x: [x[-1]['累计确诊'] -  x[-8]['累计确诊']]")
            ]
        },
        {
            "id": "weekly_death_data",
            "description": "Weekly death data of each country",
            "process": "seq",
            "operator": "lambda x: [x[-1]['累计死亡'] -  x[-8]['累计死亡']]",
            "preprocess": [
                WeeklyFilter(10)
            ],
            "postprocess": [
                Sort(),
                TopK(),
                AppendOthers("lambda x: [x[-1]['累计死亡'] -  x[-8]['累计死亡']]")
            ]
        },
        # TBD: 死亡累计大于100
        {
            "id": "weekly_confirmed_growth",
            "description": "Weekly confirmed growth of each country",
            "process": "seq",
            "operator": "lambda x: [calculate_growth(x[-1]['累计确诊'] - x[-8]['累计确诊'], x[-8]['累计确诊'] - x[-15]['累计确诊']) ]",
            "preprocess": [
                WeeklyFilter(15,0),
                RecordsFilter("lambda x: x[-1]['累计确诊'] - x[-8]['累计确诊']>500 and x[-1]['累计确诊'] > 10000")
            ],
            "postprocess": [
                Sort(),
                InsertAverage( "global","lambda x: [calculate_growth(x[-1]['累计确诊'] - x[-8]['累计确诊'], x[-8]['累计确诊'] - x[-15]['累计确诊'] ) ]")
            ]
        },
        {
            "id": "weekly_death_growth",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": "lambda x: [calculate_growth(x[-1]['累计死亡'] - x[-8]['累计死亡'], x[-8]['累计死亡'] - x[-15]['累计死亡']) ]",
            "preprocess": [
                WeeklyFilter(15,0),
                RecordsFilter("lambda x: x[-1]['累计死亡'] - x[-8]['累计死亡'] >100 and x[-1]['累计死亡'] > 300" )
            ],
            "postprocess": [
                Sort(),
                InsertAverage( "global","lambda x: [calculate_growth(x[-1]['累计死亡'] - x[-8]['累计死亡'], x[-8]['累计死亡'] - x[-14]['累计死亡'] + x[-14]['新增死亡']) ]")
            ]
        },
        {
            "id": "weekly_confirmed_growth_condition_1",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": "lambda x : [calculate_growth(sum(y['新增确诊'] for y in x[-1:]), sum(y['新增确诊'] for y in x[-8:-7]))]",
            "preprocess": [
                WeeklyFilter(14,0),
                ConfirmedConditionFilter()
            ],
            "postprocess": [
                Sort(),
                InsertAverage( "global","lambda x : [calculate_rate(sum(y['新增确诊'] for y in x[-1:]), sum(y['新增确诊'] for y in x[-8:-7])) - 1]")
            ]
        },
        {
            "id": "weekly_death_growth_condition_1",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": "lambda x : [calculate_growth(sum(y['新增死亡'] for y in x[-1:]), sum(y['新增死亡'] for y in x[-8:-7]))]",
            "preprocess": [
                WeeklyFilter(14,0),
                ConfirmedConditionFilter(),
            ],
            "postprocess": [
                Sort(),
                InsertAverage( "global","lambda x : [calculate_rate(sum(y['新增死亡'] for y in x[-7:]), sum(y['新增死亡'] for y in x[-14:-7])) - 1]")
            ]
        },
    ]

region_data_descriptions = [
        {
            "id": "regions_daily_confirmed_recovered_global",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                RegionFilter("全球")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_tbr",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                RegionFilter("一带一路")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_africa",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                RegionFilter("非洲")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_around",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                RegionFilter("周边")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        }
    ]

stage_data_descriptions = [
        {
            "id": "stage_daily_confirmed_recovered_upward",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                StageFilter("上行")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_downward",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                StageFilter("下行")
            ],
            "postprocess": [
                # SeqFilter(197)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_vibration",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                StageFilter("震荡")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_final",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                StageFilter("尾期")
            ],
            "postprocess": [
                # SeqFilter(97)
            ]
        },
    ]
def get_default_descriptions():
    descriptions = []
    descriptions.extend(global_data_descriptions)
    descriptions.extend(country_data_descriptions)
    descriptions.extend(country_seq_descriptions)
    descriptions.extend(region_data_descriptions)
    descriptions.extend(stage_data_descriptions)
    return descriptions