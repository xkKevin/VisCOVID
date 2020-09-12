# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 09:48:46 2020

@author: 93702
"""

## part1：定义相关变量
import pandas as pd, datetime
import xlrd
import xlsxwriter

def process_data(time_data):

    data_file = "./main/static/data/wang.xlsx"
    four_area_data_file = "./main/static/data/regions.xlsx"
    world_map_data = "./main/static/data/owd.csv"
    countries_json_data = "./main/static/data/countries.info.json"
    data_extract = "./main/static/data/Data_Extract_From_World_Development_Indicators.csv"

    path = "./main/static/export/"
    
    
    # data_file = '全球及重点国家疫情主要指数数据-2020-8-24-6H30.xlsx'
    # if not time_data:
    #     time_data = data_file
        
    # countries_json_data = 'countries.info.json'
    # data_extract = 'Data_Extract_From_World_Development_Indicators.csv'
    # four_area_data_file = '四个大区域以及四个阶段疫情主要指数数据-2020-8-24-6H30.xlsx'
    # world_map_data = 'owid-covid-data.csv'
    # path = ''

    tarfile = data_file[0: data_file.rfind('.')] + '_1' + '.xlsx'
    end_date = pd.to_datetime(time_data[time_data.find('-') + 1: time_data.rfind('-')])
    start_date = end_date - pd.Timedelta('13 days')
    date_range = pd.date_range(start_date, end_date)
    last_monday = date_range[0]
    last_sunday = date_range[6]
    this_monday = date_range[7]
    this_sunday = date_range[13]

    del_sheet_name = ['中国大陆', '香港', '台湾', '澳门', '全球2', '法国CDC', '北马其顿', '马约特', '法属圭亚那', 'Sheet1', 'Sheet2', 'Sheet3',
                      'Sheet4', '总表']

    ## part2：处理人口数据
    # 获取国家名称
    with open(countries_json_data, 'r', encoding = 'utf-8') as fp:
        countries_json = pd.read_json(fp, orient = 'records')
    df_country = countries_json[['country_code3', 'country_name_chinese_short']]
    # print(df_country)

    # 获取国家人口数据
    df = pd.read_csv(data_extract)
    df_num = df[['Country Code', '2018 [YR2018]']]

    # 合并国家和人口，生成对应国家人口数据表
    df_people = pd.merge(df_country, df_num, left_on = 'country_code3', right_on = 'Country Code', how = 'left')
    df_people1 = df_people.rename(
        columns={'country_name_chinese_short': '国家', '2018 [YR2018]': '2018人口', 'country_code3': '3编码'})
    df_peolpe_num = df_people1[['国家', '2018人口', '3编码']]


    ## part3：合并所有国家数据-----当提供的ecxel中国家名称只缺少后半部分时
    # 读文件
    data = xlrd.open_workbook(data_file)

    # 获取sheet页名称并过滤;
    sheet_names = data.sheet_names()
    sheet_names_fin = []
    for i in sheet_names:
        if i not in del_sheet_name:
            sheet_names_fin.append(i)
    # print('一共有%i个国家' %(len(sheet_names_fin)-1))
    # print(sheet_names_fin)

    # 新建目标文件
    wh = xlsxwriter.Workbook(tarfile)
    wadd = wh.add_worksheet('all countries')

    tar = []
    name_title = []
    # 读取源文件数据
    for sheet_name in sheet_names_fin:
        # 获取sheet页的名称
        sheet = data.sheet_by_name(sheet_name)
        # 获取表头
        sh_title = data.sheet_by_index(0).row_values(0)
        wadd.write_row('A1', sh_title)
        # 获取表的行数
        nrows = sheet.nrows
        # 循环打印
        for i in range(nrows):
            #跳过第一行
            if i == 0:
                name_title.append({sheet_name:sheet.row_values(i)})
            else:
                tar.append(sheet.row_values(i))

    for row_num, row_data in enumerate(tar):
        wadd.write_row(row_num + 1, 0, row_data)
    wh.close()
    
    # 判断标题是否有变动
    title_list = ['国家地区', '日期', '累计确诊', '新增确诊', '累计死亡', '新增死亡', '累计治愈', '仍在治疗', \
                  '重症病例', '百万人口确诊率', '百万人口死亡率', '总检测数', '百万人口检测率']
    for i in name_title:
        country = list(i.keys())[0]
        title = list(i.values())[0][0:13]    # [0:13]排除无用的标题
    #     print(title)
        error_title = [i for i in title_list if i not in title]
        if len(error_title) > 0:
            print('\n标题有错的国家为：' + country + '，错误标题为：' + str(error_title))
            return [False, '标题有错的国家为：' + country + '，错误标题为：' + str(error_title)]

    ## part4：读取合并后的疫情数据并整理
    df_yq = pd.read_excel(tarfile, sheet_name = 0)
    df_yq = df_yq[df_yq['日期'].notna()]
    df_yq['国家地区'].fillna(method='ffill', inplace = True)  # 补充国家名称-------当提供的excel中国家名称不全时
    country_lst = df_yq['国家地区'].values.tolist()
    country_dic = {'刚果': '刚果(布)',
                   '刚果民主共和国': '刚果(金)'}
    country_lst = [country_dic[i] if i in country_dic else i for i in country_lst]
    del df_yq['国家地区']
    df_yq['国家地区'] = country_lst
    df_yq = df_yq.rename(columns = {'日期': '日期戳'})

    # 将日期戳变成"pandas._libs.tslibs.timestamps.Timestamp"
    def date(dates):  # 定义转化日期戳的函数,dates为日期戳
        delta = datetime.timedelta(days = dates)
        today = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta
        return pd.to_datetime(datetime.datetime.strftime(today, '%Y-%m-%d'))

    t_list = []
    for i in df_yq['日期戳']:
        t = date(i)
        t_list.append(t)

    df_yq['日期'] = t_list
    del df_yq['日期戳']

    # 通过累计确诊和累计病死计算新增确诊和新增病死
    df_yq['累计确诊1'] = df_yq['累计确诊'].shift(1)  # 向下移一行
    df_yq['新增确诊1'] = df_yq['新增确诊']
    df_yq['新增确诊'] = df_yq['累计确诊'] - df_yq['累计确诊1']
    df_yq.loc[df_yq['日期'] == pd.to_datetime('2020-02-01'),'新增确诊'] = ''
    df_yq['累计死亡1'] = df_yq['累计死亡'].shift(1)
    df_yq['新增死亡1'] = df_yq['新增死亡']
    df_yq['新增死亡'] = df_yq['累计死亡'] - df_yq['累计死亡1']
    df_yq.loc[df_yq['日期'] == pd.to_datetime('2020-02-01'),'新增死亡'] = ''
    # print(df_yq)

    # 将人口数据合并
    df_data = pd.merge(df_yq, df_peolpe_num, left_on = '国家地区', right_on = '国家', how = 'left')
    df_data = df_data[['国家地区', '日期', '累计确诊', '新增确诊', '累计死亡', '新增死亡', '累计治愈', '仍在治疗', '重症病例',
                       '百万人口确诊率', '百万人口死亡率', '总检测数', '百万人口检测率', '2018人口', '3编码']]
    df_data = df_data[df_data['日期'] <= end_date]  # 只保留当前日期前的所有数据

    # 判断未匹配上人口的国家
    df_data1 = df_data[df_data['2018人口'].isnull()]
    country_list = list(set(list(df_data1['国家地区'])))
    if len(country_list) > 0:
        print('未匹配上人口的国家为%s，已删除' % country_list)

    # 判断是否所有国家的最后日期一致
    data_test = df_data[['国家地区', '日期', '累计确诊']]
    dd1 = data_test.loc[data_test[data_test.日期 == this_sunday].index.tolist()][["国家地区", "累计确诊"]].rename(
        columns={'累计确诊': '2'})
    countries_null = dd1[dd1['2'].isnull()]["国家地区"].tolist()
    countries_error = countries_null
    if len(countries_error) > 0:
        print('缺少当天数据的国家为%s，已删除' % countries_error)
    del_country_list = list(set(country_list + countries_error))
    df_data = df_data[-df_data.国家地区.isin(del_country_list)]  # 删除未匹配上人口和缺少当天数据的国家
#     df_data.to_csv('清洗后数据.csv', index = False, encoding = 'gbk')   # 保存清洗后的数据


    ## part5：条件参数设置
    def countries(df, day_1, day_2, condition_name, condition_num):
        df_1 = df[(df['日期'] >= day_1) & (df['日期'] <= day_2)]
        df_1 = df_1.groupby(by = ['国家地区'])[condition_name].sum().reset_index(name = condition_name + '_sum')
        lst = df_1[df_1[condition_name + '_sum'] <= condition_num]['国家地区'].values.tolist()
        return lst

    lst1 = countries(df_data, this_sunday, this_sunday, '累计确诊', 3000)   # 累计确诊<=2000的国家，后改成<=3000
    lst2 = countries(df_data, this_sunday, this_sunday, '累计确诊', 10000)  # 累计确诊<=10000的国家
    lst3 = countries(df_data, this_sunday, this_sunday, '累计死亡', 300)    # 累计死亡<=300的国家
    lst5 = countries(df_data, this_monday, this_sunday, '新增确诊', 500)    # 本周新增确诊<=500国家
    lst6 = countries(df_data, this_monday, this_sunday, '新增死亡', 100)    # 本周新增病死<=100国家

    ## part6：正文图表数据导出
    ## 2-1和2-2世界地图数据
    df = pd.read_csv(world_map_data)
    df = df[df['continent'].notna()]    # 删除没有洲的国家
    df_select = df.groupby(by = ['location'])['date'].max().reset_index(name = 'date')   # 选取最大日期
    df = df[['location', 'date','total_cases', 'total_deaths']]
    df_merge = pd.merge(df, df_select, on = ['location', 'date'], how = 'right')
    location_list = df_merge['location'].values.tolist()
    location_dic = {'Antigua and Barbuda' : 'Antigua and Barb.', 'Bosnia and Herzegovina' : 'Bosnia and Herz.',
                    'Cayman Islands' : 'Cayman Is.', 'Central African Republic' : 'Central African Rep.',
                    'Cote d\'Ivoire' : 'Côte d\'Ivoire', 'Curacao' : 'Curaçao', 'Czech Republic' : 'Czech Rep.',
                    'Democratic Republic of Congo' : 'Dem. Rep. Congo', 'Dominican Republic' : 'Dominican Rep.',
                    'Equatorial Guinea' : 'Eq. Guinea', 'Faeroe Islands' : 'Faeroe Is.', 'Falkland Islands' : 'Falkland Is.',
                    'French Polynesia' : 'Fr. Polynesia', 'Laos' : 'Lao PDR', 'Northern Mariana Islands' : 'N. Mariana Is.',
                    'Saint Vincent and the Grenadines' : 'St. Vin. and Gren.', 'Sao Tome and Principe' : 'São Tomé and Principe',
                    'South Korea' : 'Korea', 'South Sudan' : 'S. Sudan', 'Turks and Caicos Islands' : 'Turks and Caicos Is.',
                    'United States Virgin Islands' : 'U.S. Virgin Is.', 'Western Sahara' : 'W. Sahara'}
    location_list = [location_dic[i] if i in location_dic else i for i in location_list]
    del df_merge['location']
    df_merge['location'] = location_list
    df_merge.columns = [['日期', '累计确诊人数', '累计病死人数','国家']]
    df_2_1 = df_merge[['国家', '累计确诊人数']]
    df_2_2 = df_merge[['国家', '累计病死人数']]
    df_2_1.to_csv(path + '2-1.csv', index = False, encoding = 'utf-8')
    df_2_2.to_csv(path + '2-2.csv', index = False, encoding = 'utf-8')
#     print(df_merge)

    # 2-3-a至2-4-b函数
    def data_4(df, name):
        df = df[df['国家地区'] == '全球']
        if name == '全球累计确诊人数':
            df = df[df['累计确诊'].notna()][['日期','累计确诊']].rename(columns = {'累计确诊':'全球累计确诊人数'})
            return df
        elif name == '全球累计病死人数':
            df = df[df['累计死亡'].notna()][['日期','累计死亡']].rename(columns = {'累计死亡':'全球累计病死人数'})
            return df
        elif name == '全球确诊率':
            df['全球确诊率'] = df['百万人口确诊率'].astype(float) / 1000000
            return df[['日期','全球确诊率']]
        elif name == '全球病死率':
            df['全球病死率'] = df['累计死亡'].astype(float) / df['累计确诊'].astype(float)
            return df[['日期','全球病死率']]

        else:
            print('error')

    data_4(df_data, '全球累计确诊人数').to_csv(path + '2-3-a.csv', index = False, encoding = 'utf-8')    # 2-3-a 全球累计确诊人数
    data_4(df_data, '全球累计病死人数').to_csv(path + '2-3-b.csv', index = False, encoding = 'utf-8')    # 2-3-b 全球累计病死人数
    data_4(df_data, '全球确诊率').to_csv(path + '2-4-a.csv', index = False, encoding = 'utf-8')          # 2-4-a 全球确诊率
    data_4(df_data, '全球病死率').to_csv(path + '2-4-b.csv', index = False, encoding = 'utf-8')          # 2-4-b 全球病死率

    # 2-5-a 全球新增确诊人数
    data_wld_confirmed_new = df_data[df_data['国家地区'] == '全球']
    data_wld_confirmed_new = data_wld_confirmed_new.rename(columns = {'新增确诊': '新增确诊人数'})
    data_wld_confirmed_new[['日期', '新增确诊人数']].to_csv(path + '2-5-a.csv', index = False, encoding = 'utf-8')

    # 2-5-b 全球新增死亡人数
    data_wld_death_new = df_data[df_data['国家地区'] == '全球']
    data_wld_death_new = data_wld_death_new.rename(columns = {'新增死亡': '新增病死人数'})
    data_wld_death_new[['日期', '新增病死人数']].to_csv(path + '2-5-b.csv', index = False, encoding = 'utf-8')
    
    # 2-6 累计确诊人数-周末数据，前15名
    wld_confirmed_data = df_data[df_data['国家地区'] == '全球']
    wld_confirmed_data = wld_confirmed_data[wld_confirmed_data['日期'] == this_sunday]
    # print(wld_confirmed_data)
    data_confirmed = df_data[df_data['国家地区'] != '全球']
    data_confirmed = data_confirmed[data_confirmed['日期'] == this_sunday]
    data_confirmed = data_confirmed[['国家地区', '累计确诊']]
    data_confirmed = data_confirmed[data_confirmed['累计确诊'].notna()]
    data_confirmed = data_confirmed.rename(columns = {'国家地区': '国家', '累计确诊': '累计确诊人数'})
    data_confirmed = data_confirmed.sort_values(['累计确诊人数'], ascending = False).reset_index(drop = True)[
                     0:15]  # 降序，重新编写index，取前15
    # print(data_confirmed)
    # 创建一个其他的DataFrame
    data = {'国家': '其他',
            '累计确诊人数': wld_confirmed_data['累计确诊'] - data_confirmed['累计确诊人数'].sum()}
    df = pd.DataFrame(data)
    # print(df)
    data_confirmed_result = data_confirmed.append(df).reset_index(drop = True)  # 合并到一张表中
    data_confirmed_result.to_csv(path + '2-6.csv', index = False, encoding = 'utf-8')

    # 2-7 累计病死人数-周末数据，前15名
    wld_death_data = df_data[df_data['国家地区'] == '全球']
    wld_death_data = wld_death_data[wld_death_data['日期'] == this_sunday]
    # print(wld_death_data)
    data_death = df_data[df_data['国家地区'] != '全球']
    data_death = data_death[data_death['日期'] == this_sunday]
    data_death = data_death[['国家地区', '累计死亡']]
    data_death = data_death[data_death['累计死亡'].notna()]
    data_death = data_death.rename(columns = {'国家地区': '国家', '累计死亡': '累计病死人数'})
    data_death = data_death.sort_values(['累计病死人数'], ascending = False).reset_index(drop = True)[0:15]  # 降序，重新编写index，取前15
    # print(data_death)
    # 创建一个其他的DataFrame
    data = {'国家': '其他',
            '累计病死人数': wld_death_data['累计死亡'] - data_death['累计病死人数'].sum()}
    df = pd.DataFrame(data)
    # print(df)
    data_death_result = data_death.append(df).reset_index(drop = True)  # 合并到一张表中
    data_death_result.to_csv(path + '2-7.csv', index = False, encoding = 'utf-8')

    # 设置函数
    def rate5(df, column1, column2):
        df = df[df['日期'] == this_sunday]
        df = df[-df.国家地区.isin(lst1)].reset_index(drop = True)  # 剔除累计确诊小于2000的国家
        df = df.rename(columns = {'国家地区': '国家'})
        if column1 == '百万人口确诊率' and column2 == '百万人口确诊率':
            df['确诊率'] = df[column1].astype(float) / 1000000
            df = df[df['确诊率'] <= 1]
            return df
        elif column1 == '累计死亡' and column2 == '累计确诊':
            df['病死率'] = df[column1].astype(float) / df[column2].astype(float)
            df = df[df['病死率'] <= 1]
            return df
        elif column1 == '累计确诊' and column2 == '累计治愈':
            df['治愈率'] = df[column2].astype(float) / df[column1].astype(float)
            df = df[df['治愈率'] <= 1]
            return df
        elif column1 == '百万人口检测率' and column2 == '百万人口检测率':
            df = df[df['总检测数'].astype(float) > 0]
            df = df[df['2018人口'].astype(float) > 0]
            df = df[df['百万人口检测率'].notna()]
            df['检测率'] = df[column1].astype(float) / 1000000
            df = df[df['检测率'] <= 1]
            return df
        elif column1 == '累计确诊' and column2 == '总检测数':
            df = df[df['累计确诊'].astype(float) > 0]
            df = df[df['总检测数'].astype(float) > 0]
            df['阳性率'] = df[column1].astype(float) / df[column2].astype(float)
            df = df[df['阳性率'] <= 1]
            return df
        else:
            print('excel标题有改动!')
            return False

    # 2-8 确诊率---/1000000算
    df_qzl = rate5(df_data, '百万人口确诊率', '百万人口确诊率')
    # print(df_qzl)
    df_qzl = df_qzl[df_qzl['国家'] == '全球'].append(df_qzl[df_qzl['国家'] != '全球'].sort_values(['确诊率'], ascending=False))[
        ['国家', '确诊率']].reset_index(drop = True)
    df_qzl.replace('全球', '各国平均', inplace = True)
    df_qzl.to_csv(path + '2-8.csv', index = False, encoding = 'utf-8')

    # 2-9 病死率--累计死亡/累计确诊
    df_bsl = rate5(df_data, '累计死亡', '累计确诊')
    df_bsl = df_bsl[df_bsl['国家'] == '全球'].append(df_bsl[df_bsl['国家'] != '全球'].sort_values(['病死率'], ascending = False))[
        ['国家', '病死率']].reset_index(drop = True)
    df_bsl.replace('全球', '各国平均', inplace = True)
    df_bsl.to_csv(path + '2-9.csv', index = False, encoding = 'utf-8')

    # 2-10 治愈率
    df_zyl = rate5(df_data, '累计确诊', '累计治愈')
    df_zyl = df_zyl[df_zyl['国家'] == '全球'].append(df_zyl[df_zyl['国家'] != '全球'].sort_values(['治愈率'], ascending = False))[
        ['国家', '治愈率']].reset_index(drop = True)
    df_zyl.replace('全球', '各国平均', inplace = True)
    df_zyl.to_csv(path + '2-10.csv', index = False, encoding = 'utf-8')

    # 2-11 检测率---/1000000算,各国平均根据所有国家求和计算
    df_jcl = rate5(df_data, '百万人口检测率', '百万人口检测率')
    jcl_word = pd.DataFrame({'国家': '各国平均',
                             '检测率': (df_jcl['总检测数'].astype(float).sum() / df_jcl['2018人口'].astype(float).sum())},
                            index=[0])
    # print(jcl_word)
    df_jcl = jcl_word.append(
        df_jcl[df_jcl['国家'] != '全球'].sort_values(['检测率'], ascending = False)[['国家', '检测率']]).reset_index(drop = True)
    df_jcl.to_csv(path + '2-11.csv', index = False, encoding = 'utf-8')

    # 2-12 阳性率---累计确诊/总检测数，各国平均根据所有国家求和计算
    df_yxl = rate5(df_data, '累计确诊', '总检测数')
    yxl_word = pd.DataFrame({'国家': '各国平均',
                             '阳性率': (df_yxl['累计确诊'].astype(float).sum() / df_yxl['总检测数'].astype(float).sum())},
                            index=[0])
    # print(yxl_word)
    df_yxl = yxl_word.append(
        df_yxl[df_yxl['国家'] != '全球'].sort_values(['阳性率'], ascending = False)[['国家', '阳性率']]).reset_index(drop = True)
    df_yxl.to_csv(path + '2-12.csv', index = False, encoding = 'utf-8')

    # 2-13 新增死亡人数-全球7日
    data_wld_new = df_data[df_data['国家地区'] == '全球']
    data_wld_new = data_wld_new[(data_wld_new['日期'] >= this_monday) & (data_wld_new['日期'] <= this_sunday)]
    data_wld_new = data_wld_new.rename(columns={'新增确诊': '新增确诊人数', '新增死亡': '新增病死人数'})
    data_wld_new = data_wld_new[['日期', '新增确诊人数', '新增病死人数']].reset_index(drop = True)
    data_wld_new[['日期', '新增确诊人数']].to_csv(path + '2-13-a.csv', index = False, encoding = 'utf-8')
    data_wld_new[['日期', '新增病死人数']].to_csv(path + '2-13-b.csv', index = False, encoding = 'utf-8')

    # 2-14 本周新增确诊人数，前15名
    wld_confirmed_new = df_data[df_data['国家地区'] == '全球']
    wld_confirmed_new = wld_confirmed_new[
        (wld_confirmed_new['日期'] >= this_monday) & (wld_confirmed_new['日期'] <= this_sunday)]
    wld_confirmed_new = wld_confirmed_new[['国家地区', '新增确诊']]
    wld_confirmed_new1 = wld_confirmed_new.groupby(by = ['国家地区'])['新增确诊'].sum().reset_index(name = '本周新增确诊人数')
    # print(wld_confirmed_new1)
    data_confirmed_new = df_data[df_data['国家地区'] != '全球']
    data_confirmed_new = data_confirmed_new[
        (data_confirmed_new['日期'] >= this_monday) & (data_confirmed_new['日期'] <= this_sunday)]
    data_confirmed_new = data_confirmed_new[['国家地区', '新增确诊']]
    data_confirmed_new = data_confirmed_new[data_confirmed_new['新增确诊'].notna()]
    data_confirmed_new1 = data_confirmed_new.groupby(by = ['国家地区'])['新增确诊'].sum().reset_index(name = '本周新增确诊人数')
    data_confirmed_new1 = data_confirmed_new1.rename(columns = {'国家地区': '国家'})
    data_confirmed_new1 = data_confirmed_new1.sort_values(['本周新增确诊人数'], ascending = False).reset_index(drop = True)[
                          0:15]  # 降序，重新编写index，取前15
    # 创建一个其他的DataFrame
    data = {'国家': '其他',
            '本周新增确诊人数': wld_confirmed_new1['本周新增确诊人数'] - data_confirmed_new1['本周新增确诊人数'].sum()}
    df = pd.DataFrame(data, index = [0])
    # print(df)
    data_confirmed_new1_result = data_confirmed_new1.append(df).reset_index(drop = True)  # 合并到一张表中
    data_confirmed_new1_result.to_csv(path + '2-14.csv', index = False, encoding = 'utf-8')

    # 2-15 本周新增死亡人数，前15名
    wld_death_new = df_data[df_data['国家地区'] == '全球']
    wld_death_new = wld_death_new[(wld_death_new['日期'] >= this_monday) & (wld_death_new['日期'] <= this_sunday)]
    wld_death_new = wld_death_new[['国家地区', '新增死亡']]
    wld_death_new1 = wld_death_new.groupby(by=['国家地区'])['新增死亡'].sum().reset_index(name = '本周新增病死人数')
    # print(wld_death_new1)
    data_death_new = df_data[df_data['国家地区'] != '全球']
    data_death_new = data_death_new[(data_death_new['日期'] >= this_monday) & (data_death_new['日期'] <= this_sunday)]
    data_death_new = data_death_new[['国家地区', '新增死亡']]
    data_death_new = data_death_new[data_death_new['新增死亡'].notna()]
    data_death_new1 = data_death_new.groupby(by = ['国家地区'])['新增死亡'].sum().reset_index(name = '本周新增病死人数')
    data_death_new1 = data_death_new1.rename(columns = {'国家地区': '国家'})
    data_death_new1 = data_death_new1.sort_values(['本周新增病死人数'], ascending = False).reset_index(drop = True)[
                      0:15]  # 降序，重新编写index，取前15
    # print(data_death_new1)
    # 创建一个其他的DataFrame
    data = {'国家': '其他',
            '本周新增病死人数': wld_death_new1['本周新增病死人数'] - data_death_new1['本周新增病死人数'].sum()}
    df = pd.DataFrame(data, index = [0])
    # print(df)
    data_death_new1_result = data_death_new1.append(df).reset_index(drop = True)  # 合并到一张表中
    data_death_new1_result.to_csv(path + '2-15.csv', index = False, encoding = 'utf-8')

    # 定义增速函数
    def growth_rate(df, column):
        df = df.rename(columns = {'新增死亡': '新增病死'})
        df = df[df[column].notna()]
        last_week_sum = df[(df['日期'] >= last_monday) & (df['日期'] <= last_sunday)].groupby(by = ['国家地区'])[column].sum()
        this_week_sum = df[(df['日期'] >= this_monday) & (df['日期'] <= this_sunday)].groupby(by = ['国家地区'])[column].sum()
        rate = ((this_week_sum - last_week_sum) / last_week_sum).reset_index(name = '本周较上周' + column + '人数增速')
        data = pd.merge(rate, last_week_sum.reset_index(name = '上周新增'), how = 'left', on = '国家地区')
        data = pd.merge(data, this_week_sum.reset_index(name = '本周新增'), how = 'left', on = '国家地区')
        # print(data)
        lst = rate['本周较上周' + column + '人数增速'].values.tolist()
        rate_lst = []
        for i in lst:
            r = '%.0f' % (i * 100) + '%'
            rate_lst.append(r)
        data['本周较上周' + column + '人数增速' + '_%'] = rate_lst
        return data.sort_values(['本周较上周' + column + '人数增速'], ascending = False)

    # 2-16 本周较上周新增确诊人数增速，全部国家
    confirmed = df_data[-df_data.国家地区.isin(lst2)]  # 剔除累计确诊小于10000的国家
    confirmed = confirmed[-confirmed.国家地区.isin(lst5)]  # 剔除本周新增确诊少于500的国家
    confirmed_growth_rate = growth_rate(confirmed, '新增确诊')
    confirmed_growth_rate = confirmed_growth_rate[confirmed_growth_rate['国家地区'] == '全球'].append(confirmed_growth_rate \
                                                                                                    [
                                                                                                    confirmed_growth_rate[
                                                                                                        '国家地区'] != '全球']).reset_index(
        drop = True) \
        [['国家地区', '本周较上周新增确诊人数增速_%', '本周较上周新增确诊人数增速', '上周新增', '本周新增']]
    confirmed_growth_rate.replace('全球', '各国平均', inplace = True)
    confirmed_growth_rate = confirmed_growth_rate.rename(columns = {'国家地区': '国家'})
    confirmed_growth_rate[['国家', '本周较上周新增确诊人数增速']].to_csv(path + '2-16.csv', index = False, encoding = 'utf-8')

    # 2-17 本周较上周新增病死人数增速，全部国家
    death = df_data[-df_data.国家地区.isin(lst3)]  # 剔除累计死亡小于300的国家
    death = death[-death.国家地区.isin(lst6)]  # 剔除本周死亡小于100的国家
    death_growth_rate = growth_rate(death, '新增病死')
    death_growth_rate = death_growth_rate[death_growth_rate['国家地区'] == '全球'].append(death_growth_rate[death_growth_rate \
                                                                                                          [
                                                                                                          '国家地区'] != '全球']).reset_index(
        drop = True) \
        [['国家地区', '本周较上周新增病死人数增速_%', '本周较上周新增病死人数增速', '上周新增', '本周新增']]
    death_growth_rate.replace('全球', '各国平均', inplace = True)
    death_growth_rate = death_growth_rate.rename(columns = {'国家地区': '国家'})
    death_growth_rate[['国家', '本周较上周新增病死人数增速']].to_csv(path + '2-17.csv', index = False, encoding = 'utf-8')

    

    # part7: 附录
    # 2-18 累计检测数
    data_test_all = df_data[df_data['国家地区'] != '全球']
    data_test_all = data_test_all[-data_test_all.国家地区.isin(lst1)]  # 剔除累计确诊小于2000的国家
    data_test_all = data_test_all[data_test_all['日期'] == this_sunday]
    data_test_all = data_test_all[['国家地区', '总检测数']]
    data_test_all = data_test_all.rename(columns = {'国家地区': '国家', '总检测数': '累计检测数'})
    data_test_all = data_test_all[data_test_all['累计检测数'].notna()]
    data_test_all = data_test_all.sort_values(['累计检测数'], ascending = False).reset_index(drop = True)
    data_test_all.to_csv(path + '2-18.csv', index = False, encoding = 'utf-8')

    # 四大区域数据
    data = xlrd.open_workbook(four_area_data_file)
    sheet_names = data.sheet_names()
    sheet_names_use = ['全球', '非洲', '周边', '一带一路', '四个阶段分别合计', '四个阶段国家组成']
    name = [False for i in sheet_names_use if i not in sheet_names]
    if name:
        print('四大区域数据文件sheetname有改动！')
        return [False, '四大区域数据文件sheetname有改动！']
    else:
        pass

    def four_area_data(sheet_name):
        df = pd.read_excel(four_area_data_file, sheet_name=sheet_name)
        df.drop(0, inplace=True)
        df.columns = ['日期', '新增确诊（左）', '新增治愈（右）']
        df = df[df['日期'] <= end_date]
        if sheet_name == '全球':
            i = path + '2-19.csv'
        elif sheet_name == '一带一路':
            i = path + '2-20.csv'
        elif sheet_name == '非洲':
            i = path + '2-21.csv'
        elif sheet_name == '周边':
            i = path + '2-22.csv'
        df.to_csv(i, index = False, encoding = 'utf-8')

    four_area_data('全球')
    four_area_data('一带一路')
    four_area_data('非洲')
    four_area_data('周边')

    # 四个阶段数据
    df = pd.read_excel(four_area_data_file, sheet_name = '四个阶段分别合计')
    df.drop(0, inplace = True)
    col = df.columns.values
    # print(col)
    if len(col) % 3 == 0:
        pass
    else:
        print('四个阶段数据列数不正确！')
        return [False, '四个阶段数据列数不正确！']

    col_list = ['上行', '震荡', '下行', '尾期']
    name = [False for i in col_list if i not in col]
    if name:
        print('四个阶段数据标题有变动！')
        return [False, '四个阶段数据标题有变动！']
    else:
        pass

    for i in [0, 3, 6, 9]:
        j = i + 3
        df_select = df[col[i:j]]
        df_select.columns = ['日期', '新增确诊（左）', '新增治愈（右）']
        df_select = df_select[df_select['日期'] <= end_date]
        if '上行' in col[i:j]:
            df_select.to_csv(path + '2-23.csv', index = False, encoding = 'utf-8')
        elif '震荡' in col[i:j]:
            df_select.to_csv(path + '2-24.csv', index = False, encoding = 'utf-8')
        elif '下行' in col[i:j]:
            df_select.to_csv(path + '2-25.csv', index = False, encoding = 'utf-8')
        elif '尾期' in col[i:j]:
            df_select.to_csv(path + '2-26.csv', index = False, encoding = 'utf-8')

    ## part8: basic info
    basic_info_dic = {'开始日期': this_monday.date(),
                      '结束日期': this_sunday.date(),
                      '当前全球确诊数量': data_4(df_data, '全球累计确诊人数')[data_4(df_data, '全球累计确诊人数')['日期'] == this_sunday]\
                          ['全球累计确诊人数'].values[0],
                      '当前全球死亡数量': data_4(df_data, '全球累计病死人数')[data_4(df_data, '全球累计病死人数')['日期'] == this_sunday]\
                          ['全球累计病死人数'].values[0],
                      '当前全球确诊率': data_4(df_data, '全球确诊率')[data_4(df_data, '全球确诊率')['日期'] == this_sunday]\
                          ['全球确诊率'].values[0],
                      '当前全球病死率': data_4(df_data, '全球病死率')[data_4(df_data, '全球病死率')['日期'] == this_sunday]\
                          ['全球病死率'].values[0],
                      '当前全球确诊最多国家': data_confirmed_result.iloc[0, 0],
                      '当前全球确诊最多国家确诊数': data_confirmed_result.iloc[0, 1],
                      '当前全球确诊第二多国家': data_confirmed_result.iloc[1, 0],
                      '当前全球确诊第二多国家确诊数': data_confirmed_result.iloc[1, 1],
                      '当前全球死亡最多国家': data_death_result.iloc[0, 0],
                      '当前全球死亡最多国家死亡数': data_death_result.iloc[0, 1],
                      '当前全球死亡第二多国家': data_death_result.iloc[1, 0],
                      '当前全球死亡第二多国家死亡数': data_death_result.iloc[1, 1],
                      '上周全球确诊病例': data_wld_new['新增确诊人数'].sum(),
                      '上周全球确诊较前一周': confirmed_growth_rate.iloc[0, 2],
                      '上周全球死亡病例': data_wld_new['新增病死人数'].sum(),
                      '上周全球死亡较前一周': death_growth_rate.iloc[0, 2],
                      '上周确诊最多国家': data_confirmed_new1_result.iloc[0, 0],
                      '上周确诊最多国家确诊数': data_confirmed_new1_result.iloc[0, 1],
                      '上周确诊第二多国家': data_confirmed_new1_result.iloc[1, 0],
                      '上周确诊第二多国家确诊数': data_confirmed_new1_result.iloc[1, 1],
                      '上周死亡最多国家': data_death_new1_result.iloc[0, 0],
                      '上周死亡最多国家死亡数': data_death_new1_result.iloc[0, 1],
                      '上周死亡第二多国家': data_death_new1_result.iloc[1, 0],
                      '上周死亡第二多国家死亡数': data_death_new1_result.iloc[1, 1],
                      '上周确诊增速最快国家': confirmed_growth_rate.iloc[1, 0],
                      '上周确诊增速最快国家增速值': confirmed_growth_rate.iloc[1, 2],
                      '上周确诊增速第二快国家': confirmed_growth_rate.iloc[2, 0],
                      '上周确诊增速第二快国家增速值': confirmed_growth_rate.iloc[2, 2],
                      '上周死亡增速最快国家': death_growth_rate.iloc[1, 0],
                      '上周死亡增速最快国家增速值': death_growth_rate.iloc[1, 2],
                      '上周死亡增速第二快国家': death_growth_rate.iloc[2, 0],
                      '上周死亡增速第二快国家增速值': death_growth_rate.iloc[2, 2],
                      '当前全球确诊第三多国家': data_confirmed_result.iloc[2, 0],
                      '当前全球确诊第三多国家确诊数': data_confirmed_result.iloc[2, 1],
                      '所有疫情数据截止小时': time_data[time_data.rfind('H') - 1: time_data.rfind('H')],
                      '所有疫情数据截止分钟': time_data[time_data.rfind('H') + 1: time_data.rfind('.')]}
    name = list(basic_info_dic.keys())
    value = list(basic_info_dic.values())
    basic_info = pd.DataFrame({'name': name,
                               'value': value})
    basic_info.to_csv(path + 'basic_info.csv', index = False, encoding = 'utf-8')

    print('finished!\n', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return [True, [country_list, countries_error]]


if __name__ == '__main__':
    process_data("")
