#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""HsEduServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from SmartPaper.Api.Device.DeviceApi import *
from SmartPaper.Api.Device.GoodsApi import *

from SmartPaper.Api.Login.LoginApi import *
# from SmartPaper.Api.Policy.PolicyApi import *
from SmartPaper.Api.Privilege.PrivilegeApi import *
from SmartPaper.Api.System.SystemApi import *
# =====================
from SmartPaper.Api.Privilege.OrgPageRoute.OrgPageRoute import *
from SmartPaper.BaseMoudle.Task.TaskHelper import *

from SmartPaper.Api.OtherApi import *


# 启动定时任务
TaskHelper.startTask()


urlpatterns = []

# 登录
urlpatterns = urlpatterns + [
    # 缺省执行客户登录
    url(r'^$', LoginApi.openLoginHome),
    # 指定客户登录
    url(r'^login.html', LoginApi.openLoginHome),
    # 修改密码
    url(r'^change_password.html', LoginApi.goChangePassword),
    # 主页
    url(r'^index.html', LoginApi.goOrgHome),
    url(r'^home.html', OrgPageRoute.goHelpX),

    # 登录统一API
    url(r'^api/login/$', LoginApi.CommandDispatch),
]

# ################################################################################################################

# 机构管理&角色权限
urlpatterns = urlpatterns + [
    url(r'^org_list.html', PrivilegeApi.goOrgList),
    url(r'^org_add.html', PrivilegeApi.goOrgAdd),
    url(r'^account_list.html', PrivilegeApi.goAccountList),
    url(r'^account_add.html', PrivilegeApi.goAccountAdd),
    url(r'^role_list.html', PrivilegeApi.goRoleList),
    url(r'^role_add.html', PrivilegeApi.goRoleAdd),
    url(r'^account_config_role.html', PrivilegeApi.configUserRole),

    # API接口
    url(r'^api/org/$', PrivilegeApi.CommandDispatch),
]

# 终端管理
urlpatterns = urlpatterns + [
    # API接口
    url(r'^light_list.html', DeviceApi.goLightList),
    url(r'^light_add.html', DeviceApi.goLightAdd),
    url(r'^light_edit.html', DeviceApi.goLightEdit),

    url(r'^group_list.html', DeviceApi.goTerminalLedList),
    url(r'^group_add.html', DeviceApi.goTerminalAddLed),
    url(r'^group_edit.html', DeviceApi.goTerminalEditLed),
    url(r'^group_bind.html', DeviceApi.goGroupBind),


    url(r'^power_list.html', DeviceApi.goPowerList),
    url(r'^power_add.html', DeviceApi.goPowerAdd),
    url(r'^power_edit.html', DeviceApi.goPowerEdit),

    url(r'^led_list.html', DeviceApi.goLedList),
    url(r'^led_add.html', DeviceApi.goLedAdd),
    url(r'^led_edit.html', DeviceApi.goLedEdit),

    url(r'^base_device.html', DeviceApi.goTerminalList),
    url(r'^device_edit.html', DeviceApi.goTerminalEdit),

    url(r'^device_view.html', DeviceApi.goDeviceView),
    url(r'^goods_manage.html', DeviceApi.goGoodsView),
    url(r'^goods_add.html', DeviceApi.goAddGoods),

    url(r'^order_manage.html', DeviceApi.goOrderView),

    url(r'^message_config.html', SystemApi.openMessageConfig),




    url(r'^api/device/$', DeviceApi.CommandDispatch),
]


# 系统管理Api
urlpatterns = urlpatterns + [
    # API接口
    url(r'^resource_list.html', SystemApi.goResourceList),
    url(r'^log_query.html', SystemApi.goLogQuery),
    url(r'^resource_release.html', SystemApi.goResourceRelease),
    url(r'^config_list.html', SystemApi.goConfigList),
    url(r'^config_setting.html', SystemApi.goSettingConfig),


    url(r'^version_list.html', SystemApi.goVersionList),
    url(r'^version_add.html', SystemApi.goVersionAdd),
    url(r'^api/system/$', SystemApi.CommandDispatch),

    url(r'^uploadversion/$',SystemApi.uploadFile),
    url(r'^uploadgoods/$',GoodsApi.uploadGoodsData),
    url(r'^api/goods/$', GoodsApi.CommandDispatch),

    url(r'^set_goods.html', GoodsApi.goGoodsSetting),


    url(r'^upload/$',SystemApi.uploadSceenFile),

    url(r'^set_sceen.html', SystemApi.goSetSceen),


    # 启动时微信登录---等待页面
    url(r'^wait.html',OtherApi.openWaitPage),
    url(r'^get_free_paper.html',OtherApi.applyFreePaper),

    # url(r'^$',WebCenterApi.wxA),
    url(r'^shop.html',OtherApi.openShop),

    # url(r'^index.html',OtherApi.goHome),

]

# 告警Api
urlpatterns = urlpatterns + [
    # API接口
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

