#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ParamCheckHelper(object):
    def __init__(self):
        self.ParamList = []

    @staticmethod
    def getParamModule(cmd):
        rtnParamHandle = ParamCheckHelper()
        if cmd.upper() == "NORMAL_LOGIN":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account",True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
        elif cmd.upper() == "TERMINAL_LOGIN":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Version", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Device", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("MYIP", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("MAC", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TYPE", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Sign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RegCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Width", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Heigth", True))
        elif cmd.upper() == "AD_AUDIT_LOGIN":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ADMIN_LOGIN":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "HEART_BEAT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Device", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RegCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Cpu", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Disk", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Memory", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "PSWD_RESET":
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OldPassword", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("NewPassword", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SET_USER_PSWD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ACode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        # #########################################单位管理#####################################################
        elif cmd.upper() == "ORG_REGISTER":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Address", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConName", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConPhone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ParentCode", False))
        elif cmd.upper() == "ORG_MODI":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Address", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConName", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConPhone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "LIST_ORGS":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Fliter", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ParentCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ORG_UNREGISTER":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ORG_CONFIG":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TerminalCount", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("StorageSize", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "QUERY_ORG":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "GET_ORG_TREE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ORG_ADD_ORG":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConName", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConPhone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ParentCode", False))
        elif cmd.upper() == "ORG_MODI_ORG":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConName", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ConPhone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ParentCode", False))
        # #################################终端指令####################################################
        elif cmd.upper() == "DOWNLOAD_AD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ADCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TerminalCode", True))
        elif cmd.upper() == "QUERY_ADS":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PageSize", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("CurrentIndex", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Device", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RegCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "DOWNLOAD_NOTIFY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("AdCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Rate", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Device", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RegCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "PLAYER_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "LED_REGISTER":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IPAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Mac", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LedType", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Width", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Height", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "PLAYER_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "TERMINAL_AUTH":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TerminalCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "TERMINAL_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "LED_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IPAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Mac", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LedType", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LedCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "TERMINAL_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IPAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Mac", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        # ###################################角色相关#######################################################
        elif cmd.upper() == "ROLE_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Funcs", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Info", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ROLE_MODI":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Info", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Funcs", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ROLE_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ROLE_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ROLE_SET":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Users", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Types", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ROLE_LIST_USERS":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PageSize", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("CurrentIndex", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "AD_AUDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ADCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Info", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Result", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ACCOUNT_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "ACCOUNT_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Password", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Phone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("AccountType", True))
        elif cmd.upper() == "ACCOUNT_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))

        elif cmd.upper() == "ACCOUNT_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
        elif cmd.upper() == "ACCOUNT_MODI":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Phone", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Account", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("AccountType", True))
        elif cmd.upper() == "SET_USER_ROLES":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("UserCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("RoleCodes", True))
        elif cmd.upper() == "USERS_LIST_ROLES":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))

        #############################系统相关################################
        elif cmd.upper() == "GET_DATAS":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "VERSION_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "VERSION_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("VersionCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "HOME_STAT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "LOG_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SYSTEMCONFIG_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "PARAM_SETTING":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ParamCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("KeyValue", True))
        #############################媒体相关################################
        elif cmd.upper() == "REQ_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "RES_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ResCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "SPECIAL_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "SPECIAL_REQ_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SpecialCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "SPECIAL_RES_SET":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SpecialCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ResCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Way", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SPECIAL_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SpecialCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        #############################日程相关################################
        elif cmd.upper() == "SCHEDULE_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SCHEDULE_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheduleInfo", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SCHEDULE_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SCHEDULE_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "SCHEDULE_SETTING":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheduleInfo", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        # ###########################################模板管理#########################################################
        elif cmd.upper() == "TMP_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "TMP_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Width", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Height", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Zones", True))

        elif cmd.upper() == "TMP_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TmpCode", True))
        elif cmd.upper() == "TMP_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TmpCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Width", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Height", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Zones", True))
        elif cmd.upper() == "TMP_COPY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TmpCode", True))
        elif cmd.upper() == "TMP_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TmpCode", True))
        # ####################################PROGRAMS_LIST##############################################
        elif cmd.upper() == "PROGRAMS_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "PROGRAM_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TemplateCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Sound", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("BackImage", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Zones", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Configs", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("medias", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Priority", True))
        elif cmd.upper() == "PROGRAM_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ProgramCode", True))
        elif cmd.upper() == "PROGRAM_COPY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ProgramCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Priority", True))
        elif cmd.upper() == "PROGRAM_MODI":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TemplateCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Sound", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("BackImage", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Zones", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Configs", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("medias", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Priority", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ProCode", True))
        elif cmd.upper() == "PROGRAM_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ProgramCode", True))

        #     ################################频道##############################################
        elif cmd.upper() == "CHANNEL_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "CHANNEL_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ProgramCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ScheCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Ranges", True))
        elif cmd.upper() == "CHANNEL_SETTING":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ChannelCode", True))
        elif cmd.upper() == "CHANNEL_AUDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ChannelCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Context", True))
        elif cmd.upper() == "CHANNEL_DOWNLOAD_STATE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("ChannelCode", True))


        # ===========================分组管理==========================================
        elif cmd.upper() == "GROUP_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", False))
        elif cmd.upper() == "GROUP_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", False))
        elif cmd.upper() == "GROUP_DELE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
        elif cmd.upper() == "GROUPS_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", False))
        elif cmd.upper() == "GROUP_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))

        elif cmd.upper() == "GROUP_CONFIG":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))

        elif cmd.upper() == "DEVS_MYGROUP":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            # rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TypeCode", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("GroupCode", True))

        elif cmd.upper() == "GROUP_CLOSE_LIGHT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))

        elif cmd.upper() == "GROUP_OPEN_LIGHT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
        #===============================================
        elif cmd.upper() == "POWER_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TPorts", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IpAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))

        elif cmd.upper() == "POWER_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PowerCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TPorts", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IpAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))

        elif cmd.upper() == "POWER_SET":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))

        elif cmd.upper() == "POWERS_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))


        elif cmd.upper() == "POWER_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PowerCode", True))

        elif cmd.upper() == "POWER_CONTROL":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PowerCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
        elif cmd.upper() == "SET_DEV_POWER":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("PowerCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
        elif cmd.upper() == "SET_DEV_POSITION":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LeftX", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LeftY", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Width", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Height", True))

        elif cmd.upper() == "DEVICE_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevCode", True))

        elif cmd.upper() == "DEVICES_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("GrpCode", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TypeCode", False))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Filters", False))
        elif cmd.upper() == "DEVICES_STAT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

        elif cmd.upper() == "SET_DEVICE":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
        elif cmd.upper() == "DEVICE_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IPAddress", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Mac", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Port", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevType", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))

        elif cmd.upper() == "LIGHT_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LightCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IsSmart", True))
        elif cmd.upper() == "LIGHT_REGISTER":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Type", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("IsSmart", True))
        # ###################策略管理
        elif cmd.upper() == "STRATEGYS_ADD":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("StartDate", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("StopDate", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OpenTime", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("CloseTime", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
        elif cmd.upper() == "STRATEGYS_EDIT":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Name", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("StartDate", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("StopDate", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OpenTime", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("CloseTime", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgCode", True))
        elif cmd.upper() == "STRATEGYS_LIST":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
        elif cmd.upper() == "STRATEGYS_INFO":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
        elif cmd.upper() == "STRATEGYS_BIND":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("DevCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))

        elif cmd.upper() == "STRATEGYS_SET":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))

            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("State", True))
        elif cmd.upper() == "STRATEGYS_DEV_QUERY":
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("OrgSign", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("LoginCode", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("TimeStamp", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("SIGN", True))
            rtnParamHandle.ParamList.append(ParamCheckHelper.OneParam.createParam("Code", True))

        return rtnParamHandle

    def checkParamComplete(self,params):
        for oneParam in self.ParamList:
            if not params.has_key(oneParam.paramName) and oneParam.isNecessary:
                return False,oneParam.paramName

        return True,None

    def haveParam(self,name):
        for oneParam in self.ParamList:
            if name.lower() == oneParam.paramName.lower():
                return True

        return False

    class OneParam(object):
        def __init__(self):
            self.paramName = None
            self.isNecessary = False

        @staticmethod
        def createParam(paramname, nessary):
            param = ParamCheckHelper.OneParam()
            param.paramName = paramname.lower()
            param.isNecessary = nessary

            return  param