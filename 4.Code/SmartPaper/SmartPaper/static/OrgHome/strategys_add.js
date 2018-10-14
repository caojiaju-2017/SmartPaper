var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    $.loadBoxData(null);
});

$.extend({

    loadDevInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=STRATEGYS_INFO";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "code=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/strategys/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                $.fillElement(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    fillElement:function (data) {
        $("#name").val(data.name);

        $("#startdate").val(data.startdate);
        $("#stopdate").val(data.stopdate);

        $("#poweron").val(data.opentime);
        $("#poweroff").val(data.closetime);

        $("#org_list").val(data.orgcode);

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
    loadBoxData: function (orgparam) {
        var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=0";

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                for (var index = 0; index < data.length; index++) {
                    var readyText = $("#org_list").html();
                    var oneOrg = data[index];
                    var abcTemp = {};
                    abcTemp["orgcode"] = oneOrg.id;
                    abcTemp["orgname"] = oneOrg.name;

                    var tempalteResult = $.format(itemTemplate, abcTemp);

                    $("#org_list").html(readyText + tempalteResult);

                    if (code != null && orgparam != null)
                    {
                        $("#org_list").find("option[value = '"+orgparam+"']").attr("selected","selected");
                    }
                }

                layui.use('layer', function () {
                    layui.use('form', function () {
                        var form = layui.form; //只有执行了这一步，部分表单元素才会自动修饰成功
                        form.render();
                    });

                });

                 if (code != "" && code != "null" && code != null)
                {
                    $.loadDevInfo(code);
                }
                else
                {
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },


    saveInfo: function () {
        var name = $("#name").val();
        var startdate = $("#startdate").val();
        var stopdate = $("#stopdate").val();
        var poweron = $("#poweron").val();
        var poweroff = $("#poweroff").val();
        var org_list = $("#org_list").val();


        if (name == "" || startdate == "" || stopdate == ""
        || poweron == "" || poweroff == "" || org_list == "")
        {
            alert("信息不能为空");
            return;
        }

        var date3 = new Date(startdate + " " + poweroff).getTime() - new Date(startdate + " " + poweron).getTime();   //时间差的毫秒数

        var sepSecond = Math.abs(Math.floor(date3/(1000)));

        if (sepSecond < 300)
        {
            alert("上下电时间间隔太短，至少需要五分钟");
            return;
        }

        // post参数
        var postParm = new Array();
        postParm[0] = "name=" + name;
        postParm[1] = "startdate=" + startdate;
        postParm[2] = "stopdate=" + stopdate;
        postParm[3] = "opentime=" + poweron;
        postParm[4] = "closetime=" + poweroff;
        postParm[5] = "orgcode=" + org_list;


        var listParams = new Array();
        if (code != "" && code != "null" && code != null) {
            listParams[0] = "command=STRATEGYS_EDIT";
            postParm[6] = "code=" + code;
        }
        else
        {
            listParams[0] = "command=STRATEGYS_ADD";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "orgsign=" + orgsign;
        listParams[3] = "logincode=" + $.cookie("OrgUserCode");


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/strategys/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        var params = null;
        params = $.buildPostParam(postParm);

        $.post(urlCmd, params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("操作成功!");

                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.location.reload();
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});