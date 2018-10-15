#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.BaseMoudle.Util import *
from SmartPaper.BaseMoudle.Privilege import *
from SmartPaper.Api.Privilege.OrgTree import *
from SmartPaper.BaseMoudle.DBModule.DBHelper import *
from SmartPaper.BaseMoudle.DBModule.CommitData import *
from SmartPaper.BaseMoudle.Privilege.PrivilegeHelper import PrivilegeHelper


class LoginApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)
        if command == "NORMAL_LOGIN".upper():
            return LoginApi.loginSystem(req,command)
        elif command == "TERMINAL_LOGIN".upper():
            return LoginApi.terminalRegister(req, command)
        elif command == "HEART_BEAT".upper():
            return LoginApi.heartBeat(req, command)
        elif command == "PSWD_RESET".upper():
            return LoginApi.PswdReset(req, command)
        elif command == "SET_USER_PSWD".upper():
            return LoginApi.SetUserPswd(req, command)

    @staticmethod
    def SetUserPswd(request,cmd):
        '''
         复制节目
         :param request:
         :return:
         '''
        LoggerHandle.writeLogDevelope("密码重置%s" % cmd.encode('utf-8'), request)

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

        # orgHandel = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        # if not orgHandel:
        #     LoggerHandle.writeLogDevelope("客户单位数据异常", request)
        #     loginResut = json.dumps({"ErrorInfo": "客户单位数据异常", "ErrorId": 20008, "Result": {}})
        #     return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        if not userHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询账号信息
        accountModi = PaperAccount.objects.filter(code = allParams["acode"]).first()
        if not accountModi:
            LoggerHandle.writeLogDevelope("待修改的账号不存在", request)
            loginResut = json.dumps({"ErrorInfo": "待修改的账号不存在", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)

        accountModi.password = allParams["password"]
        commitDataList = []
        commitDataList.append(CommitData(accountModi, 0))

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
    def PswdReset(request,cmd):
        '''
         复制节目
         :param request:
         :return:
         '''
        LoggerHandle.writeLogDevelope("密码修改%s" % cmd.encode('utf-8'), request)

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
        # acntHandle = SmartAccount.objects.filter(account=allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        # if not acntHandle:
        #     LoggerHandle.writeLogDevelope("当前账号数据异常", request)
        #     loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
        #     return HttpResponse(loginResut)

        # # 检查当前账户是否具有权限 -- 自我修改密码，无需权限验证
        # resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        # if not resultPrivilegeSign:
        #     LoggerHandle.writeLogDevelope("权限受限", request)
        #     loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        # orgHandel = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
        # if not orgHandel:
        #     LoggerHandle.writeLogDevelope("客户单位数据异常", request)
        #     loginResut = json.dumps({"ErrorInfo": "客户单位数据异常", "ErrorId": 20008, "Result": {}})
        #     return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        if not userHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)


        # 验证原密码是否正确
        if userHandle.password != allParams["oldpassword"]:
            LoggerHandle.writeLogDevelope("原密码错误", request)
            loginResut = json.dumps({"ErrorInfo": "原密码错误", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userHandle.password = allParams["newpassword"]
        commitDataList = []
        commitDataList.append(CommitData(userHandle, 0))

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
    def loginSystem(request,cmd):
        '''
        管理后台登录指令
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到登录指令%s"%cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items()+postParams.items())
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

        # # 查询管理顶级组织机构
        # manageHandler = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        #
        # if not manageHandler:
        #     LoggerHandle.writeLogDevelope("组织机构数据错误", request)
        #     loginResut = json.dumps({"ErrorInfo": "组织机构数据错误", "ErrorId": 20003, "Result": {}})
        #     return HttpResponse(loginResut)
        #
        #
        # # 获取机构列表
        # havePrivOrgs = OrgTree.getOrgLists(manageHandler)
        #
        # # 查询整个机构账户列表
        # accounts = None
        # for oneAcnt in havePrivOrgs:
        #     if not accounts:
        #         # aaaa = SmartAccount.objects.all()
        #         accounts = PaperAccount.objects.filter(orgcode=oneAcnt,state=1)
        #     else:
        #         accounts = accounts | PaperAccount.objects.filter(state= 1,orgcode=oneAcnt)

        # 查询账户信息
        accountHandle = PaperAccount.objects.filter(account=allParams["account"],state=1).first()

        # 如果账户不存在，则验证工号
        if not accountHandle :
            accountHandle = PaperAccount.objects.filter(workno=allParams["account"], state=1).first()

        if not accountHandle:
            LoggerHandle.writeLogDevelope("账号数据不存在", request)
            loginResut = json.dumps({"ErrorInfo": "账号数据不存在", "ErrorId": 20004, "Result": {}})
            return HttpResponse(loginResut)

        # 验证账户信息
        if (accountHandle.workno == allParams["account"] and accountHandle.password == allParams["password"]) or \
                (accountHandle.account == allParams["account"] and accountHandle.password == allParams["password"]):
            # 返回登录结果
            loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": accountHandle.alias})
            return HttpResponse(loginResut)

        LoggerHandle.writeLogDevelope("账号或密码错误", request)
        loginResut = json.dumps({"ErrorInfo": "账号或密码错误", "ErrorId": 30001, "Result": {}})
        return HttpResponse(loginResut)

    @staticmethod
    def terminalRegister(request,cmd):
        '''
        超级登录指令
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("收到登录指令%s"%cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items()+postParams.items())
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

        # 判断终端 RegCode ---  注册License
        isRegister = True
        terminalCode = allParams["terminal"]
        terminalHandle = SmartDevices.objects.filter(terminalcode=terminalCode ).first()

        # 如果终端号未层注册，则进一步检查是否mac地址注册过
        if not terminalHandle:
            macCode = allParams["mac"]
            terminalHandle = SmartDevices.objects.filter(mac=macCode).first()

        # rtnDict = {}
        licenseHandle = None
        if not terminalHandle:
            isRegister = False
        else:
            # # 检查终端是否授权
            # licenseDatas = ByAdLicense.objects.filter(terminalcode = terminalCode)
            # orgcodeTerminal = allParams["orgsign"]
            # orgData = SmartOrganization.objects.filter(code=orgcodeTerminal).first()
            # result,licenseHandle = LicenseHelper.LicenseHelper.checkLicense(licenseDatas,orgData)

            # 如果当前终端被删除，则重新激活
            if terminalHandle.state != 1:
                terminalHandle.orgcode = SmartOrganization.objects.filter(code=allParams["orgsign"]).first()
                terminalHandle.name = None
                terminalHandle.gcode = None  # 新终端未分组
                terminalHandle.ipaddress = allParams["myip"]
                terminalHandle.mac = allParams["mac"]
                terminalHandle.lastcmd = None
                terminalHandle.lastcmdresult = None
                terminalHandle.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                terminalHandle.online = 1
                terminalHandle.pcode = None
                terminalHandle.type = allParams["type"]
                terminalHandle.version = allParams["version"]
                terminalHandle.port = int(allParams["port"])
                terminalHandle.ledtype = -1
                terminalHandle.state = 1
                terminalHandle.terminalsign = allParams["terminal"]
                terminalHandle.width = int(allParams["width"])
                terminalHandle.heigth = int(allParams["heigth"])

                try:
                    terminalHandle.save()
                except Exception,ex:
                    LoggerHandle.writeLogDevelope("播放器注册失败-状态更新失败", request)
                    loginResut = json.dumps({"ErrorInfo": "播放器注册失败-状态更新失败", "ErrorId": 20001, "Result": {}})
                    return HttpResponse(loginResut)
            #
            # if not result:
            #     LoggerHandle.writeLogDevelope("终端license验证失败，请联系管理员", request)
            #     loginResut = json.dumps({"ErrorInfo": "终端license验证失败，请联系管理员", "ErrorId": 20002, "Result": {}})
            #     return HttpResponse(loginResut)
            else: #验证成功
                rtnDict = {}
                rtnDict["orgsign"] = terminalHandle.orgcode_id
                rtnDict["name"] = terminalHandle.name
                rtnDict["terminal"] = terminalHandle.code

                if licenseHandle:
                    rtnDict["regcode"] = licenseHandle.licensecode

                # rtnDict["updateurl"] = VersionHelper.VersionHelper.checkUpdate(allParams["version"],allParams["type"],allParams['orgsign'])
                rtnDict["updateurl"] = ""
                loginResut = json.dumps({"ErrorInfo": "验证成功", "ErrorId": 200, "Result": rtnDict})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        if not isRegister:
            regPlayer = SmartDevices()
            regPlayer.code = allParams["terminal"]
            regPlayer.orgcode = SmartOrganization.objects.filter(code = allParams["orgsign"]).first()
            regPlayer.name = None
            regPlayer.gcode = None # 新终端未分组
            regPlayer.ipaddress = allParams["myip"]
            regPlayer.mac = allParams["mac"]
            regPlayer.lastcmd = None
            regPlayer.lastcmdresult = None
            regPlayer.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            regPlayer.online = 1
            regPlayer.pcode = None
            regPlayer.typecode = allParams["type"]
            regPlayer.version = allParams["version"]
            regPlayer.port = int(allParams["port"])
            regPlayer.ledtype = -1
            regPlayer.state = 1
            regPlayer.terminalsign = allParams["terminal"]
            regPlayer.width = int(allParams["width"])
            regPlayer.heigth = int(allParams["heigth"])

            try:
                regPlayer.save()
            except Exception,ex:
                LoggerHandle.writeLogDevelope("播放器注册失败", request)
                loginResut = json.dumps({"ErrorInfo": "播放器注册失败", "ErrorId": 20001, "Result": {}})
                return HttpResponse(loginResut)
        else:
            pass

        rtnDict = {}
        rtnDict["orgsign"] = regPlayer.orgcode_id
        rtnDict["name"] = regPlayer.name
        rtnDict["terminal"] = regPlayer.code
        if licenseHandle:
            rtnDict["regcode"] = licenseHandle.licensecode

        # rtnDict["updateurl"] = VersionHelper.VersionHelper.checkUpdate(allParams["version"],allParams["type"],allParams['orgsign'])

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "您的终端登记成功，请联系管理员授权", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def heartBeat(request,cmd):
        '''
        设备心跳包
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到心跳包指令%s"%cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items()+postParams.items())
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


        #
        # playstate = SmartDevicestat.objects.filter(terminalcode=allParams["terminal"]).first()

        # 如果首次推动，则新增记录
        # if not playstate:
        playstate = SmartDevicestat()

        playstate.code = UtilHelper.UtilHelper.newUuid()
        # 设置终端数据
        playstate.terminalcode = SmartDevices.objects.filter(code = allParams["terminal"]).first()
        playstate.cpu = int(allParams["cpu"])
        playstate.orgcode = SmartOrganization.objects.filter(code = allParams["orgsign"]).first()
        playstate.disk = int(allParams["disk"])
        playstate.memory = int(allParams["memory"])
        playstate.recordtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            playstate.save()
        except Exception,ex:
            pass

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    # +++++++++++++++++++++++++++++++++url路由++++++++++++++++++++++++++++++++++++
    @staticmethod
    def openLoginHome(request):
        dict={}
        # LoggerHandle.writeLog("fasfdsfds",request)
        LoggerHandle.writeLogDevelope("打开登录页面", request)
        return render(request, os.path.join(STATIC_TMP,'login/login.html'), dict)

    @staticmethod
    def goChangePassword(request):
        LoggerHandle.writeLogDevelope("打开修改密码", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/change_password.html'), {})


    # ################################################################
    @staticmethod
    def openAddCustomHome(request):
        dict={}
        LoggerHandle.writeLogDevelope("打开单位管理主页", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Privilege/org_add.html'), dict)

    @staticmethod
    def goOrgHome(request):
        dict = {}
        try:
            logincode = request.GET.get('logincode').lower()
            dict["logincode"] = logincode

            acntHandle = PaperAccount.objects.filter(account=logincode, state=1).first()

            if not acntHandle:
                acntHandle = PaperAccount.objects.filter(workno=logincode, state=1).first()

            if acntHandle:
                dict["useralias"] = acntHandle.alias
        except:
            LoggerHandle.writeLogDevelope("打开登录页面", request)
            return render(request, os.path.join(STATIC_TMP,'login/login.html'), dict)

        dict["lisence"] = "© 博源科技-版权所有"

        dict["privs"] = PrivilegeHelper.getUserPriv(acntHandle)
        # dict["privs"] = []
        LoggerHandle.writeLogDevelope("打开管理员主页", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/index.html'), dict)
