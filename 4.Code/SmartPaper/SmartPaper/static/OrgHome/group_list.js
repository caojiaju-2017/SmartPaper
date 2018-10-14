var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var refreshTime ;
window.onload=function()
{
};
// $(window).resize(function() {
//     window.location.reload();
// });
$(document).ready(function(e) {
    // 启动终端状态刷新定时器

});

$.extend({
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    editGroup:function (data)
    {
            layer.open({
                title: ['分区编辑', 'font-size:13px;margin-top:10px;'],
                type: 2,
                area:['500px', '260px'],
                content: 'group_add.html?code=' + data.code
            });
    },

    deleGroup:function (data)
    {
        var listParams = new Array();
        listParams[0] = "command=GROUP_DELE";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "code=" + data.code;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/group/?" ,listParams);
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
                    location.reload();
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    closeLight:function (data) {
        var listParams = new Array();
        listParams[0] = "command=GROUP_CLOSE_LIGHT";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "code=" + data.code;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/group/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    alert("指令下发成功!");
                    location.reload();
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    openLight:function (data) {
        var listParams = new Array();
        listParams[0] = "command=GROUP_OPEN_LIGHT";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "code=" + data.code;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/group/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd, params,
            function (data) {

                var ErrorId = data.ErrorId;
                var Result = data.Result;

                if (ErrorId == 200) {
                    alert("指令下发成功!");
                    location.reload();
                }
                else {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});