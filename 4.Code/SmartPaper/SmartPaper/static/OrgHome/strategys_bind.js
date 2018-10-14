var code = null;
var grpcode = null;
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

    bindStrategys:function (data) {
        var listParams = new Array();
        listParams[0] = "command=STRATEGYS_BIND";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;

        if (code == null || code == "null")
        {
            code = $.GetQueryString("code");
        }

        postParm[1] = "code=" + code;
        postParm[2] = "devcode=" + data.code;

        if (data.state == 0)
        {
            postParm[3] = "state=1";
        }
        else
        {
            postParm[3] = "state=0";
        }


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/strategys/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    //var index = parent.layer.getFrameIndex(window.name);
                    location.reload();
                    //alert("绑定成功!");
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

});