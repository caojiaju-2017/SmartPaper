#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.Api.Privilege import *
from SmartPaper.Api.Privilege.OrgTree import *

class PrivilegeApi(object):
    Org_Cmds=[]
    Org_Cmds.append('ORG_REGISTER')
    Org_Cmds.append('ORG_MODI')
    Org_Cmds.append('LIST_ORGS')
    Org_Cmds.append('ORG_UNREGISTER')
    Org_Cmds.append('ORG_CONFIG')
    Org_Cmds.append('QUERY_ORG')
    Org_Cmds.append('GET_ORG_TREE')
    Org_Cmds.append('ORG_ADD_ORG')
    Org_Cmds.append('ORG_MODI_ORG')

    Role_Cmds = []
    Role_Cmds.append('ROLE_ADD')
    Role_Cmds.append('ROLE_MODI')
    Role_Cmds.append('ROLE_DELE')
    Role_Cmds.append('ROLE_SET')
    Role_Cmds.append('ROLE_LIST_USERS')
    Role_Cmds.append('AD_AUDIT')
    Role_Cmds.append('ROLE_QUERY')

    Acnt_Cmds = []
    Acnt_Cmds.append('ACCOUNT_LIST')
    Acnt_Cmds.append('ACCOUNT_ADD')
    Acnt_Cmds.append('ACCOUNT_DELE')
    Acnt_Cmds.append('ACCOUNT_QUERY')
    Acnt_Cmds.append('ACCOUNT_MODI')
    Acnt_Cmds.append('USERS_LIST_ROLES')
    Acnt_Cmds.append('ROLE_LIST_USERS')
    Acnt_Cmds.append('SET_USER_ROLES')

    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)

        # command = req.GET.get('command').upper()
        if command in PrivilegeApi.Org_Cmds:
            return OrgApi.OrgApi.CommandDispatch(req)
        elif command in PrivilegeApi.Role_Cmds:
            return RoleApi.RoleApi.CommandDispatch(req)
        elif command in PrivilegeApi.Acnt_Cmds:
            return AccountApi.AccountApi.CommandDispatch(req)

# ###############################################################
    @staticmethod
    def goRoleAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增角色页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/role_add.html'), dict)

    @staticmethod
    def goOrgList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开单位列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/org_list.html'), dict)

    @staticmethod
    def goOrgAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增单位页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/org_add.html'), dict)

    @staticmethod
    def goAccountList(request):
        dict = {}
        dict['adminflag'] = 0

        try:
            logincode = request.GET.get('logincode').lower()
            orgsign = request.GET.get('orgsign').lower()

            userOrg, userHandle = OrgTree.getUserOrg(logincode, orgsign)
            dict['adminflag'] = userHandle.type
        except:
            LoggerHandle.writeLogDevelope("打开登录页面", request)
            return render(request, os.path.join(STATIC_TMP,'login/login.html'), dict)

        LoggerHandle.writeLogDevelope("打开账户列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/account_list.html'), dict)

    @staticmethod
    def goAccountAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开账户新建页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/account_add.html'), dict)

    @staticmethod
    def goRoleList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开角色列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/role_list.html'), dict)

    @staticmethod
    def configUserRole(request):
        dict = {}
        LoggerHandle.writeLogDevelope("配置用户角色页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/account_config_role.html'), dict)
