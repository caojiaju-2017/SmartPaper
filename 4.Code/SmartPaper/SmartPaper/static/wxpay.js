$.extend({
    notifyServer: function (codeName) {
        // alert(codeName);
        var openid = $.cookie("OpenId");
        var rtnCmd = "/api/ctm/?Command=WX_PAY_SUCCESS";

        $.post(rtnCmd, {ordercoce: codeName, openid: openid},
            function (data)
            {
                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200)
                {                }
                else
                {
                    alert(data.ErrorInfo);
                }
                location.replace('./order_detail_info.html?Command=View_Order&code={{ ResCode }}');
            },
            "json");//这里返回的类型有：json,html,xml,text
    },
});