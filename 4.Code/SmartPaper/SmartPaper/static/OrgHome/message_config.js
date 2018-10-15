var code = "";
var orgsign= "aaea68303ebd11e880d3989096c1d848";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    $.loadBoxData(null);

});

$.extend({

    loadLedInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=TERMINAL_QUERY";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "code=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/player/?" ,listParams);
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
        $("#ipaddress").val(data.ipaddress);
        $("#port").val(data.port);
        $("#mac").val(data.mac);

        $('#org_list').val(data.orgcode);
        $('#factory').val(data.type);
        $('#width').val(data.width);
        $('#height').val(data.height);

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
                    $.loadLedInfo(code);
                }
                else
                {
                    $.initTestData();
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    initTestData:function(){
        $("#name").val("营业部LED门楣");
        $("#ipaddress").val("192.168.5.162");
        $("#port").val("9393");
        $("#mac").val("98-90-96-C1-D8-48");
    },

    clearValue:function () {
        $("#name").val("");
        $("#ipaddress").val("");
        $("#port").val("");
        $("#mac").val("");
    },

    saveInfo: function () {
        var name = $("#name").val();
        var ipaddress = $("#ipaddress").val();
        var port = $("#port").val();
        var mac = $("#mac").val();
        var ownerOrg = $('#org_list').val();
        var factory = $('#factory').val();
        var width = $('#width').val();
        var height = $('#height').val();

        if (name == "" || ipaddress == "" || port == "" || mac == "" || ownerOrg == "" || factory == "" || width == "" || height == "")
        {
            alert("注册信息不能为空");
            return;
        }

        var listParams = new Array();

        if (code != "" && code != "null" && code != null) {
            listParams[0] = "command=LED_EDIT";
        }
        else
        {
            listParams[0] = "command=LED_REGISTER";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "orgsign=" + orgsign;
        listParams[3] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "name=" + name;
        postParm[1] = "ipaddress=" + ipaddress;
        postParm[2] = "mac=" + mac;
        postParm[3] = "port=" + port;
        postParm[4] = "ledtype=" + factory;
        postParm[5] = "orgcode=" + ownerOrg;
        postParm[6] = "width=" + width;
        postParm[7] = "height=" + height;
        if (code != "" && code != "null" && code != null) {
            postParm[8] = "ledcode=" + code;
        }


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/player/?" ,listParams);
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
                    $.clearValue();
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