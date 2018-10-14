var openidTemp;
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var rolecode = null;
window.onload=function()
{
};

$(window).resize(function() {
    window.location.reload();
});

$(document).ready(function(e) {
    rolecode = $.GetQueryString("code");
});

$.extend({
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    saveInfo: function () {
        var name = $("#rolename").val();

        if (name == "" || name.length <= 0)
        {
            alert("请指定角色名称");
            return;
        }


        var listParams = new Array();
        if (rolecode != "" && rolecode != "null" && rolecode != null) {
            listParams[0] = "command=ROLE_MODI";
        }
        else
        {
            listParams[0] = "command=ROLE_ADD";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "name=" + name;
        // postParm[1] = "Funcs=" + conname;
        postParm[1] = "info=" + $("#role_info").val();
        postParm[2] = "orgsign=" + orgsign;

        if (rolecode != "" && rolecode != "null" && rolecode != null) {
            postParm[3] = "rolecode=" + rolecode;
        }


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
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
                    //alert("操作成功!");
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