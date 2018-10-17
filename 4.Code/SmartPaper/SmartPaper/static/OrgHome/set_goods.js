var code = "";

var itemTemplate = "<option value='{orgcode}'>{orgname}</option>";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    $.loadBoxData(null);

});

$.extend({

    loadDevGoodsInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=QUERY_DEVICE_GOODS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + $.cookie("OrgUserCode");
        listParams[4] = "devcode=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/goods/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                $.fillElement(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    fillElement:function (datas) {

        for (oneKey in datas) {
            values = datas[oneKey];

            $("#goods_list" + oneKey).val(values[0]);
            $("#number" + oneKey).val(values[1]);
        }
        layui.use('form', function () {
            var form = layui.form; //
            form.render('select');
        });
    },
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
    loadBoxData: function (orgparam) {
        var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign="  + $.cookie("OrgUserCode");
        listParams[4] = "type=7";

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?", listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                for (var index = 0; index < data.length; index++) {
                    var readyText = $("#goods_list1").html();

                    var oneOrg = data[index];
                    var abcTemp = {};
                    abcTemp["orgcode"] = oneOrg.id;
                    abcTemp["orgname"] = oneOrg.name;

                    var tempalteResult = $.format(itemTemplate, abcTemp);

                    $("#goods_list1").html(readyText + tempalteResult);
                    $("#goods_list2").html(readyText + tempalteResult);
                    $("#goods_list3").html(readyText + tempalteResult);
                    $("#goods_list4").html(readyText + tempalteResult);

                    // if (code != null && orgparam != null)
                    // {
                    //     $("#goods_list").find("option[value = '"+orgparam+"']").attr("selected","selected");
                    // }
                }

                layui.use('layer', function () {
                    layui.use('form', function () {
                        var form = layui.form; //只有执行了这一步，部分表单元素才会自动修饰成功
                        form.render();
                    });

                });

                $.loadDevGoodsInfo(code);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    clearGoodes :function(inx)
    {
        // post参数
        var postParm = new Array();
        postParm[0] = "devcode=" + code;
        postParm[1] = "trackid=" + inx;

        var listParams = new Array();
        listParams[0] = "command=CLEAR_DEVICE_GOODS";
        listParams[1] = "logincode=" + $.cookie("OrgUserCode");

        var urlCmd = $.buildGetParam("/api/goods/?" ,listParams);

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
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },

    setTrackGoods: function (inx) {
        var goodsCode = $("#goods_list" + inx).val();
        var goodsCount = $("#number" + inx).val();
        if (goodsCode == "")
        {
            alert("信息不能为空");
            return;
        }

        if (goodsCode == "null")
        {
            $.clearGoodes(inx)
            return
        }
        if (goodsCount == "")
        {
            alert("信息不能为空");
            return;
        }

        // post参数
        var postParm = new Array();
        postParm[0] = "devcode=" + code;
        postParm[1] = "goodscode=" + goodsCode;
        postParm[2] = "count=" + goodsCount;
        postParm[3] = "trackid=" + inx;

        var listParams = new Array();

        listParams[0] = "command=BIND_DEVICE_GOODS";
        listParams[1] = "logincode=" + $.cookie("OrgUserCode");


        // var allParams = listParams.concat(postParm);
        // allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/goods/?" ,listParams);
        // urlCmd = urlCmd + "&sign=" + $.signString(allParams);

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

                    // var index = parent.layer.getFrameIndex(window.name);
                    // parent.layer.close(index);
                    // parent.location.reload();
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});