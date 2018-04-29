////////////////////
//main 流量 chart
////////////////////
var chart_status = false;
var mychart = echarts.init(document.getElementById('chart'), 'macarons');
var chart_option = {
    tooltip:{
        trigger:'axis',
        axisPointer: {
            type: 'cross'
        }
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
        data: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    },
    yAxis: {},
    series: [
        {
            name:'speed',
            type:'line',
            smooth:true,
            data:(function(){
                var data = new Array()
                for(var i=0; i<20; i++){
                data.push(Math.random() * 10);
                }
                return data
            })(),
            areaStyle: {
                normal: {}
            },
        }
    ]

}; 
mychart.setOption(chart_option) 

function update_chart(){
  data = chart_option.series[0].data;
  x = chart_option.xAxis.data;
  x.shift();
  x.push(x[x.length - 1] + 1);
  data.shift();
  next_data = (Math.random() * 10).toFixed(2);
  data.push(next_data);
  document.getElementById('current_speed').innerHTML = next_data;
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
current_view = dashboard_view;
function show_dashboard(){
    if(current_view != dashboard_view){
        current_view.style.display = 'none';
        current_view = dashboard_view;
        current_view.style.display = 'flex'
        mychart.resize()
    }
}
function show_source(){
    if(current_view != source_view){
        current_view.style.display = 'none';
        current_view = source_view;
        current_view.style.display = 'flex'
        pie_chart.resize()
    }
}
function show_strategy(){
    if(current_view != strategy_view){
        current_view.style.display = 'none';
        current_view = strategy_view;
        current_view.style.display = 'flex';
        //mychart.resize();
    }
}
function show_click_manager(){
    if(current_view != click_manage_view){
        current_view.style.display = 'none';
        current_view = click_manage_view;
        current_view.style.display = 'flex';
        //mychart.resize();
    }
}
/////////////////////////
// Source pie chart
////////////////////////

var pie_chart = echarts.init(document.getElementById('pie_chart'))

var pie_chart_option = {
   
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
  
    series : [
        {
            type:'pie',
            radius : [0, '85%'],
            center : ['50%', '50%'],
            label: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            lableLine: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {value:10, name:'rose1'},
                {value:5, name:'rose2'},
                {value:15, name:'rose3'},
                {value:25, name:'rose4'},
                {value:20, name:'rose5'},
                {value:35, name:'rose6'},
                {value:30, name:'rose7'},
                {value:40, name:'rose8'}
            ]
        },
    ]
};
pie_chart.setOption(pie_chart_option)
                    
window.onresize = function(){
    mychart.resize();
    pie_chart.resize();
};


////////////////////////////
//change Source view style
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