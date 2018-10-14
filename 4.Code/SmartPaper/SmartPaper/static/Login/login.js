// var orgsign= "1e2c68303ebd11e880d3989096c1d848";
window.onload=function()
{
};

$(document).ready(function(e) {
    //
    var userName = $.cookie("OrgUserCode");
    var userPassword = $.cookie("UserPassword");

    $("#username").val(userName);
    $("#password").val(userPassword);
});

$.extend({
    checkLogin: function () {
        // location.href = "./index.html?logincode=" + username + "&orgsign=" + orgsign;

        // 获取账户信息
        var username = $("#username").val();
        var passwordInput = $("#password").val();

        var listParams = new Array();
        listParams[0] = "command=NORMAL_LOGIN";
        var timestamp = (new Date()).valueOf();
        listParams[1] = "account=" + username;
        var password = $.md5(passwordInput);
        listParams[2] = "password=" + password;
        listParams = listParams.sort();
        console.log(password);
        // var rtnCmd = "/api/login/?command=NORMAL_LOGIN&timestamp=" + timestamp;
        var rtnCmd = "/api/login/?command=NORMAL_LOGIN" ;

        // rtnCmd = rtnCmd + "&sign=" + $.signString(listParams);

        var params = {account: username, password: password};
        // var params = {account: username, password: password,orgsign:orgsign};
        $.post(rtnCmd, params,
            function (data)
            {
                var  ErrorId = data.ErrorId;
                var  Result = data.Result;

                if (ErrorId == 200) {
                    // 记录当前登录COOKIE
                    $.cookie("OrgUserCode", username);
                    $.cookie("OrgUserAlias", Result);

                    var checkFlag = $("#remember_me").get(0).checked;
                    if (checkFlag) {
                        $.cookie("UserPassword", passwordInput);
                    }
                    else
                    {
                        $.cookie("UserPassword", "");

                    }
                    // location.href = "./index.html?logincode=" + username + "&orgsign=" + orgsign;
                    location.href = "./index.html?logincode=" + username;

                }
                else
                {
                    alert(data.ErrorInfo);
                }
            },
            "json");
    },
});