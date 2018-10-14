#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from SmartPaper.Api.Privilege.OrgTree import *
# from include import *

class PrivilegeHelper(object):
    @staticmethod
    def funcPrivCheck(cmd, acntHandle):
        '''
        检查功能权限
        :param cmd:
        :param acntHandle:
        :return:
        '''
        from SmartPaper.models import *
        # 判断账号是否为超级管理员
        if not acntHandle:
            return  False

        # 如果是单位超级管理员，或平台超级管理员，则检查通过
        if acntHandle.type == 1 or acntHandle.type == 2:
            return True

        return True
        # 获取账号拥有的角色
        acntRoles = ByAdUserRole.objects.filter(acode = acntHandle.code)

        # 获取命令码定义数据
        cmdHandle = ByAdFunctions.objects.filter(cmd = cmd).first()

        for oneRole in acntRoles:
            # 查询角色信息---暂不进行归属单位查询
            roleHandle = ByAdRoles.objects.filter(code = oneRole.rcode_id).first()

            if not roleHandle:
                continue

            # 获取角色功能清单
            roleFuncs = ByAdRoleFunc.objects.filter(rcode = roleHandle.code)

            #  检查清单是否包含当前指令
            for oneRoleFunc in roleFuncs:
                if oneRoleFunc.fcode == cmdHandle.code:
                    return True

        return False
        pass


    @staticmethod
    def dataRangeCheck(orgdata,acntHandle):
        '''
        数据范围检查
        :param orgdata:
        :param acntHandle:
        :return:
        '''
        pass

    @staticmethod
    def checkOrgExist(orgcode):
        '''
        检查单位是否存在
        :param orgcode:
        :return:
        '''
        from SmartPaper.models import *
        orgHandle = SmartOrganization.objects.filter(code = orgcode).first()
        if not orgHandle:
            return False,orgHandle

        return True,orgHandle

    @staticmethod
    def getRootOrg(orgcode):
        '''
        检查单位是否存在
        :param orgcode:
        :return:
        '''
        from SmartPaper.models import *
        orgHandle = SmartOrganization.objects.filter(code = orgcode).first()
        if not orgHandle:
            return False


        while True:
            if orgHandle.parentcode_id == orgHandle.code:
                return orgHandle

            parentHandle = SmartOrganization.objects.filter(code = orgHandle.parentcode_id).first()

            # 如果父亲单位数据异常或不存在
            if not parentHandle:
                return None

        return None

    @staticmethod
    def getUserPriv(userHandle):
        # 账户是否是单位超级管理员，则返回全部权限
        if not userHandle: # 返回空权限
            return {'00000':"0"}

        if userHandle.type == 1:  #返回全部权限
            return {'00000':"1"}

        from SmartPaper.models import *
        rtnDict = {}
        # 查询账户角色清单
        roles = PaperUserRole.objects.filter(acode=userHandle)

        for oneRole in roles:
            # 查询角色功能清单
            funcs = PaperRoleFunc.objects.filter(rcode=oneRole.rcode)

            # 提取功能ID
            for oneFunc in funcs:
                funcId = oneFunc.fcode.funcid.__str__()

                currentFuncValue = None
                # 检查当前字典是否有数据
                if rtnDict.has_key(funcId):
                    currentFuncValue = rtnDict[funcId]
                else:
                    currentFuncValue = "000000000000"
                roleConfig = oneFunc.flag

                # 更新
                rtnDict[funcId] = PrivilegeHelper.plusFlag(currentFuncValue,roleConfig)
            pass
        return  rtnDict

    @staticmethod
    def plusFlag(currentFlag,roleFlag):
        if len(currentFlag) != len(roleFlag):
            return "000000000000"

        rtnFlag = ""
        for index in range(len(currentFlag)):
            cFlagBit = currentFlag[index:index + 1]
            rFlagBit = roleFlag[index:index + 1]

            try:
                resultBit = int(cFlagBit) + int(rFlagBit)
                if resultBit > 0:
                    rtnFlag = rtnFlag + "1"
                else:
                    rtnFlag = rtnFlag + "0"
            except:
                pass

        return  rtnFlag