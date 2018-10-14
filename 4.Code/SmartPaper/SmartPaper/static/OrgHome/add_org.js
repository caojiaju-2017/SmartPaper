var code = "";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");

    if (code != "" && code != "null" && code != null)
    {
        $.loadCustomInfo(code);
    }
    else
    {
        //$.initTestData();
    }

});

$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    selectVipImage: function () {
        if (code == "" || code == "null" || code == null )
        {
            alert("请先创建账户，并保存。")
            return;
        }


    },

    getVipCode:function(){
      return code;
    },
    loadCustomInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=QUERY_ORG";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("LoginCode");
        listParams[3] = "orgsign=" + code;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                    datas = data.Result;
                // 检查查询状态
                    code = datas.code;
                    $("#orgname").val(datas.name);
                    $("#manageaccount").val(datas.maccount);
                    $("#password").val("000000");
                    $("#orgaddress").val("");
                    $("#conname").val(datas.contactname);
                    $("#conphone").val(datas.contactphone);

                    if (datas.maccount != "noset")
                    {
                        $("#manageaccount").attr("disabled","disabled");
                        $("#password").attr("disabled","disabled");
                    }

                    // $("#password").attr("disabled","disabled");
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    initTestData:function(){
        $("#orgname").val("建设银行四川分行");
        $("#manageaccount").val("jsadmin");
        $("#password").val("123456");
        $("#orgaddress").val("四川省成都市总府路109号");
        $("#conname").val("黄薇");
        $("#conphone").val("028-56903218");

    },

    clearValue:function () {
        $("#orgname").val("");
        $("#manageaccount").val("");
        $("#password").val("");
        $("#orgaddress").val("");
        $("#conname").val("");
        $("#conphone").val("");
    },

    saveInfo: function () {
        var orgname = $("#orgname").val();
        var manageaccount = $("#manageaccount").val();
        var password = $("#password").val();
        var orgaddress = $("#orgaddress").val();
        var conname = $("#conname").val();
        var conphone = $("#conphone").val();

        password = $.md5(password);

        var listParams = new Array();
        if (code != "" && code != "null" && code != null) {
            listParams[0] = "command=ORG_MODI";
        }
        else
        {
            listParams[0] = "command=ORG_REGISTER";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("LoginCode");

        var postParm = new Array();
        if (code != "" && code != "null" && code != null) {
        postParm[0] = "name=" + orgname;
        postParm[1] = "address=" + orgaddress ;
        postParm[2] = "conname=" + conname ;
        postParm[3] = "conphone=" + conphone ;
        postParm[4] = "orgsign=" + code ;

        }
        else
        {
            postParm[0] = "account=" + manageaccount;
            postParm[1] = "password="  + password;
            postParm[2] = "name=" + orgname;
            postParm[3] = "address=" + orgaddress ;
            postParm[4] = "conname=" + conname ;
            postParm[5] = "conphone=" + conphone ;
            postParm[6] = "type=1" ;
            postParm[7] = "parentcode=" ;
        }


        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();
        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
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
                    $.clearValue();
                    alert("操作成功!");
                    if (code != "" && code != "null" && code != null)
                    {
                        var index = parent.layer.getFrameIndex(window.name);
                        parent.layer.close(index);
                        parent.location.reload();
                    }
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});