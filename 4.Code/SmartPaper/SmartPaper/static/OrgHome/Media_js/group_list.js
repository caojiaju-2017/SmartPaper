var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
window.onload=function()
{
};

$(document).ready(function(e) {
    $.loSmartControlDatas();
});

$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    loSmartControlDatas:function()
    {
       var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=3" ;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                loadGroupTree(data);
                grpTree.nodes = data;
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    unbindRes:function (data,specialCode) {
        var listParams = new Array();
        listParams[0] = "command=SPECIAL_RES_SET";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "specialcode=" + specialCode;
        postParm[2] = "rescode=" + data.code;
        postParm[3] = "type=" + data.type; //资源类别
        postParm[4] = "way=" + 0;  // 1表示绑定


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/res/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert("绑定成功!");
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    deleGrp:function (grpcode) {
        var listParams = new Array();
        listParams[0] = "command=SPECIAL_DELE";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "specialcode=" + grpcode;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/res/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {
                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    // 改变 分组数据
                    selectNode = null;
                    $("#groupname").text("请选中左侧分组，查看分组资源");
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

});