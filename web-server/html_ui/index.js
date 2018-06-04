////////////////////
//实时流量图 chart
////////////////////
var chart_status = false;
var mychart = echarts.init(document.getElementById('chart'), 'macarons');
var chart_option = {
    tooltip:{
        trigger:'axis',
        axisPointer: {
            type: 'cross'
        },
        formatter: '<div>入口流量{c0} Mbps</div> <div>出口流量{c1} Mbps</div> <div style="font-size:0.75em">{b0}</div>'
    },
    dataZoom:[
        {
            type:'inside',
            xAxisIndex: 0,
            start: 20,
            end: 100,
        }
    ],
    xAxis: {
        type: 'category',
        data: function(){
            var init_data = [];
            var time = getSecondScale();
            for(var i=0; i<15; i++){
                init_data.push(time);
            }
            return init_data;
        }()
    },
    yAxis: {},
    series: [
        {
            name:'Inspeed',
            type:'line',
            smooth:true,
            data:function(){
                var init_data = [];
                for(var i=0; i<15; i++){
                    init_data.push(0);
                }
                return init_data;
            }(),
            areaStyle: {
                normal: {}
            },
        },
        {
            name:'Outspeed',
            type:'line',
            smooth:true,
            data:function(){
                var init_data = [];
                for(var i=0; i<15; i++){
                    init_data.push(1);
                }
                return init_data;
            }(),
            areaStyle: {
                normal: {}
            },
        },

    ]

}; 
mychart.setOption(chart_option) 

function getSecondScale(){
    var date = new Date();
    var minute = date.getMinutes();
    minute = (minute < 10)? '0' + minute : minute;
    var second = date.getSeconds();
    second = (second < 10)? '0' + second : second;
    var time = minute + ':' + second;
    return time;
}

function getMonthScale(){

}

//数据接口
function getDataSpeed(){

}

function update_chart(){
    data = chart_option.series[0].data;
    data2 = chart_option.series[1].data;
    x = chart_option.xAxis.data;
    
    x.shift();
    x.push(getSecondScale());
  
    data.shift();
    data2.shift();
    next_data = (Math.random() * 5 + 10).toFixed(2);  //获取下一个流量数据
    change = Math.random();
    data.push(next_data);
    next_data2 = (next_data - 10 + change).toFixed(2)
    data2.push(next_data2);

    //动态更新流量指示器
    var board = document.getElementById('current_speed')
    var gauge = document.getElementById('gauge');
    var outspeed = document.getElementById('outspeed');
    if(next_data > 50){
        gauge.style.backgroundColor = 'red';
    }else if(next_data > 30){
        gauge.style.backgroundColor = 'orange';
    }else{
        gauge.style.backgroundColor = '#1abc9c';
    }
    board.innerHTML = next_data;
    outspeed.innerHTML = next_data2;
    if(chart_status == false){
        mychart.setOption(chart_option);
        chart_option.animation = true;
    }
    else{
        chart_option.animation = false;
    }

}

timer = setInterval('update_chart()', 1000);

function chart_switch(){
  if(chart_status == false)
    chart_status = true;
  else
    chart_status = false
}

/////////////////////////
// Change view function
////////////////////////
dashboard_view = document.getElementById('dashboard_view');
source_view = document.getElementById('source_view');
strategy_view = document.getElementById('strategy_view');
click_manage_view = document.getElementById('click_manage_view');
view_buttons = document.getElementsByClassName('left_button');
current_view = dashboard_view;
current_button = view_buttons[0];
function show_dashboard(ob){
    if(current_view != dashboard_view){
        current_view.style.display = 'none';
        current_view = dashboard_view;
        current_view.style.display = 'flex'
        mychart.resize()
        current_button.style.backgroundColor = '#19997f';
        current_button = ob;
        current_button.style.backgroundColor = '#1abc9c';
    }
}
function show_source(ob){
    if(current_view != source_view){
        current_view.style.display = 'none';
        current_view = source_view;
        current_view.style.display = 'flex'
        pie_chart.resize()
        current_button.style.backgroundColor = '#19997f';
        current_button = ob;
        current_button.style.backgroundColor = '#1abc9c';
    }
}
function show_strategy(ob){
    if(current_view != strategy_view){
        current_view.style.display = 'none';
        current_view = strategy_view;
        current_view.style.display = 'flex';
        //mychart.resize();
        current_button.style.backgroundColor = '#19997f';
        current_button = ob;
        current_button.style.backgroundColor = '#1abc9c';
    }
}
function show_click_manager(ob){
    if(current_view != click_manage_view){
        current_view.style.display = 'none';
        current_view = click_manage_view;
        current_view.style.display = 'flex';
        //mychart.resize();
        current_button.style.backgroundColor = '#19997f';
        current_button = ob;
        current_button.style.backgroundColor = '#1abc9c';
    }
}
/////////////////////////
// 流量监控尺度切换
/////////////////////////
var scale_status = 5;
var scale_buttons = document.getElementsByClassName('scale_g');
scale_buttons[scale_status].style.backgroundColor = '#33C4C5';

