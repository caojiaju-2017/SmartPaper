var openId;
var openName;
var openHeadImage;

var currentType = 10;

var isResLoadFinishLoad = false;
var currentResLoadPageIndex = 0;
var currentResLoadPageSize = 10;
var queryResLoadLock = false;

var oneResourceTmpl = "<a onclick=\"$.openResourceDetail('{Code}')\" class=\"list-group-item row\"\n" +
    "                   style=\"height: 260px;padding-left: 0px;padding-right: 0px;margin-top: 10px\">\n" +
    "                    <div class=\"col-xs-4 col-sm-4 col-md4 img text-center\"\n" +
    "                         style=\"height: 100%\">\n" +
    "                        <img src=\"/static/Images/ResImage/{ResImage}\" class=\"img-thumbnail\"\n" +
    "                             style=\"margin-left: 0px;position: relative;top: 50%;transform: translateY(-50%);width: 94%;height: 80%;border-radius: 20px\"/>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-xs-5 col-sm-5 col-md5\" style=\";padding-left: 0px;padding-right: 0px\">\n" +
    "                        <div class=\"col-xs-12 col-sm-12 col-md12\" style=\"margin-top: 20px\">\n" +
    "                            <span class=\"label label-primary\" style=\"font-size: 25px\">{ResGrade}</span>\n" +
    "                            <span class=\"label label-success\" style=\"font-size: 25px\">{ResLevel}</span>\n" +
    "                            <span class=\"label label-info\" style=\"font-size: 25px\">{ResClass}</span>\n" +
    "                        </div>\n" +
    "\n" +
    "                        <div class=\"col-xs-12 col-sm-12 col-md12\"\n" +
    "                             style=\"font-size: 30px;padding-left: 20px;color: #000;margin-top: 20px;color: #606060\">\n" +
    "                            {ResTitle}\n" +
    "                        </div>\n" +
        "                    <div class=\"col-xs-12 col-sm-12 col-md12\"\n" +
    "                             style=\"font-size: 30px;padding-left: 20px;color: #000;margin-top: 20px;color: #606060\">\n" +
    "                            学习人数：{BuyCount} 人\n" +
    "                        </div>\n" +
        "                    <div class=\"col-xs-12 col-sm-12 col-md12\"\n" +
    "                             style=\"font-size: 30px;padding-left: 20px;color: #000;margin-top: 20px;color: #606060\">\n" +
    "                            课时数：{ResItemCount} 课时\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div class=\"col-xs-3 col-sm-3 col-md3 time\"\n" +
    "                         style=\"font-size: 30px;padding-left: 0px;padding-right: 0px;height: 100%\">\n" +
    "                        <div class=\"col-xs-12 col-sm-12 col-md12\" style=\"color: #000;height: 40px;margin-top: 20px\">\n" +
    "                            {Name}\n" +
    "                        </div>\n" +
    "                        <div class=\"col-xs-12 col-sm-12 col-md12\" style=\"color: #ec971f ;height: 40px;margin-top: 20px\">\n" +
    "                            价格：{Price}元\n" +
    "                        </div>\n" +
    "\n" +
    "                    <div class=\"col-xs-12 col-sm-12 col-md12 img buy-center\"\n" +
    "                         style=\"background-color: #d58512;color: white;height: 60px;width: 80%;border-radius: " +
    "10px;font-size: 36px;text-align: center;line-height: 60px;margin-top: 40px\">\n" +
    "查看详情"+
    "                    </div>\n" +

    "                    </div>\n" +
    "\n" +
    "                </a>";

var bottomSep = '<div style="height: 110px;width: 100%"></div>';
window.onload = function () {

};

$(document).ready(function () {
    // $.initLoading();
    // $(window).scroll(function () {
    //     var srollPos = $(window).scrollTop();
    //     var documentHd = $(document).height();
    //     var winHd = $(window).height();
    //
    //
    //     totalheight = parseFloat($(window).height()) + parseFloat(srollPos);
    //
    //     if (srollPos + winHd > documentHd * 0.9) {
    //         // alert(currentType);
    //         if (currentType > 9) {
    //             return;
    //         }
    //
    //         if (!isResLoadFinishLoad && !queryResLoadLock) {
    //                 queryResLoadLock = true;
    //                 // 加载数据
    //                 currentResLoadPageIndex = currentResLoadPageIndex + 1;
    //                 $.searchResource();
    //             }
    //     }
    // });
    // $.loadFirstData();
});

