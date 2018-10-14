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

    editLight:function (data)
    {
            layer.open({
                title: ['灯光编辑', 'font-size:13px;margin-top:10px;'],
                type: 2,
                area: ['500px', '400px'],
                content: 'light_add.html?code=' + data.code
            });
    },

    deleLight:function (data)
    {
        var listParams = new Array();
        listParams[0] = "command=SET_DEVICE";
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
    
    mangeLocation:function (data) {
        var newTmpLay = layer.open({
            title: ['管理灯光位置', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            scrollbar: false,
            area:['800px', '600px'],
            content: 'set_position.html?code=' + data.orgcode + "&devcode=" + data.code + "&xpos=" + data.leftx+ "&ypos=" + data.lefty + "&haveimage=" + data.haveimg
        });
    },

    setPower:function (data) {
        // var newTmpLay = layer.open({
        //     title: ['管理灯光归属电源', 'font-size:13px;margin-top:10px;font-weight:bold;'],
        //     type: 2,
        //     maxmin: true,
        //     scrollbar: false,
        //     area: ['800px', '600px'],
        //     content: 'power_bind.html?code=' + data.code
        // });
        var newTmpLay = layer.open({
            title: ['管理灯光归属电源', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            scrollbar: false,
            area: ['800px', '600px'],
            content: 'power_bind.html?code=' + data.code + "&powercode=" + data.powercode + "&powerport=" + data.powerport
        });
    },

    setGroup:function (data) {
        alert("管理设备分组");
    },
});