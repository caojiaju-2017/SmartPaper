var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var porgCode = "";
window.onload=function()
{
};

$(document).ready(function(e) {
    code = $.GetQueryString("code");
    porgCode = $.GetQueryString("pcode");

    if (code != "" && code != "null" && code != null)
    {
        $.loadCustomInfo(code);
    }
    else
    {
        //$.initTestData();
    }

    // $.loadBoxData();
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

    loadBoxData:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=0";

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                //console.
                alert(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    loadCustomInfo:function(code)
    {
        var listParams = new Array();
        listParams[0] = "command=QUERY_ORG";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
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
                    $("#conname").val(datas.contactname);
                    $("#conphone").val(datas.contactphone);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    initTestData:function(){
        // $("#orgname").val("建设银行四川分行");
        // $("#conname").val("黄薇");
        // $("#conphone").val("028-56903218");
    },

    clearValue:function () {
        $("#orgname").val("");
        $("#conname").val("");
        $("#conphone").val("");
    },

    saveInfo: function () {
        var orgname = $("#orgname").val();
        var conname = $("#conname").val();
        var conphone = $("#conphone").val();

        if (orgname == "" || orgname.length <= 0)
        {
            alert("必须指定单位名称");
            return;
        }

        var listParams = new Array();
        if (code != "" && code != "null" && code != null) {
            listParams[0] = "command=ORG_MODI_ORG";
        }
        else
        {
            listParams[0] = "command=ORG_ADD_ORG";
        }
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        if (code != "" && code != "null" && code != null) {
            postParm[0] = "name=" + orgname;
            postParm[1] = "conname=" + conname;
            postParm[2] = "conphone=" + conphone;
            postParm[3] = "orgsign=" + code;
            // postParm[4] = "parentcode=";
        }
        else
        {
            postParm[0] = "name=" + orgname;
            postParm[1] = "conname=" + conname ;
            postParm[2] = "conphone=" + conphone ;
            postParm[3] = "parentcode=" + porgCode;
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
                    // if (code != "" && code != "null" && code != null)
                    // {
                        var index = parent.layer.getFrameIndex(window.name);
                        parent.layer.close(index);
                        parent.location.reload();
                    // }
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
});