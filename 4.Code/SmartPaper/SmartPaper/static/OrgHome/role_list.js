var openidTemp;
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
var functions = [];
var selectRoleData = null;
var itemTemplate = "  <div class=\"layui-form-item\" pane=\"\">\n" +
    "    <label class=\"layui-form-label\" style='width: 160px'>{functionname}</label>\n" +
    "    <div class=\"layui-input-block\" id='{fuctioncode}'>\n" +
    "      <input type=\"checkbox\"  id='{fuctioncode}_all' lay-filter=\"functionCk\" name=\"like1[all]\" lay-skin=\"primary\" title=\"所有\" {allpriv}>\n" +
    "      <input disabled='disabled' id='{fuctioncode}_query' lay-filter=\"functionCk\" type=\"checkbox\" name=\"like1[query]\" lay-skin=\"primary\" title=\"查询\" {querypriv}>\n" +
    "      <input disabled='disabled' id='{fuctioncode}_add' lay-filter=\"functionCk\" type=\"checkbox\" name=\"like1[add]\" lay-skin=\"primary\" title=\"新增\" {addpriv}>\n" +
    "      <input disabled='disabled' id='{fuctioncode}_modi' lay-filter=\"functionCk\" type=\"checkbox\" name=\"like1[modi]\" lay-skin=\"primary\" title=\"修改\" {modipriv}>\n" +
    "      <input disabled='disabled' id='{fuctioncode}_dele' lay-filter=\"functionCk\" type=\"checkbox\" name=\"like1[dele]\" lay-skin=\"primary\" title=\"删除\" {delepriv}>\n" +
    "    </div>\n" +
    "  </div>";
window.onload=function()
{
    var docHeight = $(document).height();
    $("#vip_div").height(docHeight - 60);
};

$(window).resize(function() {
    window.location.reload();
});

$(document).ready(function(e) {
    $.loSmartControlDatas();

    $.loSmartControlFuncsDatas();
});

