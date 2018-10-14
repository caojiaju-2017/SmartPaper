var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var configCode=null;
$.extend({
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    commitSave: function () {
        var paramvalue = $("#paramvalue").val();
        if (paramvalue == "")
        {
            $.showMsg(layer, "参数值不能为空");
            return;
        }

        var listParams = new Array();

        listParams[0] = "command=PARAM_SETTING";  // 暂不使用
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "orgsign=" + orgsign;
        listParams[3] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "paramcode=" + configCode;
        postParm[1] = "keyvalue=" + paramvalue;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
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
                    $.showMsg(layer, "操作成功");

                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.location.reload();
                }
                else
                {
                    $.showMsg(layer, data.ErrorInfo);
                }

            },
            "json");
    }

});