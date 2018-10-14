var code = null;
var orgsign = "1e2c68303ebd11e880d3989096c1d848";

var itemTemplate = '<input type="checkbox" name="{roleuuid}" id="{rolecode}" lay-skin="primary" title="{rolename}" style="width: 80%;float: left">';

var roleData = null;
window.onload = function () {
};

$(document).ready(function (e) {
    code = $.GetQueryString("code");
    // 查询角色
    $.loadBoxData(null);
});

$.extend({
    loadBoxData:function () {
        var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=1" ;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                roleData = data;

                for (var index = 0; index < roleData.length; index++) {
                    var oneData = roleData[index];
                    var readyText = $("#role_div").html();
                    var abcTemp = {};
                    abcTemp["roleuuid"] = oneData.id;
                    abcTemp["rolecode"] = oneData.id;
                    abcTemp["rolename"] = oneData.name;
                    var tempalteResult = $.format(itemTemplate, abcTemp);
                    $("#role_div").html(readyText + tempalteResult);
                }

                $.loadAccountRole();

                                layui.use('layer', function () {
                    layui.use('form', function () {
                        var form = layui.form; //只有执行了这一步，部分表单元素才会自动修饰成功
                        form.render();
                    });

                });
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    GetQueryString: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    },

    loadAccountRole: function () {
        var listParams = new Array();
        listParams[0] = "command=USERS_LIST_ROLES";

        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "code=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (datas) {

                // 设置选中状态---ing
                for (var index = 0 ; index < datas.length; index ++)
                {
                    var oneMap = datas[index];
                    var roleCode = oneMap.rcode
                    $("#" + roleCode)[0].checked = true;
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

    getSelectRoles:function () {
        var rtnString = null;

        for (var index = 0 ; index < roleData.length; index ++)
        {
            var oneRole = roleData[index];
            var currentCheck = $("#" + oneRole.id);
            var checkFlag = currentCheck[0].checked;

           // .checked
            if (checkFlag)
            {
                 if (rtnString == null)
                 {
                     rtnString = oneRole.id;
                 }
                 else
                 {
                     rtnString = rtnString + "," + oneRole.id;
                 }
            }
        }

        return rtnString;

    },
    saveInfo: function () {
        var listParams = new Array();

        listParams[0] = "command=SET_USER_ROLES";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;

        var postParm = new Array();
        postParm[0] = "usercode=" + code;
        postParm[1] = "rolecodes=" + $.getSelectRoles();

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
                    alert("操作成功!");

                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.location.reload();
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});