$.extend({
    loSmartControlFuncsDatas:function()
    {
       var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=2" ;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                functions = data;
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    queryRoleFunction:function(node)
    {
        var listParams = new Array();
        listParams[0] = "command=ROLE_QUERY";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "rolecode=" + node.id;
        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                // alert(data);
                $.loadNodeFuncs(node,data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
    loadNodeFuncs:function(node, roleFuncDatas)
    {
        if (functions == null)
        {
            return;
        }
        $("#priv_detail").html("<div id=\"role_name\" style=\"margin-top: 30px;font-size: 28px;color: #444444\"></div>");

        $("#role_name").text(node.name);

        var funcsLen = functions.length;

         for (var index  = 0 ; index < funcsLen; index ++)
         {
             var oneData = functions[index];

             var confData = null;

             for (var inx = 0 ; inx < roleFuncDatas.length; inx ++)
             {
                 var conf = roleFuncDatas[inx];

                 if (conf.code == oneData.id)
                 {
                     confData = conf;
                     break;
                 }
             }

             var readyText = $("#priv_detail").html();
             var abcTemp = {};
             abcTemp["functionname"] = oneData.name;
             abcTemp["fuctioncode"] = oneData.id;
             abcTemp["querypriv"] = $.getPrivItem(confData,0);
             abcTemp["addpriv"] = $.getPrivItem(confData,1);
             abcTemp["modipriv"] = $.getPrivItem(confData,2);
             abcTemp["delepriv"] = $.getPrivItem(confData,3);

             abcTemp["allpriv"] = $.isHaveSelAny(confData);

             var tempalteResult = $.format(itemTemplate, abcTemp);

             $("#priv_detail").html(readyText + tempalteResult);
         }
         selectRoleData = node;

        layui.use('layer', function () {
                    layui.use('form', function () {
                        var form = layui.form; //只有执行了这一步，部分表单元素才会自动修饰成功
                        form.render();

                        form.on('checkbox(functionCk)', function (data) {

                            var eleCheck = data.elem.checked;

                            var index = data.elem.id.indexOf("_");

                            var preString = null;
                            if (index >= 0)
                            {
                                preString = data.elem.id.substring(0,index);
                            }
                            else
                            {
                                preString = data.elem.id;
                            }

                            $("#" + preString + "_query").prop("checked", eleCheck);
                            $("#" + preString + "_add").prop("checked", eleCheck);
                            $("#" + preString + "_modi").prop("checked", eleCheck);
                            $("#" + preString + "_dele").prop("checked", eleCheck);

                            form.render();
                        });
                    });

                });
    },
    getPrivItem:function (data,pos) {
        //'checked=""'
        if (data == "" || data == null || data == "undefined")
        {
            return ""
        }
        var flag = data.flag;
        var valueS = flag.charAt(pos);

        if (valueS == 1)
        {
            return 'checked=""';
        }
        return "";
    },
    isHaveSelAny:function (data) {
        //'checked=""'
        if (data == "" || data == null || data == "undefined")
        {
            return ""
        }
        var flag = data.flag;
        var value0 = flag.charAt(0);
        var value1 = flag.charAt(1);
        var value2 = flag.charAt(2);
        var value3 = flag.charAt(3);

        if (value0 == 1 || value1 == 1 || value2 == 1 || value3 == 1)
        {
            return 'checked=""';
        }
        return "";
    },
    loSmartControlDatas:function()
    {
       var listParams = new Array();
        listParams[0] = "command=GET_DATAS";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");
        listParams[3] = "orgsign=" + orgsign;
        listParams[4] = "type=1" ;

        var allParams = listParams;
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/system/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        // 提取用户名
        $.get(urlCmd,
            function (data) {
                // $("#RoleTree").innerText = "";
                loadRoleTree(data);
            },
            "json");//这里返回的类型有：json,html,xml,text
    },

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

    removeRole:function(data){
        if (selectRoleData == null) {
            $.showMsg(layer,"未选中角色");
            return;
        }




        var listParams = new Array();
        listParams[0] = "command=ROLE_DELE";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "rolecode=" + selectRoleData.id;
        postParm[1] = "orgsign=" + orgsign;

        var allParams = listParams.concat(postParm);
        allParams = allParams.sort();

        var urlCmd = $.buildGetParam("/api/org/?" ,listParams);
        urlCmd = urlCmd + "&sign=" + $.signString(allParams);

        params = $.buildPostParam(postParm);

        layer.confirm('你确定删除该角色？', function (index) {
            layer.close(index);

            $.post(urlCmd, params,
                function (data) {

                    var ErrorId = data.ErrorId;
                    var Result = data.Result;

                    if (ErrorId == 200) {

                        $.loSmartControlDatas();
                    }
                    else {
                        alert(data.ErrorInfo);
                    }

                },
                "json");
        });
    },
    modiRole:function(data)
    {
        layer.open({
            title: ['修改角色', 'font-size:13px;margin-top:10px;'],
            type: 2,
            area: ['400px', '500px'],
            content: 'role_add.html?orgsign='+ orgsign + "&code=" + data.code
        });
    },

    saveRole:function()
    {
        if (selectRoleData == null)
        {
            alert("未选中角色");
            return;
        }

        var listParams = new Array();
        listParams[0] = "command=ROLE_MODI";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "timestamp=" + timestamp;
        listParams[2] = "logincode=" + $.cookie("OrgUserCode");

        var postParm = new Array();
        postParm[0] = "orgsign=" + orgsign;
        postParm[1] = "funcs=" + $.getConfigUpdate();
        postParm[2] = "rolecode=" + selectRoleData.id;

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

    getConfigUpdate:function()
    {
        var funcsLen = functions.length;


        var rtnPriv = null;
         for (var index  = 0 ; index < funcsLen; index ++) {
             var oneData = functions[index];
             var boxList = $("#" + oneData.id).children();
             var rtnPrivTemplate = "000000000000";

             for (var inx = 0 ; inx < boxList.length; inx ++)
             {
                 var oneCheck = boxList[inx];

                 try {
                     var childrenName = oneCheck.name;
                     if (childrenName.indexOf("like1") != -1) {
                          if (childrenName.indexOf('query') != -1)
                          {
                                if (oneCheck.checked)
                                {
                                    rtnPrivTemplate = "1" + rtnPrivTemplate.substring(1,rtnPrivTemplate.length);
                                }
                          }
                          else if (childrenName.indexOf('add') != -1)
                          {
                                if (oneCheck.checked)
                                {
                                    rtnPrivTemplate = rtnPrivTemplate.substring(0,1) + "1" + rtnPrivTemplate.substring(2,rtnPrivTemplate.length);
                                }
                          }
                          else if (childrenName.indexOf('modi') != -1)
                          {
                                if (oneCheck.checked)
                                {
                                    rtnPrivTemplate = rtnPrivTemplate.substring(0,2) + "1" + rtnPrivTemplate.substring(3,rtnPrivTemplate.length);
                                }
                          }
                          else if (childrenName.indexOf('dele') != -1)
                          {
                                if (oneCheck.checked)
                                {
                                    rtnPrivTemplate = rtnPrivTemplate.substring(0,3) + "1" + rtnPrivTemplate.substring(4,rtnPrivTemplate.length);
                                }
                          }
                     }
                 }
                 catch(e)
                 {
                     
                 }
                 // console.log(className);
                 //
             }

             if (rtnPriv != null)
             {
                rtnPriv = rtnPriv + ","  + oneData.id + ":" + rtnPrivTemplate;
             }
            else
             {
                 rtnPriv = oneData.id + ":" + rtnPrivTemplate;
             }

         }

         console.log(rtnPriv);

         return rtnPriv;
    },

});