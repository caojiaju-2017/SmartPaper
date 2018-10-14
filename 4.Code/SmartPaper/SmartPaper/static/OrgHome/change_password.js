var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var porgCode = "";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    porgCode = $.GetQueryString("pcode");

    if (code != "" && code != "null" && code != null)
    {
        $.loadCustomInfo(code);
    }
    else
    {
        //$.initTestData();
    }

    // $.loadBoxData();
});

$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    updatePassword: function () {

        var newP1 = $("#newpassword").val()
        var newP2 = $("#comfirmpassword").val();

        if (newP1 != newP2 || newP1 == "" || newP1 == null)
        {
            $.showMsg(layer,"新密码不一致，或输入为空");
            return;
        }

        var oldP = $("#oldpassword").val();

        if (oldP == "" || oldP == null)
        {
            $.showMsg(layer,"原密码输入为空");
            return;
        }

        if (newP1 == oldP)
        {
            $.showMsg(layer,"密码修改前后一致");
            return;
        }

        var listParams = new Array();
        listParams[0] = "command=PSWD_RESET";

        var timestamp = (new Date()).valueOf();
        // listParams[1] = "timestamp=" + timestamp;
        listParams[1] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "oldpassword=" + $.md5(oldP);
        // postParm[1] = "orgsign=" + orgsign;
        postParm[1] = "newpassword=" + $.md5(newP1);

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/login/?" ,listParams);
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