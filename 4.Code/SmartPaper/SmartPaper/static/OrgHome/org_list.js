var openidTemp;
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var currentSign = null;
window.onload=function()
{
    var docHeight = $(document).height();
    $("#vip_div").height(docHeight - 60);

    $("#left_org_tree").height(docHeight);
};

$(window).resize(function() {
    window.location.reload();
});

$(document).ready(function(e) {
    // 如果cookie已超时，则返回登陆页面
    $.loadSrvOrgTree();
});

$.extend({
    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    getTestOrg:function () {
        return [{ //节点
            name: '父节点1'
            , children: [{
                name: '子节点11'
            }, {
                name: '子节点12'
            }]
        }, {
            name: '父节点2'
            , children: [{
                name: '子节点21qqq'
            }]
        }];
    },
    loadSrvOrgTree:function()
    {
       var listParams = new Array();
        listParams[0] = "command=GET_ORG_TREE";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                loadOrgTree(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    removeOrgCustom:function(data){
        var listParams = new Array();
        listParams[0] = "command=ORG_UNREGISTER";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + data.code;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        $.post(urlCmd,params,
            function (data)
            {

                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {
                    //alert("删除成功!");
                    // $.loadSrvOrgTree();
                    location.reload()
                }
                else
                {
                    alert(data.ErrorInfo);
                }

            },
            "json");
    },
    modiCustom:function(data)
    {
        layer.open({
            title: ['修改单位信息', 'font-size:13px;margin-top:10px;'],
            type: 2,
            area: ['400px', '300px'],
            content: 'org_add.html?code='+ data.code
        });
    },

    createOrg:function (pcode) {
        if (pcode == null && currentSign != null )
        {
            pcode = currentSign;
        }
        else if (pcode != null)
        {

        }
        else
        {
            pcode = orgsign;
        }
        layer.open({
            title: ['添加单位', 'font-size:13px;margin-top:10px;'],
            type: 2,
            area: ['400px', '300px'],
            content: 'org_add.html?pcode=' + pcode
        });
    }
});