#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.BaseMoudle.Util import *
from SmartPaper.BaseMoudle.Privilege import *
from SmartPaper.BaseMoudle.DBModule.DBHelper import *

from SmartPaper.Api.Privilege.OrgTree import *

class OrgApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        if command == "ORG_REGISTER".upper():
            # 记录日志
            return OrgApi.OrgRegister(req,command)
        elif command == "LIST_ORGS".upper():
            return OrgApi.ListOrgs(req, command)
        elif command == "ORG_UNREGISTER".upper():
            return OrgApi.OrgUnregister(req, command)
        elif command == "ORG_CONFIG".upper():
            return OrgApi.OrgConfig(req, command)
        elif command == "ORG_MODI".upper():
            return OrgApi.OrgModi(req, command)
        elif command == "QUERY_ORG".upper():
            return OrgApi.QueryOrg(req, command)
        elif command == "GET_ORG_TREE".upper():
            return OrgApi.GetOrgTree(req, command)
        elif command == "ORG_ADD_ORG".upper():
            return OrgApi.OrgAddOrg(req, command)
        elif command == "ORG_MODI_ORG".upper():
            return OrgApi.OrgModiOrg(req, command)


    @staticmethod
    def OrgRegister(request,cmd):
        '''
                超级登录指令
                :param request:
                :return:
                '''
        LoggerHandle.writeLogDevelope("单位注册指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 创建单位数据
        newOrg = SmartOrganization()
        newOrg.code = uuid.uuid1().__str__().replace("-", "")

        if not allParams.has_key("parentcode"):
            newOrg.parentcode = None
        else:
            # 从检查父亲单位的合法性
            parentCode = allParams["parentcode"]
            if not parentCode and len(parentCode) > 0:
                parentExist,parentHandle = PrivilegeHelper.PrivilegeHelper.checkOrgExist(allParams["parentcode"])
                if not parentExist:
                    LoggerHandle.writeLogDevelope("设定的父亲机构不存在", request)
                    loginResut = json.dumps({"ErrorInfo": "设定的父亲机构不存在", "ErrorId": 30002, "Result": {}})
                    return HttpResponse(loginResut)
                else:
                    newOrg.parentcode = parentHandle
            else:
                newOrg.parentcode = None

        newOrg.name = allParams["name"]
        newOrg.contactname = allParams["conname"]
        newOrg.contactphone = allParams["conphone"]
        newOrg.regdate = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        newOrg.signstr = newOrg.code
        newOrg.state = 1
        newOrg.type = 1
        newOrg.logo = "%s.png"%newOrg.code

        # 创建单位管理账号
        newOrgManageAccount = SmartAccount()
        newOrgManageAccount.state = 1
        newOrgManageAccount.regdate = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        newOrgManageAccount.code = uuid.uuid1().__str__().replace("-", "")
        newOrgManageAccount.orgcode = newOrg
        newOrgManageAccount.workno = allParams["account"]
        newOrgManageAccount.alias = "系统管理员"
        newOrgManageAccount.password = allParams["password"]
        newOrgManageAccount.phone = allParams["conphone"]
        newOrgManageAccount.type = 1

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(newOrg, 0))
        commitDataList.append(CommitData(newOrgManageAccount, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": newOrg.code})
        return HttpResponse(loginResut)


    @staticmethod
    def ListOrgs(request,cmd):
        '''
        超级登录指令
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位修改指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        # acntHandle = SmartAccount.objects.filter(account = allParams["logincode"]).first()
        userOrg,userHandle = OrgTree.getUserOrg(allParams["logincode"],allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账号是否具有当前权限
        if not userHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # Type
        # State
        # ParentCode
        # LoginCode
        orgS = None

        parentCode = allParams["parentcode"]
        pcode = None
        try:
            pcode = allParams["pcode"]
            parentCode = pcode
        except:
            pass

        if not parentCode or len(parentCode) == 0:
            orgS = SmartOrganization.objects.filter(state=int(allParams["state"]), parentcode = userOrg.code).order_by("id")
        else:
            orgS = SmartOrganization.objects.filter(state=int(allParams["state"]), parentcode = parentCode).order_by("id")

        orgList = []
        type = int(allParams["type"])
        if int(allParams["type"]) == 3:
            orgList = orgS
        else:
            for oneOrg in orgS:
                if oneOrg.type == type:
                    orgList.append(oneOrg)

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])
        fliter = allParams["fliter"]
        fliterStr = None

        try:
            fliterStr = allParams["fliterstring"]
        except:
            pass

        dataSets = []
        # 数据刷选
        for index, oneOrg in enumerate(orgList):
            if oneOrg.type == 3:
                continue
            if fliterStr and len(fliterStr) > 0:
                if fliterStr not in oneOrg.name:
                    continue

            if pcode and len(pcode) > 0:
                if oneOrg.parentcode_id != pcode:
                    continue

            dataSets.append(oneOrg)
        # 返回数据
        rtnList = []
        for index,oneOrg in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = oneOrg.id
            oneOrgDict['code'] = oneOrg.code
            oneOrgDict['name'] = oneOrg.name
            oneOrgDict['contactname'] = oneOrg.contactname
            oneOrgDict['contactphone'] = oneOrg.contactphone
            oneOrgDict['regdate'] = oneOrg.regdate
            oneOrgDict['logo'] = oneOrg.logo
            oneOrgDict['state'] = oneOrg.state
            oneOrgDict['type'] = oneOrg.type
            # oneOrgDict['terminalcount'] = oneOrg.terminalcount
            # oneOrgDict['storagesize'] = oneOrg.storagesize
            rtnList.append(oneOrgDict)
            pass

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(dataSets)
        dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def OrgUnregister(request,cmd):
        '''
        单位注销
        :param request:
        :param cmd:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位配置指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # 验证参数完整性
        paramCompleteness, info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询单位数据
        orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        orgHandle.state = 0

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(orgHandle, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def OrgConfig(request,cmd):
        '''
        配置单位授权信息
        :param request:
        :param cmd:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位配置指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # 验证参数完整性
        paramCompleteness, info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询单位数据
        orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        type = int(allParams["type"])


        if type == 1:
            orgHandle.terminalcount = F('terminalcount') + int(allParams["terminalcount"])
            orgHandle.storagesize = F('storagesize') + int(allParams["storagesize"])
        else:
            orgHandle.terminalcount = int(allParams["terminalcount"])
            orgHandle.storagesize = int(allParams["storagesize"])


        terminalChangeSize = int(allParams["terminalcount"])

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(orgHandle, 0))

        if type == 2:
            pass

        for index in range(terminalChangeSize):
            pass


        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def OrgModi(request,cmd):
        '''
        修改单位基础信息
        :param request:
        :param cmd:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位修改指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        # 查询单位数据
        orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)


        # orgHandle.code = uuid.uuid1().__str__().replace("-", "")
        # Name
        # Address
        # ConName
        # ConPhone


        orgHandle.name = allParams["name"]
        orgHandle.contactname = allParams["conname"]
        orgHandle.contactphone = allParams["conphone"]

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(orgHandle, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def QueryOrg(request,cmd):
        '''
         查询单位信息
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("单位查询指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # 验证参数完整性
        paramCompleteness, info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询单位数据
        orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        orgManageAccount = SmartAccount.objects.filter(orgcode = orgHandle,type = 1).first()
        # 返回单位数据
        rtnData = {}
        rtnData["code"] = orgHandle.code
        rtnData["name"] = orgHandle.name
        rtnData["contactname"] = orgHandle.contactname
        rtnData["contactphone"] = orgHandle.contactphone
        rtnData["regdate"] = orgHandle.regdate
        rtnData["state"] = orgHandle.state
        rtnData["logo"] = orgHandle.logo
        rtnData["signstr"] = orgHandle.signstr
        rtnData["parentcode"] = orgHandle.parentcode_id
        rtnData["type"] = orgHandle.type
        # rtnData["terminalcount"] = orgHandle.terminalcount
        # rtnData["storagesize"] =orgHandle.storagesize

        if not orgManageAccount:
            rtnData["maccount"] = "noset"
            rtnData["mpassword"] = "888888"
        else:
            rtnData["maccount"] = orgManageAccount.workno
            rtnData["mpassword"] = orgManageAccount.password

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": rtnData})
        return HttpResponse(loginResut)

    @staticmethod
    def GetOrgTree(request,cmd):
        '''
         查询单位树
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("单位查询查询指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # 验证参数完整性
        paramCompleteness, info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        # acntHandle = SmartAccount.objects.filter(account=allParams["logincode"]).first()
        userOrg,userHandle = OrgTree.getUserOrg(allParams["logincode"],allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账号是否具有当前权限
        if not userHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # # 查询单位数据
        # orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        # if not orgHandle:
        #     LoggerHandle.writeLogDevelope("单位数据不存在", request)
        #     loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
        #     return HttpResponse(loginResut)

        # orgManageAccount = SmartAccount.objects.filter(orgcode = userOrg,type = 1).first()

        ORG_TREE = []
        orgTree = OrgApi.getOrgTree(userOrg)

        print orgTree
        # 返回登录结果
        # loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": rtnData})
        return HttpResponse("[" + orgTree.getJson() + "]")

    ORG_TREE = {}
    @staticmethod
    def getOrgTree(org):
        if not org:
            return None

        newTree = OrgTree(org.code,org.name)

        childrens = org.children.all()
        for index in range(len(childrens)):
            child = childrens[index]

            if child and child.state == 1:
                newTree.children.append(OrgApi.getOrgTree(child))


        return newTree


    @staticmethod
    def OrgAddOrg(request,cmd):
        '''
        超级登录指令
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位添加指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 创建单位数据
        newOrg = SmartOrganization()
        newOrg.code = uuid.uuid1().__str__().replace("-", "")

        if not allParams.has_key("parentcode"):
            newOrg.parentcode = None
        else:
            # 从检查父亲单位的合法性
            parentCode = allParams["parentcode"]
            if not parentCode and len(parentCode) > 0:
                parentExist,parentHandle = PrivilegeHelper.PrivilegeHelper.checkOrgExist(allParams["parentcode"])
                if not parentExist:
                    LoggerHandle.writeLogDevelope("设定的父亲机构不存在", request)
                    loginResut = json.dumps({"ErrorInfo": "设定的父亲机构不存在", "ErrorId": 30002, "Result": {}})
                    return HttpResponse(loginResut)
                else:
                    newOrg.parentcode = parentHandle
            else:
                newOrg.parentcode = None

        newOrg.name = allParams["name"]
        newOrg.contactname = allParams["conname"]
        newOrg.contactphone = allParams["conphone"]
        newOrg.parentcode = SmartOrganization.objects.filter(code=allParams["parentcode"]).first()
        newOrg.regdate = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        newOrg.signstr = newOrg.code
        newOrg.state = 1
        newOrg.type = 1
        newOrg.logo = "%s.png"%newOrg.code


        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(newOrg, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": newOrg.code})
        return HttpResponse(loginResut)

    @staticmethod
    def OrgModiOrg(request,cmd):
        '''
        修改单位基础信息
        :param request:
        :param cmd:
        :return:
        '''
        LoggerHandle.writeLogDevelope("单位修改指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(workno = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        # 查询单位数据
        orgHandle = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)


        orgHandle.name = allParams["name"]
        orgHandle.contactname = allParams["conname"]
        orgHandle.contactphone = allParams["conphone"]
        # orgHandle.parentcode = SmartOrganization.objects.filter(code=allParams["parentcode"])

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(orgHandle, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)