function onChangeScale(ob){
    scale_buttons[scale_status].style.backgroundColor = '#34495e';
    switch(ob.innerHTML){
        case '年':
            scale_status = 0;
            break;
        case '月':
            scale_status = 1;        
            break;
        case '日':
            scale_status = 2;
            break;
        case '时':
            scale_status = 3;
            break;
        case '分':
            scale_status = 4;
            break;
        case '秒':
            scale_status = 5;
            break;
    }
    scale_buttons[scale_status].style.backgroundColor = '#33C4C5';
}

/////////////////////////
// 流量来源饼状图
/////////////////////////

var pie_chart = echarts.init(document.getElementById('pie_chart'))

var pie_chart_option = {
   
    tooltip : {
        trigger: 'item',
        formatter: '<div>{c0}Mbps</div> <div style="font-size:0.75em">{b0}</div>'
    },
  
    series : [
        {
            type:'pie',
            radius : [0, '85%'],
            center : ['50%', '50%'],
            label: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            lableLine: {
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {value:0.4, name:'192.168.0.2'},
                {value:0.3, name:'192.168.0.5'},
                {value:5, name:'210.114.121.24'},
                {value:5, name:'10.14.121.11'},
                {value:5, name:'10.42.121.211'},
              
            ]
        },
    ]
};
pie_chart.setOption(pie_chart_option)
window.onresize = function(){
    mychart.resize();
    pie_chart.resize();
};

function update_pie(){
    pie_chart_option.series[0].data[0].value = (Math.random() * 5).toFixed(2);
    pie_chart.setOption(pie_chart_option)
}
setInterval(update_pie, 1000);


////////////////////////////
//来源界面显示模式切换
///////////////////////////
var view_style_pie = document.getElementById('pie_chart_wrapper');
var view_style_list = document.getElementById('list_wrapper');
var current_view_style = view_style_list;
function change_view_style(ob){
    current_view_style.style.display = "none";
    var option = ob.value;
    if(option == 'Form'){
        view_style_list.style.display = "flex";
        current_view_style = view_style_list;
    }
    else{
        view_style_pie.style.display = "flex";
        current_view_style = view_style_pie;
        pie_chart.resize();
    }
}


/////////////////////////////
// strategy form
////////////////////////////
var current_item_focus = -1;
var current_last_item_sn = 0;
var max_item_per_page = 2;

var current_page_sn = 1;
var page_total = 2;
var offset = 0;
var table = document.getElementById('strategy_table');
var itemlist = new Array();
var data_query = 'normal';
var strategy_display_area = document.getElementById('strategy_check').firstElementChild;


function initAttr(){
    var inital_current_item_focus = -1;
    var inital_current_last_item_sn = 0;
    var inital_max_item_per_page = 2;
    var inital_current_page_sn = 0;
    var inital_page_total = 2;

    current_item_focus = inital_current_item_focus;
    current_last_item_sn = inital_current_last_item_sn;
    max_item_per_page = inital_max_item_per_page;

    offset = 0;
    current_page_sn = inital_current_page_sn;
    page_total = inital_page_total;
}

//###################
//  填充表格,翻页操作
//###################

function addRow(data){
    var tbody = table.children[1];
    var tr = document.createElement('tr');
    tr.setAttribute('value', current_last_item_sn);
    tr.setAttribute('onclick', 'onClickStrategyItem(this)')
    
    var td_list = new Array();
    for(var i=0;i<data.length;i++){
        var td = document.createElement('td');
        td.innerHTML = data[i];
        td_list.push(td)
    }
    for(var i=0;i<td_list.length;i++){
        tr.appendChild(td_list[i])
    }
    tbody.appendChild(tr);
    itemlist.push(tr);
    current_last_item_sn++;
}

//生成一行数据, raw_data格式如下[Num, name, description, enable], 该函数定义了行内格式
function generate_row_data(raw_data){
    var data = new Array();
    var enable = (raw_data[3] == true)? 'checked="checked"' : '';
    data.push('<input name="enable" type="checkbox" value="' + raw_data[0] + '"' +  enable + 'onchange="onChoose(this)" disabled="disabled">');
    for(var i=1;i<raw_data.length - 1;i++){
        data.push(raw_data[i]);
    }
    return data;
}

//载入数据到表格
function loadForm(form_data){
    //var checkbox = document.getElementsByName('enable');
    for(var i=0;i<form_data.length;i++){
        var data = generate_row_data(form_data[i]);
        addRow(data);
    }
}

//翻页，重新填充表格
function changePage(page_sn){
    offset = page_sn * max_item_per_page;
    current_page_sn = page_sn;
    current_last_item_sn = offset;
    var form_data = getFormData(offset, max_item_per_page);
    var tbody = table.children[1];
    tbody.innerHTML = "";
    current_item_focus = -1;
    itemlist = [];
    loadForm(form_data);
}



