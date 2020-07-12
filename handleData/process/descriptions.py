from functools import reduce

from .operators import f_confirmed, f_death, f_confirmed_per_million, f_death_rate, f_newly_confirmed, f_newly_confirmed_death, f_newly_death
from .operators import calculate_death_rate, calculate_positive_rate, calculate_confirmed_rate, calculate_test_rate, calculate_recovery_rate
from .operators import add_to_seq
from .builders import build_topk, build_sort, build_append_others_func, build_insert_average, build_filter_records, build_filter_weekly, build_confirmed_condition
from .builders import build_filter_region, build_filter_seq, build_filter_stage
from .calculations import calculate_rate, calculate_growth
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
            "operator": lambda x:  [x["累计确诊"]],
            "preprocess": [],
            "postprocess": [
                build_topk(),
                build_sort(),
                build_append_others_func(lambda x:  [x["累计确诊"]])
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
                build_append_others_func(lambda x:  [x["累计死亡"]])
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
            "preprocess": [
                build_filter_records(lambda x: '总检测数' in x.keys() and x['总检测数'] > x['累计确诊'])
            ],
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
        {
            "id": "recovery_rate_data",
            "description": "Recovery rate of each country",
            "process": "last_day",
            "operator": calculate_recovery_rate,
            "preprocess": [
                build_filter_records(lambda x: x['累计确诊'] > 2000)
            ],
            "postprocess": [
                # build_topk(),
                build_sort(),
                build_insert_average("global_custom", lambda x: x['累计治愈']/x['累计确诊'])
            ]
        },
        
    ]

country_seq_descriptions = [
        {
            "id": "weekly_confirmed_data",
            "description": "Weekly confirmed data of each country",
            "process": "seq",
            "operator": lambda x : [sum(y['新增确诊'] for y in x)],
            "preprocess": [
                build_filter_weekly(-7)
            ],
            "postprocess": [
                build_sort(),
                build_topk(),
                build_append_others_func(lambda x: [sum(y['新增确诊'] for y in x[len(x)-7:])])
            ]
        },
        {
            "id": "weekly_death_data",
            "description": "Weekly death data of each country",
            "process": "seq",
            "operator": lambda x : [sum(y['新增死亡'] for y in x)],
            "preprocess": [
                build_filter_weekly()
            ],
            "postprocess": [
                build_sort(),
                build_topk(),
                build_append_others_func(lambda x: [sum(y['新增死亡'] for y in x[len(x)-7:])])
            ]
        },
        # TBD: 死亡累计大于100
        {
            "id": "weekly_confirmed_growth",
            "description": "Weekly confirmed growth of each country",
            "process": "seq",
            "operator": lambda x : [calculate_rate(sum(y['新增确诊'] for y in x[len(x)-7:]), sum(y['新增确诊'] for y in x[-14:-7])) - 1],
            "preprocess": [
                build_filter_weekly(-14,0),
                build_filter_records(lambda x: reduce(lambda acc, c: acc + c['新增确诊'], x[-7:], 0)>500 and x[-1]['累计确诊'] > 10000)

                # build_filter_records(lambda x: x[-1]['累计死亡']>100)
            ],
            "postprocess": [
                build_sort(),
                build_insert_average( "global",lambda x: [calculate_growth(sum(y['新增确诊'] for y in x[len(x)-7:]), sum(y['新增确诊'] for y in x[-14:-7]))])
            ]
        },
        {
            "id": "weekly_death_growth",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": lambda x : [calculate_growth(sum(y['新增死亡'] for y in x[-7:]), sum(y['新增死亡'] for y in x[-14:-7]))],
            "preprocess": [
                build_filter_weekly(-14,0),
                build_filter_records(lambda x: reduce(lambda acc, c: acc + c['新增死亡'], x[-7:], 0)>100 and x[-1]['累计死亡'] > 300 )
            ],
            "postprocess": [
                build_sort(),
                build_insert_average( "global",lambda x : [calculate_growth(sum(y['新增死亡'] for y in x[-7:]), sum(y['新增死亡'] for y in x[-14:-7]))])
            ]
        },
        {
            "id": "weekly_confirmed_growth_condition_1",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": lambda x : [calculate_growth(sum(y['新增确诊'] for y in x[-7:]), sum(y['新增确诊'] for y in x[-14:-7]))],
            "preprocess": [
                build_filter_weekly(-14,0),
                build_confirmed_condition()
            ],
            "postprocess": [
                build_sort(),
                build_insert_average( "global",lambda x : [calculate_rate(sum(y['新增确诊'] for y in x[-7:]), sum(y['新增确诊'] for y in x[-14:-7])) - 1])
            ]
        },
        {
            "id": "weekly_death_growth_condition_1",
            "description": "Weekly death growth of each country",
            "process": "seq",
            "operator": lambda x : [calculate_growth(sum(y['新增死亡'] for y in x[-7:]), sum(y['新增死亡'] for y in x[-14:-7]))],
            "preprocess": [
                build_filter_weekly(-14,0),
                build_confirmed_condition(),
            ],
            "postprocess": [
                build_sort(),
                build_insert_average( "global",lambda x : [calculate_rate(sum(y['新增死亡'] for y in x[-7:]), sum(y['新增死亡'] for y in x[-14:-7])) - 1])
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
                build_filter_region("全球")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_tbr",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_region("一带一路")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_africa",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_region("非洲")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "regions_daily_confirmed_recovered_around",
            "description": "Daily confirmed and recovered data",
            "process": "region",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_region("周边")
            ],
            "postprocess": [
                build_filter_seq(97)
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
                build_filter_stage("上行")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_downward",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_stage("下行")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_vibration",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_stage("震荡")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
        {
            "id": "stage_daily_confirmed_recovered_final",
            "description": "Daily confirmed and recovered data",
            "process": "stage",
            "operator": add_to_seq,
            "preprocess": [
                build_filter_stage("尾期")
            ],
            "postprocess": [
                build_filter_seq(97)
            ]
        },
    ]