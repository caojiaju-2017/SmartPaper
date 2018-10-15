#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.BaseMoudle.Util import *
from SmartPaper.BaseMoudle.Privilege import *
from SmartPaper.BaseMoudle.DBModule.DBHelper import *

from SmartPaper.Api.Privilege.OrgTree import *
from SystemData import *
import glob

class SystemApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)

        if command == "GET_DATAS".upper():
            return SystemApi.GetDatas(req,command)
        elif command == "VERSION_LIST":
            return SystemApi.VersionList(req, command)
        elif command == "VERSION_DELE":
            return SystemApi.VersionDele(req, command)
        elif command == "LOG_QUERY":
            return SystemApi.LogQuery(req, command)
        elif command == "SYSTEMCONFIG_LIST":
            return SystemApi.SystemConfigList(req, command)
        elif command == "PARAM_SETTING":
            return SystemApi.ParmSetting(req, command)
        elif command == "HOME_STAT":
            return SystemApi.HomeStat(req, command)


    @staticmethod
    def HomeStat(request,cmd):
        '''
        首页统计数据
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("首页统计数据%s" % cmd.encode('utf-8'), request)

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
        userOrg,userHandle = OrgTree.getUserOrg(allParams["logincode"],allParams["orgsign"])

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

        havePrivOrgs = OrgTree.getOrgLists(userOrg)
        dictRtn={}

        # 查询设备数据
        DevLists = None
        for index ,one in enumerate(havePrivOrgs):
            if DevLists:
                DevLists = DevLists | SmartDevices.objects.filter(orgcode=one)
            else:
                DevLists = SmartDevices.objects.filter(orgcode=one)

        DevLists = DevLists.filter(~Q(state=0))

        # 对查询得到的设备进行分组返回
        # 类型分组
        typeDict = {}
        for index, oneDev in enumerate(DevLists):
            typecode = oneDev.typecode
            devArray = {}
            if typeDict.has_key(typecode):
                devArray = typeDict[typecode]
            else:
                devArray["code"] = []
                devArray["count"] = 0
            devCodes = devArray["code"]
            devCodes.append(oneDev.code)
            devArray["code"] = devCodes
            devArray["count"] = devArray["count"] + 1

            typeDict[typecode] = devArray

        dictRtn["typestats"] = typeDict

        orgDict = {}
        for index, oneDev in enumerate(DevLists):
            orgcode = oneDev.orgcode.code
            devArray = {}
            if orgDict.has_key(orgcode):
                devArray = orgDict[orgcode]
            else:
                devArray["name"] = oneDev.orgcode.name
                devArray["count"] = 0
            devArray["name"] = oneDev.orgcode.name
            devArray["count"] = devArray["count"] + 1

            orgDict[orgcode] = devArray

        dictRtn["orgstats"] = orgDict


        faultDict = {}
        for index, oneDev in enumerate(DevLists):
            state = oneDev.state
            devArray = []
            if faultDict.has_key(state):
                devArray = faultDict[state]

            devArray.append(oneDev.code)

            faultDict[state] = devArray
        if not faultDict.has_key(1):
            faultDict[1] = []

        if not faultDict.has_key(2):
            faultDict[2] = []

        dictRtn["faultstats"] = faultDict


        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def DeviceStat(request,cmd):
        '''
        首页统计数据
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("首页统计数据%s" % cmd.encode('utf-8'), request)

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
        userOrg,userHandle = OrgTree.getUserOrg(allParams["logincode"],allParams["orgsign"])

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

        havePrivOrgs = OrgTree.getOrgLists(userOrg)
        dictRtn={}

        # 查询设备数据
        DevLists = None
        for index ,one in enumerate(havePrivOrgs):
            if DevLists:
                DevLists = DevLists | SmartDevices.objects.filter(orgcode=one)
            else:
                DevLists = SmartDevices.objects.filter(orgcode=one)

        DevLists = DevLists.filter(~Q(state=0))

        # 对查询得到的设备进行分组返回
        # 类型分组
        typeDict = {}
        for index, oneDev in enumerate(DevLists):
            typecode = oneDev.typecode
            devArray = []
            if typeDict.has_key(typecode):
                devArray = typeDict[typecode]

            devArray.append(oneDev)

            typeDict[typecode] = devArray

        dictRtn["typestats"] = typeDict

        orgDict = {}
        for index, oneDev in enumerate(DevLists):
            orgcode = oneDev.orgcode.code
            devArray = []
            if orgDict.has_key(orgcode):
                devArray = orgDict[orgcode]

            devArray.append(oneDev)

            orgDict[orgcode] = devArray

        dictRtn["orgstats"] = orgDict


        faultDict = {}
        for index, oneDev in enumerate(DevLists):
            state = oneDev.state
            devArray = []
            if faultDict.has_key(state):
                devArray = faultDict[state]

            devArray.append(oneDev)

            faultDict[state] = devArray

        dictRtn["faultstats"] = faultDict

        # # 初始设备数据返回
        # limit = int(allParams["limit"])
        # pageIndex = int(allParams["page"])
        # rtnList = []
        # for index,oneData in enumerate(DevLists):
        #     if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
        #         continue
        #     oneOrgDict = {}
        #     oneOrgDict['id'] = oneData.id
        #     oneOrgDict['code'] = oneData.code
        #     oneOrgDict['name'] = oneData.name
        #     oneOrgDict['orgname'] = oneData.orgcode.name
        #     rtnList.append(oneOrgDict)
        #
        # dictRtn = {}
        # dictRtn["code"] = 0
        # dictRtn["msg"] = "success"
        # dictRtn["count"] = len(DevLists)
        # dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def ParmSetting(request,cmd):
        '''
         设置系统参数
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("列表日志指令%s" % cmd.encode('utf-8'), request)

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

        orgsign = allParams["orgsign"]
        paramcode = allParams["paramcode"]
        KeyValue = allParams["keyvalue"]

        configHandle = SmartConfig.objects.filter(orgcode_id=orgsign,code = paramcode).first()

        if not configHandle:
            LoggerHandle.writeLogDevelope("配置项不存在", request)
            loginResut = json.dumps({"ErrorInfo": "配置项不存在", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        configHandle.keyvalue = KeyValue

        try:
            configHandle.save()
        except:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def SystemConfigList(request,cmd):
        '''
         查询单位配置
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("查询单位配置指令%s" % cmd.encode('utf-8'), request)

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

        orgsign = allParams["orgsign"]
        configList = SmartConfig.objects.filter(orgcode = orgsign)

        rtnData = []
        for index,oneSet in enumerate(configList):
            oneData = {}
            oneData["id"] = oneSet.id
            oneData["code"] = oneSet.code
            oneData["name"] = oneSet.alias
            oneData["keyname"] = oneSet.keyname
            oneData["keyvalue"] = oneSet.keyvalue
            oneData["type"] = oneSet.type
            oneData["orgsign"] = oneSet.orgcode_id
            rtnData.append(oneData)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(configList)
        dictRtn["data"] = rtnData

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def LogQuery(request,cmd):
        '''
         列表日志
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("列表日志指令%s" % cmd.encode('utf-8'), request)

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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        orgsign = acntHandle.orgcode.code
        rootOrg = PaperOrgs.objects.filter(code = orgsign).first()

        orgLists = []
        orgLists = OrgTree.getOrgTreeObjects(rootOrg)
        orgLists.append(rootOrg)

        logLists = None
        for oneOrg in orgLists:
            if not logLists:
                logLists = PaperRunlog.objects.filter(orgcode = oneOrg)
            else:
                logLists = logLists | PaperRunlog.objects.filter(orgcode = oneOrg)

        logLists = logLists.order_by("-logtime")

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])

        fliterStr = None
        ipaddress = None
        operator = None
        starttime = None
        stoptime = None
        try:
            fliterStr = allParams["fliterstring"]
            fliterStr = fliterStr.strip()
            logLists = logLists.filter(operttype__icontains=fliterStr)
        except:
            pass
        try:
            ipaddress = allParams["ipaddress"]
            logLists = logLists.filter(ip__icontains=ipaddress)
        except:
            pass
        try:
            operator = allParams["operator"]
        except:
            pass

        try:
            starttime = allParams["starttime"]
            if starttime and len(starttime) >= 19:
                logLists = logLists.filter(logtime__gte=starttime)
        except:
            pass
        try:
            stoptime = allParams["stoptime"]
            if stoptime and len(stoptime) >= 19:
                logLists = logLists.filter(logtime__lte=stoptime)
        except:
            pass

        # 根据条件筛选
        dataSets = []
        # 数据刷选
        for index, oneRecord in enumerate(logLists):
            # if fliterStr and len(fliterStr) > 0:
            #     if fliterStr not in oneRecord.operttype:
            #         continue

            # if ipaddress and len(ipaddress) > 0:
            #     if ipaddress != oneRecord.ip:
            #         continue
            if operator and len(operator) > 0:
                if operator not in  oneRecord.ucode.account:
                    continue

            # if starttime and len(starttime) > 0:
            #     if oneRecord.logtime < starttime:
            #         continue
            #
            # if stoptime and len(stoptime) > 0:
            #     if oneRecord.logtime > stoptime:
            #         continue

            dataSets.append(oneRecord)

        rtnData = []
        for index,oneSet in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneData = {}
            oneData["id"] = oneSet.id
            oneData["code"] = oneSet.code


            oneData["operator"] = oneSet.ucode
            oneData["opername"] = oneSet.content

            oneData["opertype"] = oneSet.operttype
            oneData["content"] = oneSet.content

            oneData["username"] = oneSet.terminalcode

            oneData["ipaddress"] = oneSet.ip
            oneData["opertortime"] = oneSet.logtime
            rtnData.append(oneData)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(dataSets)
        dictRtn["data"] = rtnData

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)


    @staticmethod
    def VersionDele(request,cmd):
        '''
         版本删除
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("版本删除指令%s" % cmd.encode('utf-8'), request)

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

        orgsign = allParams["orgsign"]
        rootOrg = SmartOrganization.objects.filter(code = orgsign).first()

        verCode = allParams["versioncode"]

        verHandle = SmartVersion.objects.filter(code = verCode).first()
        if not verHandle:
            LoggerHandle.writeLogDevelope("版本数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        commitDataList = []
        verHandle.state = 0
        commitDataList.append(CommitData(verHandle, 0))

        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 清楚磁盘文件
        verRoot  = SystemApi.getStoragePath()
        for infile in glob.glob(os.path.join(verRoot, verCode + '.*')):
            os.remove(infile)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def VersionList(request,cmd):
        '''
         列表版本
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("列表版本指令%s" % cmd.encode('utf-8'), request)

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
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        rootOrg = OrgTree.getRootOrgByCode(acntHandle.orgcode.code)

        orgsign = rootOrg.code
        # orgsign = allParams["orgsign"]
        rootOrg = PaperOrgs.objects.filter(code = orgsign).first()

        vers = PaperVersion.objects.filter(orgcode=rootOrg).order_by("-regtime")

        # vers = vers.filter(~Q(state = 0))

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])
        fliterStr = None
        type = int(allParams["type"])

        try:
            stype = int(allParams["stype"])
            type= stype
        except:
            pass

        try:
            fliterStr = allParams["fliterstring"]
        except:
            pass

        # 根据条件筛选
        dataSets = []
        # 数据刷选
        for index, oneRecord in enumerate(vers):
            if fliterStr and len(fliterStr) > 0:
                if fliterStr not in oneRecord.name:
                    continue
            if type != 2 and type != oneRecord.type:
                continue
            dataSets.append(oneRecord)

        rtnData = []
        for index,oneSet in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneData = {}
            oneData["id"] = oneSet.id
            oneData["name"] = oneSet.name
            oneData["type"] = oneSet.type
            oneData["version"] = oneSet.version
            oneData["regtime"] = oneSet.regtime
            oneData["code"] = oneSet.code
            rtnData.append(oneData)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(vers)
        dictRtn["data"] = rtnData

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)


    @staticmethod
    def openTest(request):
        pass

    @staticmethod
    def GetDatas(request,cmd):
        '''
         查询单位信息
         :param request:
         :param cmd:
         :return:
         '''
        LoggerHandle.writeLogDevelope("查询系统数据指令%s" % cmd.encode('utf-8'), request)

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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        # orgRoot = OrgTree.getRootOrgByCode(acntHandle.orgcode)
        orgsign = acntHandle.orgcode.code
        devObject = None
        typeCode = int(allParams["type"])
        if typeCode == 6:
            devObject = PaperDevices.objects.filter(code=orgsign,state=1).first()
            if not devObject:
                acnt = PaperAccount.objects.filter(account=allParams['logincode']).first()
                if not acnt:
                    orgsign = "1e2c68303ebd11e880d3989096c1d848"
                else:
                    orgsign = acnt.orgcode_id
            else:
                orgsign = devObject.orgcode_id
        else:
            pass

        if typeCode == 5:
            acnt = PaperAccount.objects.filter(account=allParams['logincode']).first()
            if not acnt:
                loginResut = json.dumps({"ErrorInfo": "用户数据异常", "ErrorId": 20008, "Result": {}})
                return HttpResponse(loginResut)

            orgsign = acnt.orgcode_id

        rootOrg = PaperOrgs.objects.filter(code = orgsign,state=1).first()
        orgList = OrgTree.getOrgTreeObjects(rootOrg)
        orgList.append(rootOrg)

        if typeCode != 6 and typeCode != 5:
            # 查询登录账户归属单位
            for oneOrgT in orgList:
                # 查账号
                rootOrg = PaperAccount.objects.filter(account = allParams["logincode"],orgcode= oneOrgT).first()

                # 如果查到了，则跳出
                if rootOrg and rootOrg.orgcode != None:
                    break

            # 账号的归属单位
            rootOrg = rootOrg.orgcode
            if not rootOrg:
                LoggerHandle.writeLogDevelope("账户登录信息异常", request)
                loginResut = json.dumps({"ErrorInfo": "账户登录信息异常", "ErrorId": 20002, "Result": {}})
                return HttpResponse(loginResut)


        dataSets = None
        if int(allParams["type"]) == 0:
            orgList = []
            orgList = OrgTree.getOrgTreeObjects(rootOrg)
            orgList.append(rootOrg)
            dataSets = orgList
            pass
        if int(allParams["type"]) == 1:  # 查询角色列表
            dataSets = PaperRoles.objects.filter(orgcode=rootOrg,state = 1)
            # orgList = []
            # orgList = OrgTree.getOrgTreeObjects(rootOrg)
            # orgList.append(rootOrg)

            pass
        elif int(allParams["type"]) == 2: #查询可用功能
            dataSets = PaperFunctions.objects.filter(freeflag = 1)
            pass
        # elif int(allParams["type"]) == 5:
        #     for oneOrg in orgList:
        #         if not dataSets:
        #             dataSets = SmartDeviceGroup.objects.filter(orgcode=oneOrg,state = 1)
        #         else:
        #             dataSets = dataSets | SmartDeviceGroup.objects.filter(orgcode=oneOrg,state=1)
            # dataSets = SmartDeviceGroup.objects.filter(state = 1)
        #
        # elif int(allParams["type"]) == 6:
        #     # dataSets = SmartPowers.objects.filter(orgcode=orgsign)
        #     for oneOrg in orgList:
        #         if not dataSets:
        #             dataSets = SmartPowers.objects.filter(orgcode=oneOrg,state = 1)
        #         else:
        #             dataSets = dataSets | SmartPowers.objects.filter(orgcode=oneOrg,state=1)

        rtnData = []

        if not dataSets:
            return HttpResponse(json.dumps(rtnData))


        for oneSet in dataSets:
            oneData = {}
            oneData["id"] = oneSet.code
            oneData["name"] = oneSet.name

            # 特殊项
            if int(allParams["type"]) == 6:
                oneData['portcount'] = oneSet.ctrlportnumber
                oneData['binddev'] = SystemApi.getPowerPortBindInfo(oneSet.code)
                oneData['powerFlag'] = oneSet.portstates
                oneData['preContrl'] = "http://%s:%d/" %(oneSet.ipaddress,oneSet.port)
            rtnData.append(oneData)

        return HttpResponse(json.dumps(rtnData))
        # 返回登录结果

    @staticmethod
    def getPowerPortBindInfo(pcode):
        powerObject = SmartPowers.objects.filter(code=pcode).first()

        powerMapDatas = SmartPowerPortMap.objects.filter(powercode=powerObject).order_by("port")

        mapFlag = ""
        for index in range(powerObject.ctrlportnumber):
            haveBind = False
            for oneMap in powerMapDatas:
                if oneMap.port == index + 1:
                    mapFlag = mapFlag + "1"
                    haveBind = True
                    break

            if not haveBind:
                mapFlag = mapFlag + "0"
            pass

        return  mapFlag

    @staticmethod
    def getStoragePath():
        fileType = 0
        filePath = os.path.join(STATIC_ROOT,"Service")
        filePath = os.path.join(filePath, "Version")

        # 判断目录是否存在
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        return filePath

    @staticmethod
    @csrf_exempt
    def uploadSceenFile(request):
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)
        code = None

        if not getParams.has_key("code") :
            loginResut = json.dumps({"ErrorInfo": "参数错误", "ErrorId": 2999, "Result": {}})
            return HttpResponse(loginResut)

        code = getParams["code"]
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            print '==================>' + "no file"
            return HttpResponse("no files for upload!")

        fileInfo = UtilHelper.UtilHelper.GetFileNameAndExt(myFile.name)
        shortName = fileInfo[0]
        fileExtName = ""
        if len(fileInfo) == 2:
            fileExtName = fileInfo[1]

        savePath = os.path.join(STATIC_ROOT, "Service")

        # lastSavePath = os.path.join(savePath,code + fileExtName)
        lastSavePath = os.path.join(savePath, code + ".png")

        destination = open(lastSavePath, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        dict={}
        dict["code"] = 0

        lResut = json.dumps(dict)
        return HttpResponse(lResut)

    @staticmethod
    @csrf_exempt
    def uploadFile(request):
        code = None
        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)
        # allParams = dict(getParams.items() + postParams.items())

        if not getParams.has_key("code") or \
                not postParams.has_key("versionname") or \
                not postParams.has_key("versioncode") or \
                not postParams.has_key("logincode") or \
                not postParams.has_key("versiontype"):
            loginResut = json.dumps({"ErrorInfo": "参数错误", "ErrorId": 2999, "Result": {}})
            return HttpResponse(loginResut)

        acntHandle = PaperAccount.objects.filter(account=postParams["logincode"]).first()

        # 检查版本号是否存在
        orgHandle = OrgTree.getRootOrgByCode(acntHandle.orgcode.code)

        typeTemp = int(postParams["versiontype"])

        if typeTemp == 0:
            typeTemp = 2

        existVers = PaperVersion.objects.filter(orgcode=orgHandle , version=postParams["versioncode"] ,type = typeTemp)
        if len(existVers) > 0:
            LoggerHandle.writeLogDevelope("版本号存储失败", request)
            loginResut = json.dumps({"ErrorInfo": "版本号存储失败", "ErrorId": 2999, "Result": {}})
            return HttpResponse(loginResut)

        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")

        fileInfo = UtilHelper.UtilHelper.GetFileNameAndExt(myFile.name)
        shortName = fileInfo[0]
        fileExtName = ""
        if len(fileInfo) == 2:
            fileExtName = fileInfo[1]

        savePath = SystemApi.getStoragePath()

        fileUUID = UtilHelper.UtilHelper.newUuid()

        lastSavePath = os.path.join(savePath,fileUUID + fileExtName)

        destination = open(lastSavePath, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 写入数据库
        objectHandle = PaperVersion()
        objectHandle.code = fileUUID
        objectHandle.name = postParams["versionname"]
        objectHandle.orgcode = orgHandle
        objectHandle.type = typeTemp
        objectHandle.version = postParams["versioncode"]
        objectHandle.regtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        try:
            objectHandle.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("文件记录失败", request)
            loginResut = json.dumps({"ErrorInfo": "文件记录失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        dict={}
        dict["code"] = 0

        lResut = json.dumps(dict)
        return HttpResponse(lResut)
    ########################################################################################
    @staticmethod
    def goResourceList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开终端内置资源发布列表", request)
        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/resource_list.html'), dict)

    @staticmethod
    def goLogQuery(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开日志查询页面", request)
        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/log_query.html'), dict)
    @staticmethod
    def goResourceRelease(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开内置资源发布页面", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/resource_release.html'), dict)


    @staticmethod
    def goConfigList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开单位配置页面", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/config_list.html'), dict)

    @staticmethod
    def goSettingConfig(request):
        dict = {}
        LoggerHandle.writeLogDevelope("设置单位配置项", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/config_setting.html'), dict)



    @staticmethod
    def goVersionList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打卡版本列表页面", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/version_list.html'), dict)

    @staticmethod
    def goVersionAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开版本添加页面", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/System/version_add.html'), dict)

    @staticmethod
    def goSetSceen(request):
        dict = {}
        # LoggerHandle.writeLogDevelope("打开版本添加页面", request)

        return render(request, os.path.join(STATIC_TMP, 'OrgHome/Privilege/set_sceen.html'), dict)
