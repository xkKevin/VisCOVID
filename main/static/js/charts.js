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
var case_scale = [0, 1000, 10000, 50000, 100000, 500000, 1000000, 2000000, 5000000];

function worldMap(data, name, div_id, num_max) {
    var myChart = echarts.init(document.getElementById(div_id));
    // console.log(d3.max(data.map((x)=>parseInt(x[name]))));
    let data_max = Math.pow(10, num_max.length - 1);
    if (num_max[0] >= '5'){
        data_max = 5*data_max;
    }

    let pieces = [];
    let color = CSS_STYLE.color9_red;

    if (name === "累计病死人数"){
        color = CSS_STYLE.color9_blue;
        for (let i = 0; i > -9; i--) {
            let min = pieces_map(data_max, i);
            let label_min = i > -8 ? min :0;
            pieces.push({
                min: label_min,
                max: pieces_map(min, 1),
                color: color[8 + i],
                label: String(label_min)
            })
        }
    }else {
        for (let i = 0; i < 9; i++) {
            pieces.push({
                min: case_scale[i],
                max: case_scale[i + 1],
                color: color[i],
                label: String(case_scale[i])
            })
        }
    }

    var option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        width: CSS_STYLE.map.width,
        // height: CSS_STYLE.bigChart.height,
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
        title: {
            text: name,
            textStyle: {
                fontSize: 17,
                fontFamily: "楷体",
                fontWeight: "bold"
            },
            left: '5px',
            bottom: '36px'
        },
        /* tooltip: {
             trigger: 'item',
             formatter: function (params) {
                 var value = (params.value + '').split('.');
                 value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,')
                         + '.' + value[1];
                 return params.seriesName + '<br/>' + params.name + ' : ' + value;
             }
         },*/
        // legend: {
        //     formatter: function (value) {
        //         return 'Legend ' + value;
        //     }
        // },
        visualMap: {
            // min: 0,
            // max: data_max, // 1000000,
            pieces: pieces,
            // pieces: [
            //     { min: 0, max: 10, color: '#FFF7E6', label: '10' },
            //     { min: 10, max: 50, color: '#FFE6BA', label: '50' },
            //     { min: 50, max: 100, color: '#FFD591', label: '100' },
            //     { min: 100, max: 500, color: '#FFC069', label: '500' },
            //     { min: 500, max: 1000, color: '#FF8206', label: '1000' },
            //     { min: 1000, max: 5000, color: '#FF6906', label: '5000' },
            //     { min: 5000, max: 100000, color: '#FA541C', label: '100000' },
            //     { min: 100000, max: 500000, color: '#D4380D', label: '500000' },
            //     { min: data_max, max: pieces_map(), color: '#AD2101', label: '1000000' }
            // ],
            orient: 'horizontal',
            bottom: 10,
            left: '5px',
            itemGap: 10,
            textStyle: {
                color: '#000',
                'fontSize': 15
            }
        },
        series: [{
            name: name,
            type: 'map',
            mapType: 'world',
            roam: true,
            
            top: "15px",
            
            itemStyle: {
                emphasis: {
                    label: {
                        show: true
                    }
                }
            },
            
            data: data.map(function (x) {
                return {"name": x["国家"], "value": x[name]}
            })
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
    // $.post('/saveImage/',{'baseimg': picInfo,'name': div_id},function (result, statue) {
    //    console.log(result);
    // });
}

function pieChart(data, name, div_id) {
    // var myChart = echarts.init(document.getElementById(div_id), null, {renderer: 'svg'});  // 使用svg渲染
    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        width: CSS_STYLE.pieChart.width,
        height: CSS_STYLE.pieChart.height,
        toolbox: {
            feature: {
                dataView: {
                    readOnly: false,
                    optionToContent: function(opt) {
                        // console.log(opt);
                        let data_len = opt.series[0].data.length;
                        var table = `<h5>表格数据</h5>
                        <textarea rows='${data_len+1}' style="width: 100%">国家,${opt.series[0].name}`;
                        for (let i =0;i<data_len;i++){
                            table += "\n" + opt.series[0].data[i].name + "," + opt.series[0].data[i].value;
                        }
                        table += `</textarea><h5>系统配置</h5>
                                radius: <input type="text" value="${opt.series[0].radius}">（圆半径相对于整个图的大小）<br>
                                center: <input type="text" value="${opt.series[0].center}" class="last">（圆心在图中的位置(x,y)）`;
                        return table
                    },
                    contentToOption: function(html, opt) {
                        let content = $(html).children("textarea").val().split("\n");
                        let handle_data = [];
                        content.slice(1).forEach(function(x, index){
                            let data = x.split(',');
                            handle_data.push({
                                name: data[0],
                                value: data[1]
                            })
                         });
                        opt.series[0].data = handle_data;
                        let inputs = $(html).children("input");
                        opt.series[0].radius = inputs.eq(0).val();
                        opt.series[0].center = inputs.eq(1).val().split(",");
                        myChart.clear(); // 清空当前绘制的图形，要不然只会数据更新，样式不更新
                        return opt;
                    }
                },
                // restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        // title:{
        //     text: name,
        //     top: '15%',
        //     left: '',
        //     textStyle:{
        //         fontSize: 28
        //     }
        // },
        color: CSS_STYLE.color11,
        backgroundColor: CSS_STYLE.backgroundColor,

        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        series: [{
            name: name,
            type: 'pie',
            radius: CSS_STYLE.pieChart.radius,
            center: CSS_STYLE.pieChart.center,
            animationType: 'scale',  // 缩放效果，解决边框问题
            animation: false,
            data: data.map(function (x) {
                return {"name": x["国家"], "value": x[name]}
            }),
            clockwise: false, // 逆时针排序
            label: {
                formatter: function(a, b, c, d) {
                    return a.data.name + ` : {num|${parseInt(a.data.value)}}` + ' | ' + `{rate|${a.percent.toFixed(1)}%}`
                },
                // "{b} : {num|{c}} | {rate|{d.toFixed()}} {symbol|%}",
                color: "black",
                fontSize: CSS_STYLE.pieChart.fontSizeText,
                rich: {
                    num: {
                        fontSize: CSS_STYLE.pieChart.fontSizeNum,
                        fontWeight: 'bold',
                        color: "black"
                    },
                    rate: {
                        fontSize: CSS_STYLE.pieChart.fontSizeNum,
                        fontWeight: 'bold',
                        color: CSS_STYLE.color3[0]
                    },
                    symbol: {
                        fontSize: CSS_STYLE.pieChart.fontSizeNum,
                        color: "black"
                    }
                }
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function barchart(data, name, div_id) {
    data = data.map((x)=> [x["国家"],x[name]]);
    let format_min = format_percent(data[20][1]);
    let format_fixed_num = format_min.length - format_min.indexOf('.') - 2;
    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.bigChart.width,  // 如果设置了 width，就不能使用grid.right
        // width: "750px",
        height: CSS_STYLE.bigChart.width,
        toolbox: {
            feature: {
                dataView: {
                    readOnly: false,
                    optionToContent: function(opt) {
                        // console.log(opt);
                        let xAxis_max = opt.xAxis[0].max ? opt.xAxis[0].max : "";
                        let xAxis_interval = opt.xAxis[0].interval ? opt.xAxis[0].interval : "";
                        let data_len = opt.series[0].data.length;
                        var table = `<h5>表格数据</h5>
                        <textarea rows='${data_len+1}' style="width: 100%">国家,${opt.series[0].name}`;
                        for (let i =0;i<data_len;i++){
                            table += "\n" + opt.yAxis[0].data[i] + "," + opt.series[0].data[i];
                        }
                        table += `</textarea><h5>系统配置</h5>
                                max: <input type="text" value="${xAxis_max}"><br>
                                interval: <input type="text" value="${xAxis_interval}" class="last">`;
                        return table
                    },
                    contentToOption: function(html, opt) {
                        let content = $(html).children("textarea").val().split("\n");
                        let handle_data = {data:[],yAxis:[]};
                        content.slice(1).forEach(function(x, index){
                            let data = x.split(',');
                            handle_data.yAxis.push(data[0]);
                            handle_data.data.push(data[1]);
                         });
                         opt.series[0].data = handle_data.data;
                         opt.yAxis[0].data = handle_data.yAxis;
                        let inputs = $(html).children("input");
                        if (inputs.eq(0).val()){
                            opt.xAxis[0].max = parseFloat(inputs.eq(0).val());
                        }
                        if (inputs.eq(1).val()){
                            opt.xAxis[0].interval = parseFloat(inputs.eq(1).val());
                        }
                        myChart.clear(); // 清空当前绘制的图形，要不然只会数据更新，样式不更新
                        return opt;
                    }
                },
                // restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        title: {
            text: name,
            textStyle: CSS_STYLE.nameTextStyle,
            right: '3%',
            top: 10
        },
        color: CSS_STYLE.color3[2],
        tooltip: {
            // trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%', // 设置图形离上下左右的距离
            right: '6%',
            bottom: '3%',
            containLabel: true
        },
        yAxis: {
            type: 'category',
            data: data.map((x) => x[0]),
            axisTick: {
                alignWithLabel: true
            },
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            inverse: true // inverse了之后就不需要对data做reverse了
        },
        xAxis: {
            type: 'value',
            position: 'top',
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
                    formatter: function(param) {
                        let x1 = param * 1000 / 10 + "%";
                        let x2 = param * 100000 / 1000 + "%";  // 0.009 会出现精度丢失的情况
                        return x1.length <= x2.length ? x1 : x2;
                }
            }
        },
        series: [{
            name: name,
            type: 'bar',
            barWidth: 28,
            label: {
                show: true,
                position: 'right',
                formatter: function(param) {
                    if (param.dataIndex === 0){
                        return format_percent(param.value);
                    }
                    return (param.value * 100).toFixed(format_fixed_num) + "%";  // // toFixed 保留多少位小数
                },
                color: 'black',
                fontSize: CSS_STYLE.fontSize.small
            },
            data: data.map((x) =>  x[1]),
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function barchart_num(data, name, div_id, span) {
    data = data.map((x)=> [x["国家"],x[name]]);
    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.bigChart.width,  // 如果设置了 width，就不能使用grid.right
        // width: "750px",
        height: CSS_STYLE.bigChart.width,
        toolbox: {
            feature: {
                dataView: {
                    readOnly: false,
                    optionToContent: function(opt) {
                        // console.log(opt);
                        let xAxis_max = opt.xAxis[0].max ? opt.xAxis[0].max : "";
                        let xAxis_interval = opt.xAxis[0].interval ? opt.xAxis[0].interval : "";
                        let data_len = opt.series[0].data.length;
                        var table = `<h5>表格数据</h5>
                        <textarea rows='${data_len+1}' style="width: 100%">国家,${opt.series[0].name}`;
                        for (let i =0;i<data_len;i++){
                            table += "\n" + opt.yAxis[0].data[i] + "," + opt.series[0].data[i];
                        }
                        table += `</textarea><h5>系统配置</h5>
                                max: <input type="text" value="${xAxis_max}"><br>
                                interval: <input type="text" value="${xAxis_interval}" class="last">`;
                        return table
                    },
                    contentToOption: function(html, opt) {
                        let content = $(html).children("textarea").val().split("\n");
                        let handle_data = {data:[],yAxis:[]};
                        content.slice(1).forEach(function(x, index){
                            let data = x.split(',');
                            handle_data.yAxis.push(data[0]);
                            handle_data.data.push(data[1]);
                         });
                         opt.series[0].data = handle_data.data;
                         opt.yAxis[0].data = handle_data.yAxis;
                        let inputs = $(html).children("input");
                        if (inputs.eq(0).val()){
                            opt.xAxis[0].max = parseFloat(inputs.eq(0).val());
                        }
                        if (inputs.eq(1).val()){
                            opt.xAxis[0].interval = parseFloat(inputs.eq(1).val());
                        }
                        myChart.clear(); // 清空当前绘制的图形，要不然只会数据更新，样式不更新
                        return opt;
                    }
                },
                // restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        title: {
            text: name,
            textStyle: CSS_STYLE.nameTextStyle,
            right: '0%',
            top: 10
        },
        color: CSS_STYLE.color3[2],
        tooltip: {
            // trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%', // 设置图形离上下左右的距离
            right: '8%',
            bottom: '3%',
            containLabel: true
        },
        yAxis: {
            type: 'category',
            data: data.map((x) => x[0]),
            axisTick: {
                alignWithLabel: true
            },
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            inverse: true // inverse了之后就不需要对data做reverse了
        },
        xAxis: {
            type: 'value',
            position: 'top',
            max: span[0], // 16000000,
            interval: span[1], // 4000000,
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
                // formatter: function(param) {
                //     return format_number(param)
                // }
            }
        },
        series: [{
            name: name,
            type: 'bar',
            barWidth: 28,
            label: {
                show: true,
                position: 'right',
                formatter: function(param) {
                    // 如果保留两位有效数字之后是个整数，则再保留一位小数
                    // let display = (param.value * 100).toPrecision(2); // toPrecision 保留多少位有效数字
                    // if (display.includes(".")){
                    //     return display + "%";
                    // }
                    return format_number(param.value);  // // toFixed 保留多少位小数
                },
                color: 'black',
                fontSize: CSS_STYLE.fontSize.small
            },
            data: data.map((x) => x[1]),
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function linechart(data, div_id) {

    let handle_data = {
        "week": [],
        "cases": [],
        "deaths": []
    };
    data.forEach(function (x) {
        let date = new Date(x["日期"]);
        handle_data.week.push(String(date.getMonth()+1)+'/'+String(date.getDate()));
        handle_data.cases.push(x["新增确诊人数"]);
        handle_data.deaths.push(x["新增病死人数"]);
    });

    let name = {
        "save": "全球过去一周每日新增确诊人数和病死人数",
        "yAxis": "人数"
    };

    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.bigChart.width,
        // height: CSS_STYLE.bigChart.height,
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
        legend: {
            textStyle: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            data: ["新增确诊人数", "新增病死人数"],
            icon: "rect",
            itemGap: 80,
            top: 5
        },
        grid: {
            // bottom: '11%',
            top: 80,
            left: 110,
            // right: 150
        },
        xAxis: {
            type: 'category',
            data: handle_data.week,
            //   boundaryGap: false,
            axisTick: {
                alignWithLabel: true
            },
            name: "日期",
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            nameTextStyle: {
                align: "left",
                fontSize: 28,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [33, 0, 0, -15]
            }
        },
        yAxis: {
            type: 'value',
            name: name.yAxis,
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.median,
            },
            nameTextStyle: {
                //   align: "left",
                fontSize: 28,
                fontFamily: "楷体",
                fontWeight: "bold",
                // verticalAlign:"top",
                // padding: [0,220,0,0]

            },
            nameRotate: 0,
            // nameLocation:"middle",
            // position: "right",
            //   nameGap: 88
            // type: 'log',
            // logBase: 2
            // //min: 500
        },
        series: [{
            name: "新增确诊人数",
            data: handle_data.cases,
            type: 'line',
            symbol: 'circle',
            symbolSize: CSS_STYLE.symbolSize,
            lineStyle: CSS_STYLE.lineStyle,
            smooth: true,
            animation: false,
            color: CSS_STYLE.color3[2],
        }, {
            name: "新增病死人数",
            data: handle_data.deaths,
            symbol: 'circle',
            symbolSize: CSS_STYLE.symbolSize,
            lineStyle: CSS_STYLE.lineStyle,
            type: 'line',
            smooth: true,
            animation: false,
            color: CSS_STYLE.color3[0],
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function bi_directional_barchart(data, name, div_id) {
    let num = 0;
    let handle_data = [];
    let countries = [];
    data.forEach(function(x, index){
        if (index === 0){
            num++;
            countries.push(x["国家"]);
            if (x[name] >= 0){
                handle_data.push({
                    'label': {'position': 'left'},
                    'value': x[name],
                    'itemStyle': {'color': CSS_STYLE.color3[0]},
                 });
            }else{
                handle_data.push({
                    'label': {'position': 'right'},
                    'value': x[name],
                    'itemStyle': {'color': CSS_STYLE.color3[1]},
                 });
            }
        }else if (x[name] >= 0.2){
             num++;
             handle_data.push({
                'label': {'position': 'left'},
                'value': x[name],
                'itemStyle': {'color': CSS_STYLE.color3[0]},
             });
             countries.push(x["国家"]);
         }else if (x[name] <= -0.2){
             num++;
             handle_data.push({
                'label': {'position': 'right'},
                'value': x[name],
                'itemStyle': {'color': CSS_STYLE.color3[1]},
             });
             countries.push(x["国家"]);
         }
     });
    // console.log(values);

    $('#'+div_id).css("height",(30*num+95)+"px");

    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.bigChart.width,
        // height: CSS_STYLE.bigChart.heightLong,
        toolbox: {
            feature: {
                dataView: {
                    readOnly: false,
                    optionToContent: function(opt) {
                        var axisData = opt.xAxis[0].data;
                        var series = opt.series;
                        let data_len = opt.yAxis[0].data.length;
                        // console.log(opt);
                        var table = `<h5>表格数据</h5>
                        <textarea rows='${data_len+1}' style="width: 100%">国家,${opt.series[0].name}`;
                        for (let i =0;i<data_len;i++){
                            table += "\n" + opt.yAxis[0].data[i] + "," + opt.series[0].data[i].value;
                        }
                        table += "</textarea>";
                        return table
                    },
                    contentToOption: function(html, opt) {
                        let content = $(html).children("textarea").val().split("\n");
                        let handle_data = [];
                        let countries = [];
                        content.slice(1).forEach(function(x, index){
                            let country = x.split(',')[0];
                            let value = parseFloat(x.split(',')[1]);
                            if (index === 0){
                                countries.push(country);
                                if (value >= 0){
                                    handle_data.push({
                                        'label': {'position': 'left'},
                                        value,
                                        'itemStyle': {'color': CSS_STYLE.color3[0]},
                                     });
                                }else{
                                    handle_data.push({
                                        'label': {'position': 'right'},
                                        value,
                                        'itemStyle': {'color': CSS_STYLE.color3[1]},
                                     });
                                }
                            }else if (value >= 0.2){
                                 handle_data.push({
                                    'label': {'position': 'left'},
                                    value,
                                    'itemStyle': {'color': CSS_STYLE.color3[0]},
                                 });
                                 countries.push(country);
                             }else if (value <= -0.2){
                                 handle_data.push({
                                    'label': {'position': 'right'},
                                    value,
                                    'itemStyle': {'color': CSS_STYLE.color3[1]},
                                 });
                                 countries.push(country);
                             }
                         });
                         opt.series[0].data = handle_data;
                         opt.yAxis[0].data = countries;
                        // console.log(opt);
                        myChart.clear(); // 清空当前绘制的图形，要不然只会数据更新，样式不更新
                        return opt;
                    }
                },
                // restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        title: {
            text: name,
            textStyle: CSS_STYLE.nameTextStyle,
            right: "2%",
            top: 10
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: 150,
            top: 85,
            bottom: 10,
            right: "5%"
        },
        xAxis: {
            type: 'value',
            position: 'top',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small,
                formatter: function(param) {
                    return param * 100 + "%"
                }
            }
        },
        yAxis: {
            type: 'category',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            data: countries,
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small + 1
            },
            inverse: true
        },
        series: [{
            name: '增速',
            type: 'bar',
            // color: '#6EA748',
            label: {
                show: true,
                formatter: (param) => (Math.round(param.value * 100) + "%").padStart(4, " "), //.toFixed(2),
                color: '#000',
                fontSize: CSS_STYLE.fontSize.small - 1
                // position: 'top'
            },
            barWidth: 23,
            data: handle_data,
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
    return countries.length;  // 返回有多少个国家数量（包括“各国平均”）
}

function linechart_num(data, div_id) {
    let handle_data = {value:[], date:[]};
    data.forEach(function (x) {
        let date = new Date(x[data.columns[0]]);
        // handle_data.date.push(date);
        handle_data.date.push(String(date.getMonth()+1)+'/'+String(date.getDate()));
        handle_data.value.push(x[data.columns[1]]);
    });

    let handle_data_len = handle_data.value.length;
    let max_data_value = handle_data.value[handle_data_len-1];
    let precision_len = format_number(max_data_value).length;
    if (max_data_value > 8000000){
        precision_len = 10;
    }else if (max_data_value > 800000){
        precision_len = 9;
    }
    console.log(div_id, precision_len, max_data_value);

    var myChart = echarts.init(document.getElementById(div_id));

    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.smallChart.width,
        // height: CSS_STYLE.smallChart.height,
        toolbox: {
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        xAxis: {
            type: 'category',
            data: handle_data.date,
            axisTick: {
                alignWithLabel: true
            },
            name: "日期",
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-4,
                showMaxLabel: true,
                showMinLabel: true,
                // splitNumber: 3
                interval: Math.round((handle_data_len)/5)-1,
            },
            nameTextStyle: {
                align: "left",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [28, 0, 0, 6]
            }
        },
        grid: {
            bottom: '11%',
            top: 45,
            left: 33+5*precision_len,
            right: 65
        },
        tooltip:{ trigger: 'axis'},
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
            name: "人数",
            nameTextStyle: {
                align: "center",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [0, 0, 2, 18]
            }
        },
        series: [{
            name: "人数",
            data: handle_data.value,
            type: 'line',
            lineStyle: CSS_STYLE.lineStyle,
            symbol: 'none',
            symbolSize: CSS_STYLE.symbolSize,
            smooth: true,
            color: CSS_STYLE.color3[0],
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function linechart_num_week(data, div_id) {
    let handle_data = {value:[], date:[]};
    data.forEach(function (x) {
        let date = new Date(x[data.columns[0]]);
        // handle_data.date.push(date);
        handle_data.date.push(String(date.getMonth()+1)+'/'+String(date.getDate()));
        handle_data.value.push(x[data.columns[1]]);
    });

    let handle_data_len = handle_data.value.length;
    let precision_len = format_number(handle_data.value[handle_data_len-1]).length;

    var myChart = echarts.init(document.getElementById(div_id));

    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.smallChart.width,
        // height: CSS_STYLE.smallChart.height,
        toolbox: {
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        xAxis: {
            type: 'category',
            data: handle_data.date,
            axisTick: {
                alignWithLabel: true
            },
            name: "日期",
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-4,
                showMaxLabel: true,
                showMinLabel: false,
                // splitNumber: 3
                interval: Math.round((handle_data_len)/6)-1,
            },
            nameTextStyle: {
                align: "left",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [28, 0, 0, -12]   // 上右下左
            }
        },
        grid: {
            bottom: '11%',
            top: 45,
            left: 33+5*precision_len,
            right: 47
        },
        tooltip:{ trigger: 'axis'},
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
            name: "人数",
            nameTextStyle: {
                align: "center",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [0, 0, 2, 18]
            }
        },
        series: [{
            name: "人数",
            data: handle_data.value,
            type: 'line',
            lineStyle: CSS_STYLE.lineStyle,
            symbol: 'none',
            symbolSize: CSS_STYLE.symbolSize,
            smooth: true,
            color: CSS_STYLE.color3[0],
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function linechart_rate(data, div_id) {
    let handle_data = {value:[], date:[]};
    data.forEach(function (x) {
        let date = new Date(x[data.columns[0]]);
        // handle_data.date.push(date);
        handle_data.date.push(String(date.getMonth()+1)+'/'+String(date.getDate()));
        handle_data.value.push(x[data.columns[1]]);
    });

    let handle_data_len = handle_data.value.length;
    let precision_len = div_id.includes('a') ? 4 : 1;
    // let precision_len = (handle_data.value[handle_data_len-1]*100).toPrecision(1).length;
    // console.log(handle_data_len);

    var myChart = echarts.init(document.getElementById(div_id));

    let option = {
        backgroundColor: CSS_STYLE.backgroundColor,
        // width: CSS_STYLE.smallChart.width,
        // height: CSS_STYLE.smallChart.height,
        toolbox: {
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        tooltip:{ trigger: 'axis'},
        xAxis: {
            type: 'category',
            data: handle_data.date,
            axisTick: {
                alignWithLabel: true
            },
            name: "日期",
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-4,
                showMaxLabel: true,
                showMinLabel: true,
                // splitNumber: 3
                interval: Math.round((handle_data_len)/5)-1,
            },
            nameTextStyle: {
                align: "left",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [28, 0, 0, 6]
            }
        },
        grid: {
            bottom: '11%',
            top: 45,
            left: 35+6*precision_len,
            right: 65
        },
        yAxis: {
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-4,
                formatter: function(value) {
                    if (precision_len>1){
                        return (value*100).toFixed(precision_len-2) + '%'; // 用从长度减去2（即0.）
                    }
                    return (value*100).toFixed(0) + '%'
                }
            },
            type: 'value',
            name: data.columns[1].slice(2),
            nameTextStyle: {
                align: "center",
                fontSize: CSS_STYLE.fontSize.median-1,
                fontFamily: "楷体",
                fontWeight: "bold",
                padding: [0, 0, 2, 18]
            }
        },
        series: [{
            name: data.columns[1].slice(2),
            data: handle_data.value,
            type: 'line',
            lineStyle: CSS_STYLE.lineStyle,
            symbol: 'none',
            symbolSize: CSS_STYLE.symbolSize,
            smooth: true,
            color: CSS_STYLE.color3[0],
            animation: false,
        }]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}

function bi_yAxis_barchart(data, name, div_id, span) {
    data = data.map((x)=> [x["日期"],x["新增确诊（左）"],x["新增治愈（右）"]]);
    let x_data = data.map(function(x) {
       let date = new Date(x[0]);
       return String(date.getMonth()+1)+'/'+String(date.getDate());
    });
    var myChart = echarts.init(document.getElementById(div_id));
    let option = {
        title: {
            text: name,
            left: 'center',
            textStyle: {
                color: CSS_STYLE.color3[0],
                fontSize: 26,
                fontWeight: "bold"
            }
        },
        toolbox: {
            feature: {
                dataView: {
                    readOnly: false,
                    optionToContent: function(opt) {
                        // console.log(opt.title);
                        let data_len = opt.series[0].data.length;
                        var table = `<h5>表格数据</h5>
                        <textarea rows='${data_len+1}' style="width: 100%">日期,${opt.series[0].name},${opt.series[1].name}`;
                        for (let i =0;i<data_len;i++){
                            table += "\n" + opt.xAxis[0].data[i] + "," + opt.series[0].data[i] + "," + opt.series[1].data[i];
                        }
                        table += `</textarea><h5>系统配置</h5>
                                title: <input type="text" value="${opt.title[0].text}" style="width: 60%"><br>
                                left max: <input type="text" value="${opt.yAxis[0].max}"><br>
                                right max: <input type="text" value="${opt.yAxis[1].max}"><br>
                                interval: <input type="text" value="${opt.yAxis[0].interval}" class="last">`;
                        return table
                    },
                    contentToOption: function(html, opt) {
                        let content = $(html).children("textarea").val().split("\n");
                        let handle_data = {data:[[],[]],xAxis:[]};
                        content.slice(1).forEach(function(x, index){
                            let data = x.split(',');
                            handle_data.xAxis.push(data[0]);
                            handle_data.data[0].push(data[1]);
                            handle_data.data[1].push(data[2]);
                         });
                         opt.series[0].data = handle_data.data[0];
                         opt.series[1].data = handle_data.data[1];
                         opt.xAxis[0].data = handle_data.xAxis;
                        let inputs = $(html).children("input");
                        opt.title[0].text = inputs.eq(0).val();
                        opt.yAxis[0].max = parseFloat(inputs.eq(1).val());
                        opt.yAxis[1].max = parseFloat(inputs.eq(2).val());
                        opt.yAxis[0].min = -opt.yAxis[1].max;
                        opt.yAxis[1].min = -opt.yAxis[0].max;
                        opt.yAxis[0].interval = opt.yAxis[1].interval = parseFloat(inputs.eq(3).val());
                        myChart.clear(); // 清空当前绘制的图形，要不然只会数据更新，样式不更新
                        return opt;
                    }
                },
                // restore: {},
                saveAsImage: {
                    name: div_id
                }
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function(param){
                return param[0].name +"<br>" + param[0].marker + param[0].seriesName + ": " + param[0].value
                        + "<br>" + param[1].marker + param[1].seriesName + ": " + (param[1].value);
            }
        },
        legend:{
            itemGap: 120,
            top: 43,
            textStyle: {
                fontSize: CSS_STYLE.fontSize.small,
            },
        },
        grid: {
            top: 95,
            bottom: 46,
            left: 92,
            right: 92
        },
        yAxis: [{
            type: 'value',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            axisLine: {show: false},
            axisTick: {show: false},
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-2,
            },
            max:span[0],
            min:-span[1],
            interval: span[2]
        },{
            type: 'value',
            position: 'right',
            inverse: true,
            axisLine: {show: false},
            axisTick: {show: false},
            axisLabel: {
                fontSize: CSS_STYLE.fontSize.small-2,
                
            },
            max:span[1],
            min:-span[0],
            interval: span[2]
        }],
        xAxis: [{
            type: 'category',
            axisLine: {onZero: false},
            axisTick: {alignWithLabel: true},
            axisLabel: {
                // rotate: 90,
                // showMaxLabel: true,
                margin: 17, // default: 8 label与x轴刻度的距离
                fontSize: CSS_STYLE.fontSize.small-3,
                showMaxLabel: true,
                showMinLabel: true,
                // align: "center",
                interval: 15


            },
            data: x_data,
        },{
            type: 'category',
            axisLine: {show: false},
            axisTick: {show: false},
            axisLabel: {show: false},
            data: x_data,
        }],
        series: [
            {
                yAxisIndex: 0,
                xAxisIndex: 0,
                name: '新增确诊（左）',
                // color: 'red',//CSS_STYLE.color3[0],
                type: 'bar',
                data: data.map((x) => x[1]),
                animation: false,
            },{
                yAxisIndex: 1,
                xAxisIndex: 1,
                // stack: 'new',
                name: '新增治愈（右）',
                color: 'green',//CSS_STYLE.color3[1],
                type: 'bar',
                data: data.map((x) => x[2]),
                animation: false,
            }
        ]
    };
    myChart.setOption(option);
    imagesInfo[div_id] = myChart.getDataURL({
        pixelRatio: 2,
        excludeComponents: ['toolbox'],
    });
}