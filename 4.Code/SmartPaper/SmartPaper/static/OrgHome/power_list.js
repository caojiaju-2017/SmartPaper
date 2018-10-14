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

    closePower:function(data)
    {
        // 关闭电源所有通道
        var commandUrl = "http://" + data.ipaddress + ":" + data.port + "/powerControl?ports=0";

        $.get(commandUrl,
            function (data) {
                if (data == "Success")
                {

                }
            });
    },

    openPower:function(data)
    {
        var commandUrl = "http://" + data.ipaddress + ":" + data.port + "/powerControl?ports=1";

        $.get(commandUrl,
            function (data) {
                if (data == "Success")
                {

                }
            });
    },

    editPower:function (data)
    {
            layer.open({
                title: ['电源编辑', 'font-size:13px;margin-top:10px;'],
                type: 2,
                area: ['600px', '500px'],
                content: 'power_add.html?code=' + data.code
            });
    },

    delePower:function (data)
    {
        var listParams = new Array();
        listParams[0] = "command=POWER_SET";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "code=" + data.code;
        postParm[2] = "state=0";

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/device/?" ,listParams);
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

    authTerminal:function (data)
    {
        var type = 0;
        if(data.authstate == 0)
        {
            type = 1;
        }
        else
        {
            type = 0;
        }

        var listParams = new Array();
        listParams[0] = "command=TERMINAL_AUTH";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "terminalcode=" + data.code;
        postParm[2] = "type=" + type;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/player/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    alert(data.ErrorInfo);
                    location.reload();
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    snapTerminal:function (data)
    {
        var newTmpLay = layer.open({
            title: ['远程截图', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            area:['1000px', '600px'],
            content: 'http://' + data.ipaddress +  ':' + "21233" + '/shotScreen?'
        });
    },

    bindBox:function (data)
    {
    },

    downloadTerminalLog:function (data)
    {
        // var newTmpLay = layer.open({
        //     title: ['远程查看日志', 'font-size:13px;margin-top:10px;font-weight:bold;'],
        //     type: 2,
        //     maxmin: true,
        //     area: ['1000px', '600px'],
        //     content: 'http://' + data.ipaddress + ':' + "21233" + '/manageLog?'
        // });
        window.open('http://' + data.ipaddress + ':' + "21233" + '/manageLog?');
    },
    updataButton:function (data) {
        layui.use('table', function () {
            var table = layui.table;
            var oldData = table.cache["testReload"];

            for (var index = 0; index < oldData.length; index ++)
            {
                var oneRecord = oldData[index];
            }
        });
    },
});