//后台数据接口
function getFormData(offset, amount){
    var a = [];
    if(offset == 0){
        a.push([1,'UdpFlood Defense','针对Udp泛洪攻击的防御策略',false])
        a.push([2,'RstAtack Defense','针对rst复位攻击的防御策略',true]);
        a.push([3,'SmufFlood Defense','针对Smuf攻击的防御攻击的防御策略',true]);
        a.push([4,'LandAtack Defense','针对Land攻击的防御策略',true]);
        a.push([5,'RED Defense','基于RED拥塞控制的防御策略',true]);
    }else if(offset == 2){
        a.push([3,'hdddd','hi',false])
        a.push([4,'haaaa','hello',true]);
    }
  
    return a;
}

function getBackendData(){

}

//################
// 处理表格项目点击
//###############
function unfocus(ob){
    ob.style.backgroundColor = 'lightcyan';
    ob.style.color = 'black';
}

function focus(ob){
    ob.style.backgroundColor = '#1abc9c';
    ob.style.color = 'white';
}

function _focus(ob){
    ob.style.backgroundColor = '#1abc9c';
    ob.style.color = 'white';
}

function getStrategyContent(num){
    return '';
}
function onClickStrategyItem(ob){
    var num = Number(ob.getAttribute('value'));
    if(current_item_focus != -1){
        unfocus(itemlist[current_item_focus]);
    }
    strategy_display_area.innerHTML = getStrategyContent(num);
    current_item_focus = num - offset;
    focus(ob);
}

//###################
//strategy checkbox
//###################
function onChoose(object){
}

//##################
//  启动和退出编辑
//##################
function editEnable(enable){
    //进入/退出编辑状态的UI切换
    var b_editing = document.getElementsByClassName('b_editing');
    var b_edited = document.getElementsByClassName('b_edited');
    var checkbox = document.getElementsByName('enable');
    if(enable == true){
        var b_editing_display = "inline";
        var b_edited_display = "none";
        for(var i=0;i<checkbox.length;i++){
            checkbox[i].removeAttribute('disabled');
        }
    }else{
        b_editing_display = "none";
        b_edited_display = "inline";
        for(var i=0;i<checkbox.length;i++){
            checkbox[i].setAttribute('disabled','disabled');
        }
    }

    for(var i=0;i<b_editing.length;i++){
        b_editing[i].style.display = b_editing_display;
    }

    for(var i=0;i<b_edited.length;i++){
        b_edited[i].style.display = b_edited_display;
    }
}

function onEnableEdit(){
    editEnable(true);
}

function onDisableEdit(ob){
    editEnable(false);
    if(ob.innerHTML == '取消'){
        alert('未保存');
    }else{
        alert('已保存');
        var checkbox = document.getElementsByName('enable');
        for(var i=0;i<checkbox.length;i++){
            alert(checkbox[i].checked);
        }
    }

}

var strategy_pagination = document.getElementById('s_p');
var last_button = strategy_pagination.firstElementChild.children[0];
var next_button = strategy_pagination.firstElementChild.children[2];
//#################################
//  翻页指示器（切换翻页按钮的高亮状态）
//#################################
var page_indicators = strategy_pagination.getElementsByTagName('span')[0].children;
function setPageIndicator(enable){
    if(enable == true){
        page_indicators[current_page_sn].style.backgroundColor = '#1abc9c';
    }else{
        page_indicators[current_page_sn].style.backgroundColor = '#34495e';
    }
}


//##################
//  翻页事件
//##################
function setNextLastButton(){
    if(current_page_sn == 0){
        last_button.style.visibility = 'hidden';
    }else{
        last_button.style.visibility = 'visible';
    }

    if(current_page_sn == page_total - 1){
        next_button.style.visibility = 'hidden';
    }else{
        next_button.style.visibility = 'visible';
    }
}

function onStrategySwitchPage(ob){
    var value = ob.getAttribute('value');
    setPageIndicator(false);
    switch(value){
        case 'l':
            current_page_sn = current_page_sn - 1;
            break;
        case 'n':
            current_page_sn = current_page_sn + 1;
            break;
        default:
            value = Number(value);
            current_page_sn = value - 1;
            break;
    }
    setNextLastButton();
    changePage(current_page_sn);
    setPageIndicator(true);
}

//#############
//  初始化
//#############
function initalForm(){
    
    initAttr();
    if(page_total > 1){
        strategy_pagination.style.display='flex';
    }
    setNextLastButton();
    changePage(0);
    setPageIndicator(true);
}

initalForm();
////////////////////////
// search event
////////////////////////
function onSearchChange(ob){
}

function onSearchBarBlur(ob){
    if(ob.value == ""){
        ob.style.backgroundColor = '#19997f';
    }
}
function onSearchBarFocus(ob){
    if(ob.value == ""){
        ob.style.backgroundColor = '#1abc9c';
    }
}