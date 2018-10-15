var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    $.loadDevInfo(code);
});

$.extend({

    loadDevInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=DEVICE_INFO";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "devcode=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/device/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                $.fillElement(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    fillElement:function (data) {
        $("#name").text(data.name);
        $("#ipaddress").text(data.ipaddress);
        $("#macaddress").text(data.mac);
        $("#port").text(data.port);
        $("#dev_type").text(data.typename);
        $('#state_list').text(data.state);
        $('#org_list').text(data.orgname);

        $('#bind_power').text(data.powername);
        $('#pportname').text(data.pportname);

        $('#bind_group').text(data.grpname);

        $.setupChart1Prepare(data.stats);

        layui.use('form', function () {
            var form = layui.form; //
            form.render('select');
        });
    },
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    setupChart1Prepare:function (datas) {
        // var dataArrages = V2.4.3 Array();
        //
        // var addData = V2.4.3 Array();
        // var deleData = V2.4.3 Array();
        // var stopData = V2.4.3 Array();
        // var labsData = V2.4.3 Array();
        //
        // var keyList = V2.4.3 Array();
        // for(var key in datas) {
        //     keyList[keyList.length] = key;
        // }
        // keyList.sort();
        //
        // for(var index = 0 ; index < keyList.length; index ++)
        // {
        //     var currentKey = keyList[index];
        //     var data = datas[currentKey];
        //
        //
        //     addData[addData.length] = data.add;
        //     deleData[deleData.length] = data.remove;
        //     stopData[stopData.length] = data.stop;
        //
        //     labsData[labsData.length] = currentKey.substring(5,10);
        // }


        var dataArrages = new Array();
        dataArrages["name"] = "";
        dataArrages["adddatas"] = [12,14,10,90];
        dataArrages["stopdatas"] = [2,4,13,18];
        dataArrages["deldatas"] = [0,12,1,8];

        dataArrages["axisx"] = ["A","B","C","D"];

        dataArrages["minvalue"] = 0;
        dataArrages["maxvalue"] = 100;


        $.setupChart2("ichart-render1",datas);
    },
    setupChart1:function (idname,datas) {
        {
            var heigth = $("#ichart-render1").height();
            var width = $("#ichart-render1").width();
            heigth = 190;
            // $.calcSize();
            // var actWidth = Math.round(width * 0.65);
            // var actHeigth = Math.round(heigth / 2) - 30;
            var actWidth = width;
            var actHeigth = heigth;

            var data = [
				         	{
				         		name : '新增',
				         		value:datas.adddatas,
				         		color:'#1385a5'
				         	},
				         	{
				         		name : '停播',
				         		value:datas.stopdatas,
				         		color:'#c56966'
				         	},
				         	{
				         		name : '删除',
				         		value:datas.deldatas,
				         		color:'#106966'
				         	}
				         ];
				var chart = new iChart.ColumnMulti2D({
						render : idname,
						data: data,
						labels:datas.axisx,
						title :datas.name,
						subtitle : '',
						footnote : '',
						width : actWidth,
						height : actHeigth,
						background_color : '#ffffff',
						legend:{
							enable:true,
							background_color : null,
							border : {
								enable : false
							}
						},
						coordinate:{
							background_color : '#ffffff',
							scale:[{
								 position:'left',
								 start_scale:0,
								 end_scale:datas.maxvalue,
								 scale_space:datas.minvalue
							}],
							width:actWidth - 100,
							height:actHeigth - 90
						},
						sub_option: {
                            listeners: {
                                /**
                                 * r:iChart.Rectangle2D对象
                                 * e:eventObject对象
                                 * m:额外参数
                                 */
                                click: function (r, e, m) {
                                    //alert(r.get('name') + ' ' + r.get('value'));
                                }
                            }
                        }
				});
				chart.draw();
        }
    },

    setupChart2: function (idname, datasT) {
        var heigth = $("#ichart-render1").height();
        var width = $("#ichart-render1").width();
        heigth = 270;

        var cpuDatas = [];
        var memDatas = [];
        var diskDatas = [];
        var labels = [];

        for (var index = 0 ; index < datasT.length; index ++)
        {
            var oneData = datasT[index];

            cpuDatas.push(oneData.cpu);
            memDatas.push(oneData.memory);
            diskDatas.push(oneData.disk);

            labels.push(oneData.recordtime);
        }

        if (labels.length < 2)
        {
            return;
        }
        // for (var i = 0; i < 10; i++) {
        //     cpuDatas.push(Math.floor(Math.random() * (10 + ((i % 16) * 5))) + 10);
        // }
        // for (var i = 0; i < 10; i++) {
        //     memDatas.push(Math.floor(Math.random() * (10 + ((i % 16) * 5))) + 10);
        // }
        // for (var i = 0; i < 10; i++) {
        //     diskDatas.push(Math.floor(Math.random() * (10 + ((i % 16) * 5))) + 10);
        // }
        var data = [
            {
                name: '处理器',
                value: cpuDatas,
                color: '#ec4646',
                line_width: 2
            },
            {
                name: '内存',
                value: memDatas,
                color: '#0c4646',
                line_width: 2
            },
            {
                name: '磁盘',
                value: diskDatas,
                color: '#f0f0f0',
                line_width: 2
            }
        ];

        // var labels = ["2018-06-03 10:10:09", "2018-06-03 10:10:09", "2018-06-03 10:10:09", "2018-06-03 10:10:09",
        //     "2018-06-03 10:10:09", "2018-06-03 10:10:09", "2018-06-03 10:10:09", "2018-06-03 10:10:09", "2018-06-03 10:10:09",
        //     "2018-06-03 10:10:09"];

        var chart = new iChart.LineBasic2D({
            render: idname,
            data: data,
            align: 'center',
            title: {
                text: '历史资源占用',
                font: '微软雅黑',
                fontsize: 20,
                color: '#b4b4b4'
            },
            subtitle: {
                text: '',
                font: '微软雅黑',
                color: '#b4b4b4'
            },
            footnote: {
                text: '',
                font: '微软雅黑',
                fontsize: 11,
                fontweight: 600,
                padding: '0 28',
                color: '#b4b4b4'
            },
            width: width,
            height: heigth,
            shadow: true,
            shadow_color: '#202020',
            shadow_blur: 8,
            shadow_offsetx: 0,
            shadow_offsety: 0,
            background_color: '#2e2e2e',
            tip: {
                enable: true,
                shadow: true,
                listeners: {
                    //tip:提示框对象、name:数据名称、value:数据值、text:当前文本、i:数据点的索引
                    parseText: function (tip, name, value, text, i) {

                        return "<span style='color:#005268;font-size:12px;'>" + name + ":" + labels[i] + ":<br/>" +
                            "</span><span style='color:#005268;font-size:20px;'>" + value + "%</span>";
                    }
                }
            },
            crosshair: {
                enable: true,
                line_color: '#ec4646'
            },
            sub_option: {
                smooth: true,
                label: false,
                hollow: false,
                hollow_inside: false,
                point_size: 8
            },
            coordinate: {
                width: 640,
                height: 260,
                striped_factor: 0.18,
                grid_color: '#4e4e4e',
                axis: {
                    color: '#252525',
                    width: [0, 0, 4, 4]
                },
                scale: [{
                    position: 'left',
                    start_scale: 0,
                    end_scale: 100,
                    scale_space: 10,
                    scale_size: 2,
                    scale_enable: false,
                    label: {color: '#9d987a', font: '微软雅黑', fontsize: 11, fontweight: 600},
                    scale_color: '#9f9f9f'
                }, {
                    position: 'bottom',
                    label: {color: '#9d987a', font: '微软雅黑', fontsize: 11, fontweight: 600},
                    scale_enable: false,
                    labels: labels
                }]
            }
        });
        //利用自定义组件构造左侧说明文本
        chart.plugin(new iChart.Custom({
            drawFn: function () {
                //计算位置
                var coo = chart.getCoordinate(),
                    x = coo.get('originx'),
                    y = coo.get('originy'),
                    w = coo.width,
                    h = coo.height;
                //在左上侧的位置，渲染一个单位的文字
                chart.target.textAlign('start')
                    .textBaseline('bottom')
                    .textFont('600 11px 微软雅黑')
                    .fillText('占用率', x - 40, y - 12, false, '#9d987a')
                    .textBaseline('top')
                    .fillText('(时间)', x + w + 12, y + h + 10, false, '#9d987a');

            }
        }));
        //开始画图
        chart.draw();
    },
});