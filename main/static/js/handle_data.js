function format_number(n) {
    var b = parseInt(n).toString();
    var len = b.length;
    if (len <= 3) { return b; }
    var r = len % 3;
    return r > 0 ? b.slice(0, r) + "," + b.slice(r, len).match(/\d{3}/g).join(",") : b.slice(r, len).match(/\d{3}/g).join(",");
}

function format_percent(f) {
    // 如果保留两位有效数字之后是个整数，则再保留一位小数
    let display = (f * 100).toPrecision(2); // toPrecision 保留多少位有效数字
    if (display.includes(".")){
        return display + "%";
    }
    return (f * 100).toFixed(1) + "%";  // // toFixed 保留多少位小数
}

function pieces_map(basedata, num) {
    /**
     * basedata: 基准数据；num：前进或后退的数量
     */
    let strdata = String(basedata);
    if (num < 0){
        for (let i = 0; i < Math.abs(num); i++) {
            if (strdata[0] === '5'){
                strdata = '1' + strdata.slice(1);
            }else{
                strdata = '5' + strdata.slice(2);
            }
        }
    }else{
        for (let i = 0; i < num; i++) {
            if (strdata[0] === '5'){
                strdata = '10' + strdata.slice(1);
            }else{
                strdata = '5' + strdata.slice(1);
            }
        }
    }
    return parseInt(strdata)
}