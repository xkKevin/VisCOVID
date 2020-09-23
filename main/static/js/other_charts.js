/*
    var myChart = echarts.init(document.getElementById(div_id));
    myChart.setOption(option);
 */
var CSS_STYLE = {
    'color11' :['#c23531', '#61a0a8', '#d48265','#749f83','#2f4554', '#91c7ae',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'],  // 11色，和echarts默认色系基本一致
    'color9_red': ['#FFF7E6', '#FFE6BA', '#FFD591','#FFC069','#FF8206','#FF6906','#FA541C','#D4380D','#AD2101'],
    'color9_blue': ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b'],
    'color3': ["#D4380D", "#6EA748", "#5d80b6"], // 红绿蓝
    'nameTextStyle': {
        align: "left",
        fontSize: 28,
        fontFamily:"楷体",
        fontWeight: "bold"
    },
    'fontSize': {
        small: 20,
        median: 22,
        large: 28
    },
    'lineStyle':{
        width:3
    },
    'backgroundColor': "white",
    "symbolSize": 7,
    // 长宽：0.618 （黄金分割比）,
    "map": {
       width: "850px",
        height: "495px",
        heightLong: "950px"
    },
    'bigChart':{
        width: "1800px",
        height: "495px",
        heightLong: "950px"
    },
    'smallChart':{
        width: "350px",
        height: "216px"
    },
    'pieChart':{
        width: "850px",
        height: "600px",
        radius: '50%',
        center: ['47%', '35%'],
        fontSizeText: 18,
        fontSizeNum: 20
    }
};


function stack_bar_chart(data, name, div_id) {
    var myChart = echarts.init(document.getElementById(div_id));
    let countries = [], stage_data=[];
    data.forEach((item)=>{
        countries.push(item["国家"]);
        stage_data.push({
            name: item["国家"],
            type: 'bar',
            stack: '总量',
            data: [item["阶段一"],item["阶段二"],item["阶段三"]]
        });
    });
    let option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            // position: ['50%', '0%'],  // 左右，上下
            position: function (point, params, dom, rect, size) {
                // 固定在顶部
                return [point[0], '0%'];
            }
        },
        toolbox: {
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        legend: {
            data: countries,
            left: 80,
            bottom: 6,
            textStyle: {
                fontSize: CSS_STYLE.fontSize.small -1 ,
            },
            // top: 'center',
            // orient: 'vertical'
        },
        color: ["#FFA65E", "#46A9A8", "#8177D8", "#65DCB8", "#F596C6", "#5EC6D7", "#CC69D9", "#EF7D52", "#FBC94B", "#5D7092", "#5ABF61", "#5ABF61", "#005730", "#00506F", "#465B7D", "#993C67"],
        grid: {
            left: '3%',
            right: '4%',
            bottom: 85,
            top: 56,
            containLabel: true
        },
        title: {
            text: name,
            textStyle: CSS_STYLE.nameTextStyle,
            right: '2%',
            top: 6
        },
        xAxis: {
            type: 'value',
            position: 'top',
            max: 1,
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
                    formatter: function(param) {
                        let x1 = param * 1000 / 10 + "%";
                        let x2 = param * 100000 / 1000 + "%";  // 0.009 会出现精度丢失的情况
                        return x1.length <= x2.length ? x1 : x2;
                }
            }
        },
        yAxis: {
            type: 'category',
            data: ['阶段一', '阶段二', '阶段三'],
            axisTick: {
                alignWithLabel: true
            },
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            inverse: true,
            zlevel: 1
        },
        // color: ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b'],
        series: stage_data
    };
    myChart.setOption(option);
}


function vertical_bar_chart(data, name, div_id) {
    let stage_data = data.map(item=>item[name]);
    let precision_len = Math.max.apply(null, stage_data).toString().length;
    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        toolbox: {
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        tooltip:{},
        color: CSS_STYLE.color3[2],
        grid: {
            bottom: '11%',
            top: 45,
            left: 26+8*precision_len,
            right: 10
        },
        xAxis: {
            type: 'category',
            data: ['阶段一', '阶段二', '阶段三'],
            axisTick: {
                alignWithLabel: true
            },
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small - 4
            }
        },
        yAxis: {
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-6,
                // formatter: function(value) {
                //     if (precision_len>1){
                //         return (value*100).toFixed(precision_len-2) + '%'; // 用从长度减去2（即0.）
                //     }
                //     return (value*100).toFixed(0) + '%'
                // }
            },
            type: 'value',
            name: name.slice(2),//"人数",
            nameTextStyle: {
                align: "center",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [0, 0, 2, 0]
            }
        },
        series: [{
            data: stage_data,
            type: 'bar',
            name: name,
            label: {
                show: true,
                position: 'top',
                formatter: function(param) {
                    return format_number(param.value, true);
                },
                color: 'black',
                fontSize: CSS_STYLE.fontSize.small-6
            },
            // barWidth: '58%'
        }]
    };
    myChart.setOption(option);
}