$.extend({
    setUserInfo: function (openid, username, headimg) {
        $.cookie("OpenId", openid);
        $.cookie("WxName", username);
        $.cookie("HeadImg", headimg);

        //    设置头像数据
        $("#uName").text(username);
        $("#user_head").attr('src', headimg);
    },
    showResource: function (index) {
        currentType = index;
        // alert(currentType);
        $.cookie("BrowserIndex", currentType);
        // 设置背景色
        $("#abc_" + 1).css("color","#4C555A");
        $("#abc_" + 2).css("color","#4C555A");
        $("#abc_" + 3).css("color","#4C555A");
        $("#abc_" + 4).css("color","#4C555A");
        $("#abc_" + 10).css("color","#4C555A");

        $("#abc_" + 1).css("background-color","#FFFFFF");
        $("#abc_" + 2).css("background-color","#FFFFFF");
        $("#abc_" + 3).css("background-color","#FFFFFF");
        $("#abc_" + 4).css("background-color","#FFFFFF");
        $("#abc_" + 10).css("background-color","#FFFFFF");

        $("#abc_" + currentType).css("color","#FFFFFF");
        $("#abc_" + currentType).css("background-color","#06BBD0");


        if (index > 9)
        {
            $("#res_div").hide();
            $("#usercenter_div").show();
            $.showUser();
        }
        else
        {
            $("#res_div").show();
            $("#usercenter_div").hide();
            $.beginSearch();
        }

    },
    loadFirstData:function () {
        $.showResource(currentType);
    },
    getMyOrder: function () {
        //javascrtpt:window.parent.location.href='./res_order.html?Command=Get_Orders&Type=1'
        var openId = $.cookie("OpenId");
        location.href = './res_order.html?Command=Get_Orders&Type=1&openId=' + openId;
    },
    showUser: function () {
        $("#res_div").hide();
        $("#usercenter_div").show();
        currentType = 10;
    },
    // openNews: function (codeName) {
    //     window.location = "/view_news.html?Command=View_News&Code=" + codeName;
    // },
    StringFormat: function () {
        if (arguments.length == 0)
            return null;
        var str = arguments[0];
        for (var i = 1; i < arguments.length; i++) {
            var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
            str = str.replace(re, arguments[i]);
        }
        return str;
    },
    format: function (source, args) {
        var result = source;
        if (typeof(args) == "object") {
            if (args.length == undefined) {
                for (var key in args) {
                    if (args[key] != undefined) {
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            } else {
                for (var i = 0; i < args.length; i++) {
                    if (args[i] != undefined) {
                        var reg = new RegExp("({[" + i + "]})", "g");
                        result = result.replace(reg, args[i]);
                    }
                }
            }
        }
        return result;
    },

    changeSelect: function (btnId, selVal) {
        $("#" + btnId).html(selVal + "<span class=\"caret\"></span>");
    },
    get_resquery_cmd: function (filter) {

        var rtnCmd = "/api/ctm/?Command=Query_Res&pageindex={0}&pagesize={1}&filter={2}&subject={3}";
        rtnCmd = $.StringFormat(rtnCmd, currentResLoadPageIndex, currentResLoadPageSize, filter,currentType);
        return rtnCmd;
    },
    initLoading:function () {
        $("body").append("<!-- loading -->" +
            "<div class='modal fade' id='loading' tabindex='-1' role='dialog' aria-labelledby='myModalLabel' data-backdrop='static'>" +
            "<div class='modal-dialog' role='document'>" +
            "<div class='modal-content'>" +
            "<div class='modal-header'>" +
            "<h4 class='modal-title' id='myModalLabel' style='font-size: 32px'>提示</h4>" +
            "</div>" +
            "<div id='loadingText' class='modal-body' style='font-size: 36px'>" +

            "数据处理中，请稍候 . . ." +
            "</div>" +
            "</div>" +
            "</div>" +
            "</div>"
        );
    },
    searchResource: function () {
        var fliter = $("#fliter_input").val();

        // 准备发送查询指令
        var cmdString = $.get_resquery_cmd(fliter);
        // alert(cmdString);
        // 提取用户名
        $("#loading").modal("show");
        $.get(cmdString,
            function (data) {
                // 检查查询状态
                var ErrorId = data.ErrorId;
                var Result = data.Result;
                var Datas = Result;
                $("#loading").modal("hide");
                if (ErrorId == 200) {
                    if (Datas.length <= 0 || Datas.length < currentResLoadPageSize) {
                        isResLoadFinishLoad = true;
                    }

                    for (i = 0; i < Datas.length; i++) {
                        var oneCode1 = Datas[i];

                        var abcTemp = {};
                        abcTemp["ResGrade"] = oneCode1.ResGrade;
                        abcTemp["ResLevel"] = oneCode1.ResLevel;
                        abcTemp["ResClass"] = oneCode1.ResClass;
                        abcTemp["ResInfo"] = oneCode1.ResInfo;
                        abcTemp["Name"] = oneCode1.Name;
                        abcTemp["Price"] = oneCode1.Price;
                        abcTemp["ViewCount"] = oneCode1.ViewCount;
                        abcTemp["BuyCount"] = oneCode1.BuyCount;
                        abcTemp["ResImage"] = oneCode1.ResImage;
                        abcTemp["Code"] = oneCode1.Code;
                        abcTemp["ResTitle"] = oneCode1.ResTitle;
                        abcTemp["ResItemCount"] = oneCode1.ResItemCount;
                        var oneT = $("#res_item_div").html();

                        $("#res_item_div").html(oneT + $.format(oneResourceTmpl, abcTemp));
                    }
                    queryResLoadLock = false;
                }

            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    beginSearch: function () {
        isResLoadFinishLoad = false;
        currentResLoadPageIndex = 0;
        currentResLoadPageSize = 10;
        queryResLoadLock = false;
        $("#res_item_div").html("");
        $.searchResource();

    },
    openENGame: function () {
        var openId = $.cookie("OpenId");
        location.href = './game_home.html?Command=Open_ENGame' + "&openid=" + openId;
    },
});
