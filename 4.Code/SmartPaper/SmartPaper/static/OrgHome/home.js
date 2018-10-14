//http://www.ichartjs.com/   报表官网
var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var porgCode = "";
var width = 0;
var heigth = 0;
var loadingLayIndex=null;
window.onload=function()
{
};

$(document).ready(function(e) {
    $.calcSize();
    $.queryStatData();
});

$.extend({
    calcSize:function () {
        heigth =  $(document).height();
        width =  $(document).width();

        $("#ichart-render1").height(heigth / 2);
        $("#ichart-render2").height(heigth / 2);

        $("#ichart-render3").height(heigth / 2);
        $("#demo").height(0);

        // $("#demo").height(width *0.35);
    },
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    queryStatData:function()
    {
        var listParams = new Array();
        listParams[0] = "command=HOME_STAT";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
            var aToStr=JSON.stringify(data);

                $.setupChart1("ichart-render1", data.typestats,data.faultstats);
                $.setupChart2("ichart-render2", data.orgstats);
                $.setupChart3("ichart-render3", data.faultstats);

            // $("#right_panel").show();
            // layer.close(loadingLayIndex);

            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    getDevTypeName:function(typecode)
    {
        if (typecode == 1001)
        {
            return "互动桌面";
        }
        else if (typecode == 1002)
        {
            return "二维码屏";
        }
        else if (typecode == 1003)
        {
            return "3D导览";
        }
        else if (typecode == 1004)
        {
            return "全息投影";
        }
        else if (typecode == 1005)
        {
            return "分接屏";
        }
        else if (typecode == 2001 )
        {
            return "LED";
        }
        else if (typecode == 2002 )
        {
            return "白炽灯";
        }
        else if (typecode == 2003 )
        {
            return "荧光灯";
        }
    },

    isNormal:function(code,states)
    {
        var normalDevs = states[1];

        for (var index = 0 ; index < normalDevs.length; index++)
        {
            var normalDCode = normalDevs[index];

            if (normalDCode == code)
            {
                return true;
            }
        }
        return false;
    },


    //机构--展示正常和非正常设备
    setupChart1:function (idname,datas,stateDatas) {
        // var data = [
        //     {
        //         name: '正常',
        //         value: [9, 12, 10, 11, 16],
        //         color: '#007500'
        //     },
        //     {
        //         name: '故障',
        //         value: [63, 42, 38, 21, 14],
        //         color: '#e0b645'
        //     }
        // ];

        // labels = ["浙江", "江苏", "广东", "北京", "上海"];

        // 构造数据
        normalData=[];
        faultData=[];
        labelData=[];
        var maxValue = 0;
        for (var oneType in datas)
        {
            labelData[labelData.length] = $.getDevTypeName(oneType);
            var devCodes = datas[oneType]["code"]

            var normalCount = 0;
            var faultCount = 0;
            for (var index  = 0 ; index < devCodes.length ; index ++)
            {
                var oneDevCode = devCodes[index];
                var result = $.isNormal(oneDevCode,stateDatas);

                if (result)
                {
                    normalCount = normalCount + 1;
                }
                else
                {
                    faultCount = faultCount + 1;
                }
            }
            normalData[normalData.length] = normalCount;
            faultData[faultData.length] = faultCount;

            if (normalCount + faultCount > maxValue)
            {
                maxValue = normalCount + faultCount ;
            }
        }



        var data = [
            {
                name: '正常',
                value: normalData,
                color: '#007500',
                typecode:oneType,
                devstate:1
            },
            {
                name: '故障',
                value: faultData,
                color: '#e0b645',
                typecode:oneType,
                devstate:2
            }
        ];

        var chart = new iChart.ColumnStacked3D({
            render: idname,
            data: data,
            labels:labelData,
            title: {
                text: '按类型设备汇总',
                color: '#254d70'
            },
            footnote: '',
            width: width * 0.60*0.8,
            height: heigth / 2,
            column_width: 70,
            background_color: '#ffffff',
            shadow: true,
            shadow_blur: 3,
            shadow_color: '#aaaaaa',
            shadow_offsetx: 1,
            shadow_offsety: 0,
            sub_option: {
                label: {color: '#f9f9f9', fontsize: 12, fontweight: 600},
                border: {
                    width: 2,
                    color: '#ffffff'
                },
                listeners: {
                    /**
                     * r:iChart.Rectangle2D对象
                     * e:eventObject对象
                     * m:额外参数
                     */
                    click: function (r, e, m) {
                        // alert(r.get('typecode'));
                        // alert(r.get('devstate'));
                        // loadDataByTypeState(r.get('typecode'),r.get('devstate'));
                    }
                },
            },
            label: {color: '#254d70', fontsize: 12, fontweight: 600},
            legend: {
                enable: true,
                background_color: null,
                line_height: 25,
                color: '#254d70',
                fontsize: 12,
                fontweight: 600,
                border: {
                    enable: false
                }
            },
            tip: {
                enable: true,
                listeners: {
                    //tip:提示框对象、name:数据名称、value:数据值、text:当前文本、i:数据点的索引
                    parseText: function (tip, name, value, text, i) {
                        return name + ":" + value + '个';
                    }
                }
            },
            text_space: 16,//坐标系下方的label距离坐标系的距离。
            zScale: 0.5,
            xAngle: 50,
            bottom_scale: 1.1,
            coordinate: {
                width: '74%',
                height: '80%',
                board_deep: 10,//背面厚度
                pedestal_height: 10,//底座高度
                left_board: false,//取消左侧面板
                shadow: true,//底座的阴影效果
                grid_color: '#6a6a80',//网格线
                wall_style: [{//坐标系的各个面样式
                    color: '#6a6a80'
                }, {
                    color: '#b2b2d3'
                }, {
                    color: '#a6a6cb'
                }, {
                    color: '#6a6a80'
                }, {
                    color: '#74749b'
                }, {
                    color: '#a6a6cb'
                }],
                axis: {
                    color: '#c0d0e0',
                    width: 0
                },
                scale: [{
                    position: 'left',
                    scale_enable: false,
                    start_scale: 0,
                    scale_space: Math.round(maxValue / 6 + 0.5),
                    end_scale: Math.round(maxValue*(1 + 0.2)),
                    label: {color: '#254d70', fontsize: 11, fontweight: 600}
                }]
            }
        });

        //利用自定义组件构造左上侧单位
        chart.plugin(new iChart.Custom({
            drawFn: function () {
                //计算位置
                var coo = chart.getCoordinate(),
                    x = coo.get('originx'),
                    y = coo.get('originy');
                //在左上侧的位置，渲染一个单位的文字
                chart.target.textAlign('end')
                    .textBaseline('bottom')
                    .textFont('600 12px 微软雅黑')
                    .fillText('单位(个)', x + 10, y - 20, false, '#254d70')

            }
        }));

        chart.draw();
    },

    setupChart2:function (idname,datas) {
        var data = [
            // {name: '正常', value: 35.75, color: '#a5c2d5'},
            // {name: '故障', value: 29.84, color: '#cbab4f'},
        ];

        var maxValue = 0;
        for(var oneData in datas)
        {
            var oneDataDic = {name: datas[oneData].name, value: datas[oneData].count, color: $.randomColor(),code:oneData};
            data[data.length] = oneDataDic;

            if (datas[oneData].count > maxValue)
            {
                maxValue = datas[oneData].count;
            }
        }


        new iChart.Column2D({
            render: idname,
            data: data,
            title: '按网点设备汇总',
            // showpercent: true,
            decimalsnum: 2,
            width: width * 0.60 *0.8,
            height: heigth / 2,
            coordinate: {
                background_color: '#fefefe',
                scale: [{
                    position: 'left',
                    start_scale: 0,
                    end_scale: Math.round(maxValue*(1 + 0.3)),
                    scale_space: Math.round(maxValue*0.3 + 0.5),
                    listeners: {
                        parseText: function (t, x, y) {
                            // return {text: t + "%"}
                        }
                    }
                }]
            },
            sub_option: {
                listeners: {
                    /**
                     * r:iChart.Rectangle2D对象
                     * e:eventObject对象
                     * m:额外参数
                     */
                    click: function (r, e, m) {
                        //alert(r.get('name') + ' ' + r.get('value') + ' ' + r.get('code'));
                        loadOrgData(r.get('code'));
                    }
                }
            }
        }).draw();
    },

    setupChart3:function (idname,datas) {
        var data = [
            {name: '正常设备', value: datas[1].length, color: '#4572a7',state:1},
            {name: '故障设备', value: datas[2].length, color: '#aa4643',state:2},
        ];


        var chart = new iChart.Pie2D({
            render: idname,
            data: data,
            title: {
                text: '全网设备健康状况',
                color: '#3e576f'
            },
            footnote: {
                text: '',
                color: '#486c8f',
                fontsize: 11,
                padding: '0 38'
            },
            sub_option: {
                label: {
                    background_color: null,
                    sign: false,//设置禁用label的小图标
                    padding: '0 4',
                    border: {
                        enable: false,
                        color: '#666666'
                    },
                    fontsize: 11,
                    fontweight: 600,
                    color: '#4572a7'
                },
                listeners: {
                    /**
                     * r:iChart.Rectangle2D对象
                     * e:eventObject对象
                     * m:额外参数
                     */
                    click: function (r, e, m) {
                        loadStateData(r.get('state'));
                    }
                },
                border: {
                    width: 2,
                    color: '#ffffff'
                }
            },
            shadow: true,
            shadow_blur: 6,
            shadow_color: '#aaaaaa',
            shadow_offsetx: 0,
            shadow_offsety: 0,
            background_color: '#fefefe',
            offsetx: -60,//设置向x轴负方向偏移位置60px
            offset_angle: -120,//逆时针偏移120度
            showpercent: true,
            decimalsnum: 2,
            width: width * 0.35,
            height: heigth / 2,
            radius: 120
        });
        //利用自定义组件构造右侧说明文本
        chart.plugin(new iChart.Custom({
            drawFn: function () {
                //计算位置
                var y = chart.get('originy'),
                    w = chart.get('width');

                // alert("f");
                //在右侧的位置，渲染说明文字
                // chart.target.textAlign('start')
                //     .textBaseline('middle')
                //     .textFont('600 16px Verdana')
                //     .fillText('UC浏览器、\n手机QQ浏览器及\n欧朋浏览器的份额\n位列第三方手机浏览器\n市场前三甲', w - 220, y - 40, false, '#be5985', false, 20);
            }
        }));

        chart.draw();
    },

});