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
        var name = $("#groupname").val();

        if (name == "" || name.length <= 0)
        {
            alert("必须为分组指定名称");
            return;
        }

        var listParams = new Array();
        listParams[0] = "command=SPECIAL_ADD";

        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "name=" + name;
        postParm[1] = "orgsign=" + orgsign;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/res/?" ,listParams);
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