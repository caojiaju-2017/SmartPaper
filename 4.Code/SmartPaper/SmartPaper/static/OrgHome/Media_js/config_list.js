var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
window.onload=function()
{
};

$(document).ready(function(e) {
});

$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    removeVersion:function (data) {
        var listParams = new Array();
        listParams[0] = "command=VERSION_DELE";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "versioncode=" + data.code;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("删除成功!");
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

});