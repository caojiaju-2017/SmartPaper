var orgsign= "1e2c68303ebd11e880d3989096c1d848";
$(document).on('click', ".menuitem", function (e) {
    var titleName = e.target.innerText;
    var titleCode = $.md5(titleName);
    openTab (titleName,titleCode,getTabUrl(titleName));
});
function getTabUrl(tabname) {
    if (tabname == "单位管理")
    {
        return "./org_list.html";
    }
    else if (tabname == "角色管理")
    {
        return "./role_list.html";
    }
    else if (tabname == "账户管理")
    {
        return "./account_list.html?logincode=" + $.cookie("OrgUserCode") + "&orgsign=" + orgsign;
    }
    else if (tabname == "基础设备")
    {
        return "./base_device.html";
    }
    else if (tabname == "电源管理")
    {
        return "./power_list.html";
    }
    else if (tabname == "灯光管理")
    {
        return "./light_list.html";
    }
    else if (tabname == "LED管理")
    {
        return "./led_list.html";
    }
    else if (tabname == "分区管理")
    {
        return "./group_list.html";
    }
    else if (tabname == "策略管理")
    {
        return "./strategys_list.html";
    }
    else if (tabname == "日志查询")
    {
        return "./log_query.html";
    }
    else
    {
        return "./org_list.html";
    }
}
function openTab(title, code,url)
{
        var element = layui.element;
        var $ = jQuery = layui.jquery;

        var isOpen = false;
        $.each($(".layui-tab-title li[lay-id]"), function () {
            if ($(this).attr("lay-id") == code) {
                isOpen = true;
            }
        });
        if (!isOpen) {
            element.tabAdd('showbody', {
                title: title //用于演示
                , content: '<iframe src=' + url + ' style="overflow: hidden;border:0px solid #ccc"></iframe>'
                , id: code //实际使用一般是规定好的id，这里以时间戳模拟下
            });
        }

        FrameWH();
        element.tabChange('showbody', code);
}

function FrameWH() {
    var h = $(window).height() - 41 - 10 - 60 - 10 - 44 - 30;
    var rightWd = $("#right-layout").width();
    var w = $(window).width() - rightWd - 65;
    $("iframe").css("height", h + "px");
    $("iframe").css("width", w + "px");
}

$(window).resize(function () {
    FrameWH();
});

function goChangePassword()
{
    layui.use('layer', function () {
        var layer = layui.layer;
        layer.open({
            title: ['修改密码', 'font-size:13px;margin-top:10px;'],
            type: 2,
            area: ['400px', '350px'],
            content: 'change_password.html'
        });
    });

}