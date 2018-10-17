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
    // refreshTime = setInterval("$.reloadData()",60000);
});

$.extend({
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    viewDevice:function (data) {
        var newTmpLay = layer.open({
            title: ['设备信息', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            scrollbar: false,
            area:['680px', '580px'],
            content: 'device_view.html?code=' + data.code
        });
    },

    editDevice:function (data) {
        var newTmpLay = layer.open({
            title: ['编辑设备', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            scrollbar: false,
            area:['520px', '700px'],
            content: 'device_edit.html?code=' + data.code
        });
    },

    deleDevice:function (data) {
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

    snapDevice:function (data) {
        var newTmpLay = layer.open({
            title: ['远程截图', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            area:['1000px', '600px'],
            content: 'http://' + data.ipaddress +  ':' + data.port + '/shotScreen?'
        });
    },

    restartDevice:function (data) {
        var urlCommad = "http://" + data.ipaddress + ":" + data.port + "/onRestart?";
        $.get(urlCommad, function (data, status) {
        });
    },

    shutdownDevice:function (data) {
        var urlCommad = "http://" + data.ipaddress + ":" + data.port +  "/onShutdown?";
        $.get(urlCommad, function (data, status) {
        });
    },

    setGoods:function (data) {
        var newTmpLay = layer.open({
            title: ['管理设备商品', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            maxmin:true,
            scrollbar: false,
            area:['700px', '350px'],
            content: 'set_goods.html?' + "code=" + data.code
        });
    },

    setDevPower:function (data) {
        var newTmpLay = layer.open({
            title: ['管理设备归属电源', 'font-size:13px;margin-top:10px;font-weight:bold;'],
            type: 2,
            scrollbar: false,
            area: ['800px', '600px'],
            content: 'power_bind.html?code=' + data.code + "&powercode=" + data.powercode + "&powerport=" + data.powerport
        });
    },
    setDevGrp:function (data) {
        alert("设置设备归属分组");
    },

    viewResource:function (mname,mphone,alginid) {
        var tipValue = null;

        tipValue = "管理员：" + mname ;
        tipValue = tipValue + "<br>联系电话：" + mphone ;


        layer.tips(tipValue, '#'+alginid, {
                tips: [3, '#0FA6D8'], //设置tips方向和颜色 类型：Number/Array，默认：2 tips层的私有参数。支持上右下左四个方向，通过1-4进行方向设定。如tips: 3则表示在元素的下面出现。有时你还可能会定义一些颜色，可以设定tips: [1, '#c00']
                tipsMore: false, //是否允许多个tips 类型：Boolean，默认：false 允许多个意味着不会销毁之前的tips层。通过tipsMore: true开启
                time:4000  //2秒后销毁，还有其他的基础参数可以设置。。。。这里就不添加了
            });
    },

    viewLocation:function (long,lant,alginid) {
        var tipValue = null;

        tipValue = "经度：" + long ;
        tipValue = tipValue + "<br>纬度：" + lant ;


        layer.tips(tipValue, '#'+alginid, {
                tips: [3, '#0FA6D8'], //设置tips方向和颜色 类型：Number/Array，默认：2 tips层的私有参数。支持上右下左四个方向，通过1-4进行方向设定。如tips: 3则表示在元素的下面出现。有时你还可能会定义一些颜色，可以设定tips: [1, '#c00']
                tipsMore: false, //是否允许多个tips 类型：Boolean，默认：false 允许多个意味着不会销毁之前的tips层。通过tipsMore: true开启
                time:4000  //2秒后销毁，还有其他的基础参数可以设置。。。。这里就不添加了
            });
    },
    closeResourceTips:function () {

    },
        openMap:function () {
        alert("暂不支持");
    },

});