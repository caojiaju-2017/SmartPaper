#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.BaseMoudle.Util import *
from SmartPaper.BaseMoudle.Privilege import *
from SmartPaper.BaseMoudle.DBModule.DBHelper import *
from SmartPaper.BaseMoudle.Privilege.PrivilegeHelper import PrivilegeHelper
from SmartPaper.BaseMoudle.DBModule.CommitData import *
from SmartPaper.Api.Privilege.OrgTree import *

class AccountApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        if command == "ACCOUNT_LIST".upper():
            return AccountApi.AccountList(req,command)
        elif command == "ACCOUNT_ADD".upper():
            return AccountApi.AccountAdd(req, command)
        elif command == "ACCOUNT_DELE".upper():
            return AccountApi.AccountDele(req, command)
        elif command == "ACCOUNT_QUERY".upper():
            return AccountApi.AccountQuery(req, command)
        elif command == "ACCOUNT_MODI".upper():
            return AccountApi.AccountModi(req, command)
        elif command == "USERS_LIST_ROLES".upper():
            return AccountApi.UserListRoles(req, command)
        elif command == "SET_USER_ROLES".upper():
            return AccountApi.SetUserRoles(req, command)

    @staticmethod
    def SetUserRoles(request,cmd):
        '''
        账户修改
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("账户修改指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # # 检查单位是否存在
        # orgHandle = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        # if not orgHandle:
        #     LoggerHandle.writeLogDevelope("单位不存在", request)
        #     loginResut = json.dumps({"ErrorInfo": "单位不存在", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查账户是否存在
        accountHandle = PaperAccount.objects.filter(code = allParams["usercode"],state=1).first()
        if not accountHandle:
            LoggerHandle.writeLogDevelope("账户数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "账户数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        roles = allParams["rolecodes"].split(",")

        # 提交变更
        commitDataList = []

        commitDataList.append(CommitData(PaperUserRole.objects.filter(acode=accountHandle), 1))
        for oneRoleCode in roles:
            if not oneRoleCode or oneRoleCode == "" or oneRoleCode == "null":
                continue
            newMap = PaperUserRole()
            newMap.rcode = PaperRoles.objects.filter(code = oneRoleCode).first()
            newMap.code = uuid.uuid1().__str__().replace("-", "")
            newMap.acode = accountHandle
            commitDataList.append(CommitData(newMap, 0))

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
    def UserListRoles(request,cmd):
        LoggerHandle.writeLogDevelope("查询账户角色%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # # 检查当前账户是否具有权限
        # resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        # if not resultPrivilegeSign:
        #     LoggerHandle.writeLogDevelope("权限受限", request)
        #     loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        # # 查询单位数据
        # orgHandle = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        # if not orgHandle:
        #     LoggerHandle.writeLogDevelope("单位数据不存在", request)
        #     loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
        #     return HttpResponse(loginResut)

        acntHandle = PaperAccount.objects.filter(code=allParams["code"]).first()
        roleUserMaps = PaperUserRole.objects.filter(acode = acntHandle )

        rtnList = []
        for oneMap in roleUserMaps:
            oneOrgDict = {}
            oneOrgDict['code'] = oneMap.code
            oneOrgDict['rcode'] = oneMap.rcode_id
            rtnList.append(oneOrgDict)

        # 返回登录结果
        lResut = json.dumps(rtnList)
        return HttpResponse(lResut)
    @staticmethod
    def AccountModi(request,cmd):
        '''
        账户修改
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("账户修改指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查单位是否存在
        orgHandle = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        if not orgHandle:
            LoggerHandle.writeLogDevelope("单位不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位不存在", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查账户是否存在
        accountHandle = PaperAccount.objects.filter(code = allParams["code"], state=1).first()
        if not accountHandle:
            LoggerHandle.writeLogDevelope("账户不存在", request)
            loginResut = json.dumps({"ErrorInfo": "账户不存在", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        accountHandle.alias = allParams["name"]
        accountHandle.phone = allParams["phone"]
        accountHandle.account = allParams["phone"]
        accountHandle.type = int(allParams["accounttype"])
        accountHandle.orgcode = orgHandle

        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(accountHandle, 0))

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
    def AccountQuery(request,cmd):
        LoggerHandle.writeLogDevelope("账户查询指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # # 查询单位数据
        # orgHandle = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        # if not orgHandle:
        #     LoggerHandle.writeLogDevelope("单位数据不存在", request)
        #     loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
        #     return HttpResponse(loginResut)

        oneAccount = PaperAccount.objects.filter(code = allParams["code"],workno=allParams["account"]).first()

        if not oneAccount:
            LoggerHandle.writeLogDevelope("账户数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "账户数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        oneOrgDict = {}
        oneOrgDict['id'] = oneAccount.id
        oneOrgDict['code'] = oneAccount.code
        oneOrgDict['account'] = oneAccount.workno
        oneOrgDict['name'] = oneAccount.alias
        oneOrgDict['phone'] = oneAccount.account
        oneOrgDict['type'] = oneAccount.type
        oneOrgDict['regdate'] = oneAccount.regdate
        oneOrgDict['orgcode'] = oneAccount.orgcode_id

        # 返回登录结果
        lResut = json.dumps(oneOrgDict)
        return HttpResponse(lResut)

    @staticmethod
    def AccountDele(request,cmd):
        LoggerHandle.writeLogDevelope("删除账户指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询单位数据
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("单位数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "单位数据不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        accountHandle = PaperAccount.objects.filter(code = allParams["code"],workno=allParams["account"]).first()

        accountHandle.state = 2
        # 提交变更
        commitDataList = []
        commitDataList.append(CommitData(accountHandle, 0))

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
    def AccountAdd(request,cmd):
        '''
        超级登录指令
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("执行添加账户指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        orgS = None
        orgList=[]
        orgsign = acntHandle.orgcode.code
        # orgsign = allParams["orgsign"]
        orgList = OrgTree.getOrgTreeObjects(PaperOrgs.objects.filter(code = orgsign).first())
        orgList.append(PaperOrgs.objects.filter(code=orgsign).first())

        accountList = []
        for oneOrg in orgList:
            acns = PaperAccount.objects.filter(orgcode = oneOrg,state = 1)
            for oneAcnt in acns:
                accountList.append(oneAcnt)

        #  检查账户是否重复
        for oneActTemp in accountList:
            if oneActTemp.workno == allParams["account"]:
                LoggerHandle.writeLogDevelope("登陆账号重复", request)
                loginResut = json.dumps({"ErrorInfo": "登陆账号重复", "ErrorId": 20007, "Result": {}})
                return HttpResponse(loginResut)

            continue

        orgsign = allParams["orgsign"]
        Name = allParams["name"]
        Account = allParams["account"] #工号
        Password = allParams["password"]
        Phone = allParams["phone"] # 手机号码
        OrgCode = allParams["orgcode"]
        accounttype = int(allParams["accounttype"])
        LoginCode = allParams["logincode"]

        orgHandle = PaperOrgs.objects.filter(code = OrgCode).first()

        newAccount = PaperAccount()
        newAccount.alias = Name
        newAccount.orgcode = orgHandle
        newAccount.code = uuid.uuid1().__str__().replace("-", "")
        newAccount.type = accounttype
        newAccount.state = 1

        # 登陆账号
        newAccount.account = Phone
        newAccount.mobile = Phone
        newAccount.workno = Account
        newAccount.password = Password
        newAccount.regdate = time.strftime("%Y-%m-%d", time.localtime())
        commitDataList = []
        commitDataList.append(CommitData(newAccount, 0))

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
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": newAccount.code})
        return HttpResponse(loginResut)

    @staticmethod
    def AccountList(request,cmd):
        '''
        超级登录指令
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("账户列表指令%s" % cmd.encode('utf-8'), request)

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

        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        orgS = None

        # orgsign = allParams["orgsign"]
        orgsign = acntHandle.orgcode.code
        orgcode = None

        try:
            orgcode = allParams["orgcode"]
        except:
            pass

        orgList = []
        if orgcode:
            orgList.append(PaperOrgs.objects.filter(code = orgcode).first())
        else:
            orgList = OrgTree.getOrgTreeObjects(PaperOrgs.objects.filter(code = orgsign).first())
            orgList.append(PaperOrgs.objects.filter(code=orgsign).first())


        accountList = []
        for oneOrg in orgList:
            acns = PaperAccount.objects.filter(orgcode = oneOrg,state = 1)
            acns = acns.filter(~Q(type = 1))
            for oneAcnt in acns:
                accountList.append(oneAcnt)


        # 排序
        accountList.sort(lambda p1,p2:cmp(p1.id,p2.id))

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])
        fliterStr = None

        try:
            fliterStr = allParams["fliterstring"]
        except:
            pass

        dataSets = []
        # 数据刷选
        for index, oneAccount in enumerate(accountList):
            if fliterStr and len(fliterStr) > 0:
                if fliterStr not in oneAccount.alias and fliterStr not in oneAccount.account and fliterStr not in oneAccount.workno:
                    continue

            dataSets.append(oneAccount)
        # 返回数据
        rtnList = []
        for index,oneAccount in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = oneAccount.id
            oneOrgDict['code'] = oneAccount.code
            oneOrgDict['account'] = oneAccount.workno
            oneOrgDict['name'] = oneAccount.alias
            oneOrgDict['phone'] = oneAccount.account
            oneOrgDict['type'] = oneAccount.type

            if oneAccount.type == 0:
                oneOrgDict['typename'] = "普通账号"
            elif oneAccount.type == 2:
                oneOrgDict['typename'] = "PAD账号"
            else:
                oneOrgDict['typename'] = "未知"
            oneOrgDict['regdate'] = oneAccount.regdate
            oneOrgDict['orgcode'] = oneAccount.orgcode_id
            oneOrgDict['orgname'] = oneAccount.orgcode.name
            rtnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(dataSets)
        dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)