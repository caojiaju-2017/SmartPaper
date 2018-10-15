var code = null;
var orgsign = "1e2c68303ebd11e880d3989096c1d848";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload = function () {
};

$(document).ready(function (e) {
    code = $.GetQueryString("code");
    account = $.GetQueryString("account");
    // $.loadBoxData();

    if (code != "" && code != "null" && code != null) {
        $.loadAccountInfo(code,account);
    }
    else {
        //$.initTestData();
        $.loadBoxData(null);
    }


});

$.extend({

    GetQueryString: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    },

    selectVipImage: function () {
        if (code == "" || code == "null" || code == null) {
            alert("请先创建账户，并保存。")
            return;
        }


    },

    getVipCode: function () {
        return code;
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
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    loadAccountInfo: function (code,account) {
        var listParams = new Array();
        listParams[0] = "command=ACCOUNT_QUERY";

        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "code=" + code;
        listParams[5] = "account=" + account;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (datas) {
                // 检查查询状态
                $("#accountname").val(datas.name);
                $("#conphone").val(datas.phone);
                $("#account").val(datas.account);

                // 该参数在后台不予处理，密码修改为专用通道
                $("#password").val("123456");

                $("#conphone").attr("disabled","disabled");
                $("#account").attr("disabled","disabled");
                $("#password").attr("disabled","disabled");

                $("#account_type_list").find("option[value = '"+datas.type +"']").attr("selected","selected");
                $.loadBoxData(datas.orgcode);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    initTestData: function () {
        $("#accountname").val("黄先生");
        $("#conphone").val("028-56903218");
        $("#account").val("huangxiansheng");
        $("#password").val("123456");
    },

    clearValue: function () {
        $("#accountname").val("");
        $("#conphone").val("");
        $("#account").val("");
        $("#password").val("");
    },

    saveInfo: function () {
        var accountname = $("#accountname").val();
        var conphone = $("#conphone").val();
        var account = $("#account").val();
        var password = $("#password").val();
        var account_type_list = $('#account_type_list').val();
        var accountOrg = $('#org_list').val();

        if (accountname == "" || accountname.length <= 0)
        {
            alert("请指定账户使用者真实名称");
            return;
        }
        if (conphone == "" || conphone.length <= 0)
        {
            alert("未输入账户");
            return;
        }


        if (account == "" || account.length <= 0)
        {
            alert("请设置员工工号");
            return;
        }

        if (password == "" || password.length <= 0)
        {
            alert("账户登陆密码不能为空");
            return;
        }

        if (accountOrg == "" || accountOrg.length <= 0)
        {
            alert("请选择账户归属单位");
            return;
        }

        if (account_type_list == "" || account_type_list.length <= 0)
        {
            alert("请选择账户类型");
            return;
        }

        var listParams = new Array();
        if (code != "" && code != "null" && code != null) {
            listParams[0] = "command=ACCOUNT_MODI";
        }
        else {
            listParams[0] = "command=ACCOUNT_ADD";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;

        password = $.md5(password);
        var postParm = new Array();
        postParm[0] = "name=" + accountname;
        postParm[1] = "phone=" + conphone;
        postParm[2] = "orgcode=" + accountOrg;
        postParm[3] = "account=" + $("#account").val();
        postParm[4] = "accounttype=" + account_type_list;

        if (code != "" && code != "null" && code != null) {
            postParm[5] = "code=" + code;
        }
        else
        {
            postParm[5] = "password=" + password;
        }


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/org/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        var params = null;
        params = $.buildPostParam(postParm);

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    $.clearValue();
                    alert("操作成功!");
                    // if (code != "" && code != "null" && code != null)
                    // {
                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.location.reload();
                    // }
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});