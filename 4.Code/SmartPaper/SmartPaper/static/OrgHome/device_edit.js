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
        $("#name").val(data.name);
        $("#ipaddress").val(data.ipaddress);
        $("#macaddress").val(data.mac);
        $("#port").val(data.port);
        $("#dev_type").val(data.typecode);
        $('#state_list').val(data.state);
        $('#org_list').val(data.orgcode);

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
        var ipaddress = $("#ipaddress").val();
        var port = $("#port").val();
        var macaddress = $("#macaddress").val();
        var dev_type = $("#dev_type").val();
        var state_list = $("#state_list").val();
        var ownerOrg = $('#org_list').val();


        if (name == ""
        || ipaddress == ""
        || port == ""
        || ownerOrg == ""
        || macaddress == ""
            || state_list == ""
        || dev_type == "")
        {
            alert("信息不能为空");
            return;
        }


        // post参数
        var postParm = new Array();
        postParm[0] = "name=" + name;
        postParm[1] = "ipaddress=" + ipaddress;
        postParm[2] = "port=" + port;
        postParm[3] = "mac=" + macaddress;
        postParm[4] = "state=" + state_list;
        postParm[5] = "devtype=" + dev_type;
        postParm[6] = "orgcode=" + ownerOrg;


        var listParams = new Array();
        listParams[0] = "command=DEVICE_EDIT";
        postParm[7] = "code=" + code;


        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "orgsign=" + orgsign;
        listParams[3] = "logincode=" + $.cookie("OrgUserCode");


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/device/?" ,listParams);
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