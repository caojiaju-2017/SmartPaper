var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    $.loadBoxData(null);

    $.initTestData();
});

$.extend({
    initTestData:function()
    {
        $("#name").val("测试设备");

        $("#managename").val("曹家驹");
        $("#managephone").val("15836225941");

        $("#ipaddress").val("192.168.0.208");
        $("#macaddress").val("98-90-96-C1-D8-48");

        $("#longitude").val("104.096693");
        $("#latitude").val("30.672411");

        $("#dev_type").val("BY-Paper-S002");
        $("#state_list").val("1");
        $('#org_list').val("cadd0280bb1111e8bfc1989096c1d848");
    },
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

        $("#managename").val(data.managename);
        $("#managephone").val(data.managephone);
        $("#longitude").val(data.longitude);
        $("#latitude").val(data.latitude);

        $("#dev_type").val(data.devtype);
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

        var managename = $("#managename").val();
        var managephone = $("#managephone").val();

        var ipaddress = $("#ipaddress").val();
        var macaddress = $("#macaddress").val();

        var longitude = $("#longitude").val();
        var latitude = $("#latitude").val();

        var dev_type = $("#dev_type").val();
        var state_list = $("#state_list").val();
        var ownerOrg = $('#org_list').val();


        if (name == ""
            || ipaddress == ""
            || ownerOrg == ""
            || macaddress == ""
            || state_list == ""
            || managename == ""
            || managephone == ""
            || longitude == ""
            || latitude == ""
            || dev_type == "")
        {
            alert("信息不能为空");
            return;
        }


        // post参数
        var postParm = new Array();
        postParm[0] = "name=" + name;
        postParm[1] = "ipaddress=" + ipaddress;
        postParm[2] = "mac=" + macaddress;
        postParm[3] = "state=" + state_list;
        postParm[4] = "devtype=" + dev_type;
        postParm[5] = "orgcode=" + ownerOrg;
        postParm[6] = "managename=" + managename;
        postParm[7] = "managephone=" + managephone;
        postParm[8] = "longitude=" + longitude;
        postParm[9] = "latitude=" + latitude;


        var listParams = new Array();

        if (code != "" && code != "null" && code != null)
        {
            listParams[0] = "command=DEVICE_EDIT";
            postParm[10] = "code=" + code;
        }
        else
        {
            listParams[0] = "command=DEVICE_ADD";
        }

        // postParm[7] = "code=" + code;

        //
        // var timestamp = (new Date()).valueOf();
        // listParams[1] = "timestamp=" + timestamp;
        // listParams[2] = "orgsign=" + orgsign;
        listParams[1] = "logincode=" + $.cookie("OrgUserCode");


        // var allParams = listParams.concat(postParm);
        // allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/device/?" ,listParams);
        // urlCmd = urlCmd + "&sign=" + $.signString(allParams);

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