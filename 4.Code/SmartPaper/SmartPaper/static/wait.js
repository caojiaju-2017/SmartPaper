var appID = "wx75e53a9db8f89fce";
var appsecret = "c45eefc37a8a0889fa4ebe020a9eb696";

window.onload=function()
{
    type = $.GetQueryString("type");
    type = parseInt (type);
    code = $.GetQueryString("code");

    if (type == 0)
    {
        $.getFreePaper(code);
    }
    else
    {
        $.weixinLogin();
    }

};

$(document).ready(function()
{
});

$.extend({
    weixinLogin:function () {
        // alert("wx:" + devcode);
            var urlCode = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + appID + "&redirect_uri=http%3a%2f%2fwww.h-sen.com/shop.html&response_type=code&scope=snsapi_userinfo&state=abc#wechat_redirect";
            location.href = urlCode;
        },

    getFreePaper:function(devcode)
    {
        location.href = "get_free_paper.html?code=" + devcode;
    },

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },
});
