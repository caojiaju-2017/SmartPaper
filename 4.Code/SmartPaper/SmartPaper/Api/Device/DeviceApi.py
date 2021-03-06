#!/usr/bin/env python
# -*- coding: utf-8 -*-
from include import *

from include import *

from SmartPaper.BaseMoudle.DBModule.DBHelper import *
from SmartPaper.BaseMoudle.Util import *
from SmartPaper.BaseMoudle.Privilege import *
from SmartPaper.Api.Privilege.OrgTree import *

from SmartPaper.BaseMoudle.Device.DeviceHelper import DeviceHelper
from SmartPaper.BaseMoudle.Device.PowerHelper import PowerHelper
from SmartPaper.BaseMoudle.Privilege.PrivilegeHelper import PrivilegeHelper
from SmartPaper.BaseMoudle.DBModule.CommitData import *

class DeviceApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)

        if command == "LED_REGISTER".upper():
            return DeviceApi.LedRegister(req,command)
        elif command == "LED_EDIT".upper():
            return DeviceApi.LedEdit(req,command)
        elif command == "LIGHT_REGISTER".upper():
            return DeviceApi.LightRegister(req, command)
        elif command == "LIGHT_EDIT".upper():
            return DeviceApi.LightEdit(req, command)
        elif command == "DEVICE_ADD":
            return DeviceApi.DeviceAdd(req, command)
        elif command == "DEVICE_EDIT":
            return DeviceApi.DeviceEdit(req, command)
        elif command == "SET_DEVICE":
            return DeviceApi.SetDevice(req, command)
        elif command == "DEVICES_LIST".upper():
            return DeviceApi.DeviceList(req, command)
        elif command == "DEVICE_INFO".upper():
            return DeviceApi.DeviceInfo(req, command)
        elif command == "DEVICE_CONTROL".upper():
            return DeviceApi.DeviceControl(req, command)
        elif command == "SET_DEV_POSITION".upper():
            return DeviceApi.SetDevPosition(req, command)
        elif command == "SET_DEV_POWER".upper():
            return DeviceApi.SetDevPower(req, command)

        elif command == "POWER_ADD".upper():
            return DeviceApi.PowerAdd(req, command)
        elif command == "POWER_EDIT".upper():
            return DeviceApi.PowerEdit(req, command)
        elif command == "POWER_SET".upper():
            return DeviceApi.PowerSet(req, command)
        elif command == "POWERS_LIST".upper():
            return DeviceApi.PowerList(req, command)
        elif command == "POWER_INFO".upper():
            return DeviceApi.PowerInfo(req, command)
        elif command == "DEVICES_STAT".upper():
            return DeviceApi.DeviceStat(req, command)
        elif command == "POWER_QUERY_DEVS".upper():
            return DeviceApi.QueryDevices(req, command)
        elif command == "POWER_CONTROL".upper():
            return DeviceApi.PowerControl(req, command)

        # 本次新增
        elif command == "TERMINAL_STATUS".upper():
            return DeviceApi.TerminalStatus(req, command)
        elif command == "TERMINAL_ QRCODE".upper():
            return DeviceApi.TerminalQRCode(req, command)
        elif command == "HEAT_BEAT".upper():
            return DeviceApi.HeartBeat(req, command)

    @staticmethod
    def TerminalStatus(request,cmd):
        '''
        LED查询
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到设备查询指令%s"%cmd.encode('utf-8'), request)
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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle or not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        # ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        status = int(allParams["status"])
        mac = allParams["mac"]
        eventid = allParams["eventid"]


        # 检查logioncode是否为权力机构
        devHandles = PaperDevices.objects.filter(mac=mac)
        devHandle = devHandles.filter(~Q(state = 0)).first()

        # 检查当前账号是否具有当前权限
        if not devHandle:
            LoggerHandle.writeLogDevelope("当前设备数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前设备数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 设备状态
        devHandles.state = status
        eventHandle = None
        # 如果状态不正常，则需要更新
        if status in [21,22,23,24,8,20]:
            eventHandle = PaperDevicesEvent.objects.filter(mac = mac,eventid = eventid).first()
            if not eventHandle:
                eventHandle = PaperDevicesEvent()
                eventHandle.mac = mac
                eventHandle.count = 0
                eventHandle.eventid = eventid
                eventHandle.eventtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())



        commitDataList = []
        commitDataList.append(CommitData(devHandles, 0))
        if eventHandle:
            commitDataList.append(CommitData(eventHandle, 0))

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
    def TerminalQRCode(request,cmd):
        '''
        LED查询
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到设备查询指令%s"%cmd.encode('utf-8'), request)
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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle or not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        # ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        mac = allParams["mac"]

        # 查询设备信息
        devHandle = PaperDevices.objects.filter(mac = mac).first()
        if not devHandle or devHandle.state in [21,22,23,24,8,20]:
            LoggerHandle.writeLogDevelope("设备异常或故障", request)
            loginResut = json.dumps({"ErrorInfo": "设备异常或故障", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        type = int(allParams["type"])

        ermaUrl = "http://" + request.META['HTTP_HOST']
        if type == 0: # 免费取纸
            url = "http://" + request.META['HTTP_HOST'] + "/wait.html?code=" + devHandle.code + "&type=0"
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "images" + os.sep + "qrcode"), "%s_0.jpg" % devHandle.code))
            ermaUrl = ermaUrl + "/static/images/qrcode/%s_0.jpg" % devHandle.code
        elif type == 1:
            url = "http://" + request.META['HTTP_HOST'] + "/wait.html?code=" + devHandle.code + "&type=1"
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "images" + os.sep + "qrcode"), "%s_1.jpg"%devHandle.code))
            ermaUrl = ermaUrl + "/static/images/qrcode/%s_1.jpg" % devHandle.code

        # 返回登录结果
        lResut = json.dumps(ermaUrl)
        return HttpResponse(lResut)

    @staticmethod
    def HeartBeat(request,cmd):
        '''
        LED查询
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到设备查询指令%s"%cmd.encode('utf-8'), request)
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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle or not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        # ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        mac = allParams["mac"]
        devHandle = PaperDevices.objects.filter(mac = mac).first()
        if not devHandle:
            LoggerHandle.writeLogDevelope("设备数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "设备数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        haveApply = PaperApplyFreePaper.objects.filter(devcode = devHandle,state = 0).first()
        outpaper = 0
        if haveApply:
            outpaper = 1

        # 查询付款成功项
        orderHandle = PaperOrders.objects.filter(dcode=devHandle,state=1).first()
        deliver = -1
        if orderHandle:
            updateMapData = PaperDevGoodsMap.objects.filter(dcode=devHandle,gcode=orderHandle).first()
            if not updateMapData:
                deliver = -1
            else:
                deliver = updateMapData.trackindex

        # 先更新状态
        commitDataList = []
        if haveApply:
            haveApply.state = 1
            commitDataList.append(CommitData(haveApply, 0))

        if orderHandle:
            haveApply.state = 2
            commitDataList.append(CommitData(orderHandle, 0))

        if updateMapData:
            # 增量修改值---数据库保证锁定数据----这是一段错误的代码
            # count 减  lockcount 加
            updateMapData.count = updateMapData.count - 1
            updateMapData.lockcount = updateMapData.lockcount + 1
            # 成功吐出物件后， 更新PaperDevGoodsMap 对应的lockcount 和 count
            commitDataList.append(CommitData(updateMapData, 0))

        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)
            if not result:
                loginResut = json.dumps({"ErrorInfo": "刷新数据失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            LoggerHandle.writeLogDevelope("内部错误或网络错误", request)
            loginResut = json.dumps({"ErrorInfo": "内部错误或网络错误", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)


        # Result = {“deliver”:trackid;“outpaper”:0 / 1; “reboot”:0;}
        rtnDict = {}
        rtnDict["deliver"] = deliver
        rtnDict["ordercode"] = orderHandle.code
        rtnDict["outpaper"] = outpaper
        rtnDict["reboot"] = 0

        # 返回登录结果
        lResut = json.dumps(rtnDict)
        return HttpResponse(lResut)

    @staticmethod
    def syncControl(dev,power,port,state):
        '''
        异步开关机
        :param dev:
        :param power:
        :param port:
        :param state:
        :return:
        '''
        # 关机
        if state == 1:
            pass
        elif state == 0:
            DeviceHelper.DeviceShutdown(dev)
            time.sleep(30)

        # 断电
        if state == 1:
            PowerHelper.openPort(power, port)
        elif state == 0:
            PowerHelper.closePort(power, port)

    @staticmethod
    def QueryDevices(request,cmd):
        '''

        :param request:
        :return:
        '''

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)

        allParams = getParams

        if not allParams.has_key("code"):
            loginResut = json.dumps({"ErrorInfo": "参数不足", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        code = allParams["code"]

        powerHandle = SmartPowers.objects.filter(code = code,state=1).first()

        if not powerHandle:
            loginResut = json.dumps({"ErrorInfo": "电源数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        rtnData = []
        dataSets = SmartPowerPortMap.objects.filter(powercode=powerHandle)

        for oneData in dataSets:
            oneDev = {}
            oneDev["code"] = oneData.devcode.code
            oneDev["name"] = oneData.devcode.name

            powerFlag = oneData.powercode.portstates
            bindPort = oneData.port

            oneDev["powerstate"] = powerFlag[bindPort - 1:bindPort]
            rtnData.append(oneDev)
            pass

        return HttpResponse(json.dumps(rtnData))

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
                DevLists = DevLists | PaperDevices.objects.filter(orgcode=one)
            else:
                DevLists = PaperDevices.objects.filter(orgcode=one)

        DevLists = DevLists.filter(~Q(state=0))

        # 如果输入了单位
        try:
            ocode = allParams["ocode"]
            DevLists = DevLists.filter(orgcode_id= ocode)
        except:
            pass

        # 如果输入了设备状态
        try:
            dstate = int(allParams["dstate"])
            DevLists = DevLists.filter(state= dstate)
        except:
            pass

        # 如果传入了设备类型
        try:
            typecode = int(allParams["dtype"])
            DevLists = DevLists.filter(typecode= typecode)
        except:
            pass

        # 初始设备数据返回
        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])
        rtnList = []
        for index,oneData in enumerate(DevLists):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue
            oneOrgDict = {}
            oneOrgDict['id'] = oneData.id
            oneOrgDict['code'] = oneData.code
            oneOrgDict['name'] = oneData.name
            oneOrgDict['orgname'] = oneData.orgcode.name
            if oneData.typecode == 1001:
                oneOrgDict['typename'] = "互动桌面"
            elif oneData.typecode == 1002:
                oneOrgDict['typename'] = "二维码屏"
            elif oneData.typecode == 1003:
                oneOrgDict['typename'] = "3D导览"
            elif oneData.typecode == 1004:
                oneOrgDict['typename'] = "全息投影"
            elif oneData.typecode == 1005:
                oneOrgDict['typename'] = "分接屏"
            elif oneData.typecode == 2001:
                oneOrgDict['typename'] = "LED"
            elif oneData.typecode == 2002:
                oneOrgDict['typename'] = "白炽灯"
            elif oneData.typecode == 2003:
                oneOrgDict['typename'] = "荧光灯"


            if oneData.state == 1:
                oneOrgDict['statename'] = "正常"
            elif oneData.state == 2:
                oneOrgDict['statename'] = "故障"
            rtnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(DevLists)
        dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def PowerAdd(request,cmd):
        '''
        注册
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("收到电源注册指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)

        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList :
                powerList = SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                powerList = powerList | PaperDevices.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        # 当前单位下检查名字唯一性
        for onePlay in powerList:
            if onePlay.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("名称重复", request)
                loginResut = json.dumps({"ErrorInfo": "名称重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

            # if onePlay.ipaddress == allParams["ipaddress"]:
            #     loginResut = json.dumps({"ErrorInfo": "控制主机IP冲突", "ErrorId": 20006, "Result": {}})
            #     return HttpResponse(loginResut)

        # 全网机构内检查ip和mac的合法性
        orgRootTemp = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps :
                playerListTemps = SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        for onePlay in playerListTemps:
            if onePlay.ipaddress == allParams["ipaddress"]:
                LoggerHandle.writeLogDevelope("控制器IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "控制器IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        regPower = SmartPowers()
        regPower.code = UtilHelper.UtilHelper.newUuid()
        regPower.orgcode = ownerOrgHandel
        regPower.name = allParams["name"]
        regPower.ipaddress = allParams["ipaddress"]
        regPower.port = allParams["port"]
        regPower.ctrlportnumber = int(allParams["tports"])
        regPower.state = 1
        regPower.type = allParams["type"]
        regPower.portstates = "0000000000000000000000000000000000000000000000000000000000000000"

        try:
            regPower.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def PowerEdit(request,cmd):
        '''
        电源编辑
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("电源编辑指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        
        ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 查询电源数据
        powerObject = SmartPowers.objects.filter(code = allParams["powercode"]).first()

        if not powerObject:
            LoggerHandle.writeLogDevelope("给定的电源数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "给定的电源数据异常", "ErrorId": 20007, "Result": {}})
            return HttpResponse(loginResut)


        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)

        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList :
                powerList = SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                powerList = powerList | PaperDevices.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        # 当前单位下检查名字唯一性
        for onePlay in powerList:
            if onePlay.code != powerObject.code and onePlay.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("名称重复", request)
                loginResut = json.dumps({"ErrorInfo": "名称重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

            # if onePlay.ipaddress == allParams["ipaddress"]:
            #     loginResut = json.dumps({"ErrorInfo": "控制主机IP冲突", "ErrorId": 20006, "Result": {}})
            #     return HttpResponse(loginResut)

        # 全网机构内检查ip和mac的合法性
        orgRootTemp = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps :
                playerListTemps = SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | SmartPowers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        for onePlay in playerListTemps:
            if onePlay.code != powerObject.code and onePlay.ipaddress == allParams["ipaddress"]:
                LoggerHandle.writeLogDevelope("控制器IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "控制器IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果修改了单位，则需要判断是否存在绑定关系
        if ownerOrgHandel.code != powerObject.orgcode_id:
            powerMap = SmartPowerPortMap.objects.filter(powercode=powerObject).first()
            if powerMap:
                loginResut = json.dumps(
                    {"ErrorInfo": "电源已绑定了设备，变更归属单位，请先解除绑定", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

            pass

        # 如果已经注册--- 直接返回成功
        # regPower = SmartPowers()
        # powerObject.code = UtilHelper.UtilHelper.newUuid()
        powerObject.orgcode = ownerOrgHandel
        powerObject.name = allParams["name"]
        powerObject.ipaddress = allParams["ipaddress"]
        powerObject.port = allParams["port"]
        powerObject.ctrlportnumber = int(allParams["tports"])
        # powerObject.state = 1
        powerObject.type = allParams["type"]

        try:
            powerObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def PowerSet(request,cmd):
        '''
        注册
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到电源设置指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)
        #
        # # 检查当前账户是否具有权限
        # ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        # if not ownerOrgHandel:
        #     LoggerHandle.writeLogDevelope("归属单位数据异常", request)
        #     loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        # 查询电源对象
        powerObj = SmartPowers.objects.filter(code=allParams["code"]).first()

        if not powerObj:
            loginResut = json.dumps({"ErrorInfo": "电源数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        commitDataList = []
        powerObj.state = int(allParams["state"])
        commitDataList.append(CommitData(powerObj, 0))

        if powerObj.state == 0:
            bindRecords = SmartPowerPortMap.objects.filter(powercode=powerObj)
            commitDataList.append(CommitData(bindRecords, 1))

        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)
            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)

        except Exception, ex:
            LoggerHandle.writeLogDevelope("操作失败", request)
            loginResut = json.dumps({"ErrorInfo": "操作失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def PowerList(request,cmd):
        '''
        查询终端列表
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("查询终端列表%s" % cmd.encode('utf-8'), request)

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

        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])

        fliterStr = None

        try:
            fliterStr = allParams["fliterstring"]
        except:
            pass
        currentAllOrgs = OrgTree.getOrgTreeObjects(userOrg)
        currentAllOrgs.append(userOrg)

        devicesList = None
        for oneOrg in currentAllOrgs:
            if not devicesList :
                devicesList = SmartPowers.objects.filter(orgcode=oneOrg,state = 1).order_by("-id")
            else:
                devicesList = devicesList | SmartPowers.objects.filter(orgcode=oneOrg,state = 1).order_by("-id")

        dataSets = []
        # 数据刷选
        for index, oneRecord in enumerate(devicesList):
            if fliterStr and len(fliterStr) > 0:
                if fliterStr not in oneRecord.name and fliterStr.lower() not in oneRecord.name.lower():
                    continue

            dataSets.append(oneRecord)
        # 返回数据
        rtnList = []
        for index,oneData in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = oneData.id
            oneOrgDict['code'] = oneData.code
            oneOrgDict['name'] = oneData.name

            oneOrgDict['ipaddress'] = oneData.ipaddress
            oneOrgDict['port'] = oneData.port
            oneOrgDict['orgcode'] = oneData.orgcode_id
            oneOrgDict['orgname'] = oneData.orgcode.name

            oneOrgDict['ctrlportnumber'] = oneData.ctrlportnumber
            oneOrgDict['type'] = oneData.type

            # 电源绑定设备数量
            bindRecords = SmartPowerPortMap.objects.filter(powercode=oneData)

            oneOrgDict['binddevs'] = len(bindRecords)

            rtnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(dataSets)
        dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def PowerInfo(request,cmd):
        '''
        查询终端列表
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("查询终端列表%s" % cmd.encode('utf-8'), request)

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

        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        powerCode = allParams["powercode"]



        powerObj = SmartPowers.objects.filter(~Q(state=0),code = powerCode).first()
        if not powerObj:
            loginResut = json.dumps({"ErrorInfo": "电源数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        # 返回数据
        oneOrgDict = {}
        oneOrgDict['id'] = powerObj.id
        oneOrgDict['code'] = powerObj.code
        oneOrgDict['name'] = powerObj.name
        oneOrgDict['ipaddress'] = powerObj.ipaddress
        oneOrgDict['port'] = powerObj.port
        oneOrgDict['ctrlportnumber'] = powerObj.ctrlportnumber
        oneOrgDict['state'] = powerObj.state
        oneOrgDict['orgcode'] = powerObj.orgcode_id
        oneOrgDict['orgname'] = powerObj.orgcode.name
        oneOrgDict['type'] = powerObj.type

        # 返回登录结果
        lResut = json.dumps(oneOrgDict)
        return HttpResponse(lResut)

    @staticmethod
    def LedRegister(request,cmd):
        '''
        LED注册
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("收到LED注册指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        if allParams["ledtype"] != "0":
            LoggerHandle.writeLogDevelope("未找到LED板卡厂商", request)
            loginResut = json.dumps({"ErrorInfo": "未找到LED板卡厂商", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)

        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList :
                playerList = PaperDevices.objects.filter(orgcode=oneOrg,typecode = 2001,state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg,typecode = 2001,state=1).order_by("-id")

        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("LED设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "LED设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)


        # 全网机构内检查ip和mac的合法性
        orgRootTemp = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps :
                playerListTemps = PaperDevices.objects.filter(orgcode=oneOrg,type = 2001,state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | PaperDevices.objects.filter(orgcode=oneOrg,type = 2001,state=1).order_by("-id")

        for onePlay in playerListTemps:
            if onePlay.mac == allParams["mac"]:
                LoggerHandle.writeLogDevelope("MAC地址已被注册", request)
                loginResut = json.dumps({"ErrorInfo": "MAC地址已被注册", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)
            if onePlay.ipaddress == allParams["ipaddress"]:
                LoggerHandle.writeLogDevelope("IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        regPlayer = PaperDevices()
        regPlayer.code = UtilHelper.UtilHelper.newUuid()
        regPlayer.orgcode = ownerOrgHandel
        # regPlayer.orgcode_id = allParams["orgsign"]
        regPlayer.name = allParams["name"]
        regPlayer.ipaddress = allParams["ipaddress"]
        regPlayer.mac = allParams["mac"]
        regPlayer.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        regPlayer.terminalsign = regPlayer.code
        regPlayer.typecode = 2001
        regPlayer.state = 1
        regPlayer.port = int(allParams["port"])
        regPlayer.externinfo1 = int(allParams["Width"])
        regPlayer.externinfo2 = int(allParams["Height"])
        regPlayer.externinfo3 = int(allParams["LedType"])

        try:
            regPlayer.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def LedEdit(request,cmd):
        '''
        LED注册
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到LED编辑指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

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

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code=allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        if allParams["ledtype"] != "0":
            LoggerHandle.writeLogDevelope("未找到LED板卡厂商", request)
            loginResut = json.dumps({"ErrorInfo": "未找到LED板卡厂商", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查led设备是否存在
        ledDevice = PaperDevices.objects.filter(typecode=2001,code=allParams["ledcode"],state=1).first()
        if not ledDevice:
            LoggerHandle.writeLogDevelope("LED设备数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "LED设备数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)

        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList:
                playerList = PaperDevices.objects.filter(orgcode=oneOrg, typecode=2001, state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg, typecode=2001, state=1).order_by(
                    "-id")

        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"] and onePlay.code != ledDevice.code:
                LoggerHandle.writeLogDevelope("LED设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "LED设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 全网机构内检查ip和mac的合法性
        orgRootTemp = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps:
                playerListTemps = PaperDevices.objects.filter(orgcode=oneOrg, type=0, state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | PaperDevices.objects.filter(orgcode=oneOrg, type=0,
                                                                                state=1).order_by("-id")

        for onePlay in playerListTemps:
            if onePlay.mac == allParams["mac"] and onePlay.code != ledDevice.code:
                LoggerHandle.writeLogDevelope("MAC地址已被注册", request)
                loginResut = json.dumps({"ErrorInfo": "MAC地址已被注册", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)
            if onePlay.ipaddress == allParams["ipaddress"] and onePlay.code != ledDevice.code:
                LoggerHandle.writeLogDevelope("IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        # regPlayer = PaperDevices()
        # ledDevice.code = UtilHelper.UtilHelper.newUuid()
        ledDevice.orgcode = ownerOrgHandel
        # ledDevice.orgcode_id = allParams["orgsign"]
        ledDevice.name = allParams["name"]
        ledDevice.ipaddress = allParams["ipaddress"]
        ledDevice.mac = allParams["mac"]
        ledDevice.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ledDevice.terminalsign = ledDevice.code
        ledDevice.typecode = 2001
        ledDevice.state = 1
        ledDevice.port = int(allParams["port"])
        ledDevice.externinfo1 = int(allParams["Width"])
        ledDevice.externinfo2 = int(allParams["Height"])
        ledDevice.externinfo3 = int(allParams["LedType"])

        try:
            ledDevice.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("修改LED信息失败", request)
            loginResut = json.dumps({"ErrorInfo": "修改LED信息失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def LightRegister(request,cmd):
        '''
        LED注册
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("收到灯光注册指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        userOrg, userHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)


        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, userHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)
        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList :
                playerList = PaperDevices.objects.filter(orgcode=oneOrg,typecode = 2002 ,state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg,typecode = 2002 ,state=1).order_by("-id")

        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        regPlayer = PaperDevices()
        regPlayer.code = UtilHelper.UtilHelper.newUuid()
        regPlayer.orgcode = ownerOrgHandel
        # regPlayer.orgcode_id = allParams["orgsign"]
        regPlayer.name = allParams["name"]
        regPlayer.gcode = None  # 新终端未分组
        regPlayer.ipaddress = None
        regPlayer.mac = None
        regPlayer.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        regPlayer.terminalsign = None
        regPlayer.typecode = int(allParams["type"])
        regPlayer.state = 1
        regPlayer.port = -1
        regPlayer.externinfo4 = int(allParams["type"])
        regPlayer.externinfo5 = int(allParams["issmart"])

        try:
            regPlayer.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "注册成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def LightEdit(request,cmd):
        '''
         LED注册
         :param request:
         :return:
         '''

        LoggerHandle.writeLogDevelope("收到灯光修改指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

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


        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code=allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查灯光是否存在
        lightObject = PaperDevices.objects.filter(code=allParams["lightcode"],state=1).first()
        if not lightObject:
            loginResut = json.dumps({"ErrorInfo": "灯光数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 如果修改了单位，则需要判断是否存在绑定关系
        if ownerOrgHandel.code != lightObject.orgcode_id:
            mapHandle = SmartGroupDeviceMap.objects.filter(devicecode=lightObject).first()
            if mapHandle:
                loginResut = json.dumps({"ErrorInfo": "当前灯光绑定的分区所归属单位同新单位不一致，请先解除原有分区", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

            powerMap = SmartPowerPortMap.objects.filter(devcode=lightObject).first()
            if powerMap:
                loginResut = json.dumps(
                    {"ErrorInfo": "当前灯光绑定的电源所归属单位同新单位不一致，请先解除原有电源", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

            # 更换单位，清空设备坐标信息
            lightObject.leftx = 0
            lightObject.lefty=0
            lightObject.width = 0
            lightObject.height = 0
            pass

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)
        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList:
                playerList = PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by(
                    "-id")

        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"] and onePlay.code != lightObject.code:
                LoggerHandle.writeLogDevelope("设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        # regPlayer = PaperDevices()
        # lightObject.code = UtilHelper.UtilHelper.newUuid()
        lightObject.orgcode = ownerOrgHandel
        lightObject.name = allParams["name"]
        lightObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        lightObject.typecode = int(allParams["type"])
        lightObject.externinfo5 = int(allParams["issmart"])
        lightObject.externinfo4 = int(allParams["type"])

        try:
            lightObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "注册成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def DeviceAdd(request,cmd):
        '''

         :param request:
         :return:
         '''
        LoggerHandle.writeLogDevelope("收到设备修改指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

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

        # 检查logioncode是否为权力机构
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle or not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户或单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户或单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code=allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # # 检查灯光是否存在
        # deviceObject = PaperDevices.objects.filter(code=allParams["code"]).first()
        #
        # if not deviceObject or deviceObject.state == 0:
        #     loginResut = json.dumps({"ErrorInfo": "设备数据异常", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)
        #
        # if deviceObject.typecode == 2001 or deviceObject.typecode == 2002:
        #     loginResut = json.dumps({"ErrorInfo": "该接口不支持灯光、LED编辑", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)
        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList:
                playerList = PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by(
                    "-id")

        # playerList = playerList.filter(~Q(typecode=2001))
        # playerList = playerList.filter(~Q(typecode=2002))
        # playerList = playerList.filter(typecode__lte=2000)


        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"] and onePlay.state != 0:
                LoggerHandle.writeLogDevelope("设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 全网机构内检查ip和mac的合法性
        orgRootTemp = PaperOrgs.objects.filter(code=acntHandle.orgcode.code).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)

        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps:
                playerListTemps = PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
        # playerListTemps = playerListTemps.filter(~Q(typecode=2001))
        # playerListTemps = playerListTemps.filter(~Q(typecode=2002))

        # playerListTemps = playerListTemps.filter(typecode__lte=2000)

        for onePlay in playerListTemps:
            if onePlay.mac == allParams["mac"]:
                LoggerHandle.writeLogDevelope("MAC地址已被注册", request)
                loginResut = json.dumps({"ErrorInfo": "MAC地址已被注册", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)
            if onePlay.ipaddress == allParams["ipaddress"]:
                LoggerHandle.writeLogDevelope("IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # # 如果修改了单位，则需要判断是否存在绑定关系
        # if ownerOrgHandel.code != deviceObject.orgcode_id:
        #     mapHandle = SmartGroupDeviceMap.objects.filter(devicecode=deviceObject).first()
        #     if mapHandle:
        #         loginResut = json.dumps({"ErrorInfo": "当前设备绑定的分区所归属单位同新单位不一致，请先解除原有分区", "ErrorId": 20006, "Result": {}})
        #         return HttpResponse(loginResut)
        #
        #     powerMap = SmartPowerPortMap.objects.filter(devcode=deviceObject).first()
        #     if powerMap:
        #         loginResut = json.dumps(
        #             {"ErrorInfo": "当前设备绑定的电源所归属单位同新单位不一致，请先解除原有电源", "ErrorId": 20006, "Result": {}})
        #         return HttpResponse(loginResut)
        #
        #     # 更换单位，清空设备坐标信息
        #     deviceObject.leftx = 0
        #     deviceObject.lefty=0
        #     deviceObject.width = 0
        #     deviceObject.height = 0
        #     pass

        # postParm[0] = "name=" + name;
        # postParm[1] = "ipaddress=" + ipaddress;
        # postParm[2] = "mac=" + macaddress;
        # postParm[3] = "state=" + state_list;
        # postParm[4] = "devtype=" + dev_type;
        # postParm[5] = "orgcode=" + ownerOrg;
        # postParm[6] = "managename=" + managename;
        # postParm[7] = "managephone=" + managephone;
        # postParm[8] = "longitude=" + longitude;
        # postParm[9] = "latitude=" + latitude;
        #
        # 如果已经注册--- 直接返回成功
        deviceObject = PaperDevices()
        deviceObject.code = UtilHelper.UtilHelper.newUuid()
        deviceObject.name = allParams["name"]
        deviceObject.ipaddress = allParams["ipaddress"]
        deviceObject.mac = allParams["mac"]
        deviceObject.state = int(allParams["state"])
        deviceObject.devtype = allParams["devtype"]
        deviceObject.orgcode = ownerOrgHandel

        deviceObject.managename = allParams["managename"]
        deviceObject.managephone = allParams["managephone"]

        deviceObject.longitude = allParams["longitude"]
        deviceObject.latitude = allParams["latitude"]


        deviceObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # deviceObject.port = allParams["port"]


        try:
            deviceObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("修改设备失败", request)
            loginResut = json.dumps({"ErrorInfo": "修改设备失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def DeviceEdit(request,cmd):
        '''

         :param request:
         :return:
         '''
        LoggerHandle.writeLogDevelope("收到设备修改指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # # 验证参数完整性
        # paramCompleteness, info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)
        #
        # if paramCompleteness:
        #     LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
        #     loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
        #     return HttpResponse(loginResut)
        #
        # # 参数验签
        # verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        # if verifyResult:
        #     LoggerHandle.writeLogDevelope("参数验签成功", request)
        # else:
        #     LoggerHandle.writeLogDevelope("参数验签失败", request)
        #     loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
        #     return HttpResponse(loginResut)

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)
        #
        # # 检查当前账户是否具有权限
        # resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        # if not resultPrivilegeSign:
        #     LoggerHandle.writeLogDevelope("权限受限", request)
        #     loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)
        #
        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code=allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)


        # 检查灯光是否存在
        deviceObject = PaperDevices.objects.filter(code=allParams["code"]).first()

        if not deviceObject or deviceObject.state == 0:
            loginResut = json.dumps({"ErrorInfo": "设备数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)
        #
        # if deviceObject.typecode == 2001 or deviceObject.typecode == 2002:
        #     loginResut = json.dumps({"ErrorInfo": "该接口不支持灯光、LED编辑", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(acntHandle.orgcode)
        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(acntHandle.orgcode)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList:
                playerList = PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
            else:
                playerList = playerList | PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by(
                    "-id")

        # playerList = playerList.filter(~Q(typecode=2001))
        # playerList = playerList.filter(~Q(typecode=2002))
        # playerList = playerList.filter(typecode__lte=2000)


        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.name == allParams["name"] and onePlay.code != deviceObject.code:
                LoggerHandle.writeLogDevelope("设备名字重复", request)
                loginResut = json.dumps({"ErrorInfo": "设备名字重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # 全网机构内检查ip和mac的合法性
        # orgRootTemp = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        orgRootTemp = OrgTree.getRootOrg(acntHandle.orgcode)
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTemps = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTemps:
                playerListTemps = PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
            else:
                playerListTemps = playerListTemps | PaperDevices.objects.filter(orgcode=oneOrg, state=1).order_by("-id")
        # playerListTemps = playerListTemps.filter(~Q(typecode=2001))
        # playerListTemps = playerListTemps.filter(~Q(typecode=2002))

        # playerListTemps = playerListTemps.filter(typecode__lte=2000)

        for onePlay in playerListTemps:
            if onePlay.mac == allParams["mac"] and onePlay.code != deviceObject.code:
                LoggerHandle.writeLogDevelope("MAC地址已被注册", request)
                loginResut = json.dumps({"ErrorInfo": "MAC地址已被注册", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)
            if onePlay.ipaddress == allParams["ipaddress"] and onePlay.code != deviceObject.code:
                LoggerHandle.writeLogDevelope("IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        # # 如果修改了单位，则需要判断是否存在绑定关系
        # if ownerOrgHandel.code != deviceObject.orgcode_id:
        #     mapHandle = SmartGroupDeviceMap.objects.filter(devicecode=deviceObject).first()
        #     if mapHandle:
        #         loginResut = json.dumps({"ErrorInfo": "当前设备绑定的分区所归属单位同新单位不一致，请先解除原有分区", "ErrorId": 20006, "Result": {}})
        #         return HttpResponse(loginResut)
        #
        #     powerMap = SmartPowerPortMap.objects.filter(devcode=deviceObject).first()
        #     if powerMap:
        #         loginResut = json.dumps(
        #             {"ErrorInfo": "当前设备绑定的电源所归属单位同新单位不一致，请先解除原有电源", "ErrorId": 20006, "Result": {}})
        #         return HttpResponse(loginResut)
        #
        #     # 更换单位，清空设备坐标信息
        #     deviceObject.leftx = 0
        #     deviceObject.lefty=0
        #     deviceObject.width = 0
        #     deviceObject.height = 0
        #     pass

        # 如果已经注册--- 直接返回成功
        # deviceObject.name = allParams["name"]
        # deviceObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # deviceObject.ipaddress = allParams["ipaddress"]
        # deviceObject.mac = allParams["mac"]
        # deviceObject.port = allParams["port"]
        # deviceObject.orgcode = ownerOrgHandel
        # deviceObject.state = int(allParams["state"])
        # deviceObject.typecode = int(allParams["devtype"])
        deviceObject.name = allParams["name"]
        deviceObject.ipaddress = allParams["ipaddress"]
        deviceObject.mac = allParams["mac"]
        deviceObject.state = int(allParams["state"])
        deviceObject.devtype = allParams["devtype"]
        deviceObject.orgcode = ownerOrgHandel

        deviceObject.managename = allParams["managename"]
        deviceObject.managephone = allParams["managephone"]

        deviceObject.longitude = allParams["longitude"]
        deviceObject.latitude = allParams["latitude"]


        deviceObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        try:
            deviceObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("修改设备失败", request)
            loginResut = json.dumps({"ErrorInfo": "修改设备失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def SetDevice(request,cmd):
        '''
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到设备修改指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

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

        # userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # # 检查当前账户是否具有权限
        # resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        # if not resultPrivilegeSign:
        #     LoggerHandle.writeLogDevelope("权限受限", request)
        #     loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        # 检查灯光是否存在
        deviceObject = PaperDevices.objects.filter(code=allParams["code"], state=1).first()
        if not deviceObject:
            loginResut = json.dumps({"ErrorInfo": "设备数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        deviceObject.state = int(allParams["state"])
        deviceObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        try:
            deviceObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("设置设备失败", request)
            loginResut = json.dumps({"ErrorInfo": "修改设备失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def getDevStateInfo(devHandle):
        if not devHandle or not isinstance(devHandle,PaperDevices):
            return None,None

        if devHandle.state == 1:
            return "正常"
        elif devHandle.state == 21:
            return "缺纸"
        elif devHandle.state == 22:
            return "纸将尽"
        elif devHandle.state == 23:
            return "堵纸"
        elif devHandle.state == 24:
            return "卡纸"
        elif devHandle.state == 5:
            return "换纸成功"
        elif devHandle.state == 6:
            return "开机"
        elif devHandle.state == 7:
            return "关机"
        elif devHandle.state == 8:
            return "售卖机故障"
        elif devHandle.state == 20:
            return "其他故障"
    @staticmethod
    def DeviceList(request,cmd):
        '''
        查询终端列表
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("查询终端列表%s" % cmd.encode('utf-8'), request)

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

        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # # 检查当前账户是否具有权限
        # resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        # if not resultPrivilegeSign:
        #     LoggerHandle.writeLogDevelope("权限受限", request)
        #     loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
        #     return HttpResponse(loginResut)

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])

        fliterStr = None

        try:
            fliterStr = allParams["fliterstring"]
        except:
            pass

        typeCode = None
        try:
            typeCode = int(allParams["typecode"])
        except:
            pass

        currentAllOrgs = OrgTree.getOrgTreeObjects(userOrg)
        currentAllOrgs.append(userOrg)

        devicesList = None
        for oneOrg in currentAllOrgs:
            if not devicesList :
                devicesList = PaperDevices.objects.filter(orgcode=oneOrg).order_by("-id")
            else:
                devicesList = devicesList | PaperDevices.objects.filter(orgcode=oneOrg).order_by("-id")

        devicesList = devicesList.filter(~Q(state = 0))

        # 根据终端类型过滤

        # if typeCode == None:
        #     pass
        # elif typeCode == -1:
        #     devicesList = devicesList.filter(typecode__lte=2000)
        # elif typeCode == 1:
        #     devicesList = devicesList.filter(typecode__gte=2000)
        # else:
        #     devicesList = devicesList.filter(typecode=typeCode)

        dataSets = []
        # 数据刷选
        for index, oneRecord in enumerate(devicesList):
            if fliterStr and len(fliterStr) > 0:
                if fliterStr not in oneRecord.name and fliterStr.lower() not in oneRecord.name.lower():
                    continue

            dataSets.append(oneRecord)




        # 设备类型 < 2000 ---基础设备，显示资源占用
        # 设备类型 = 2001 ---LED设备， 显示开断，电源
        # 设备类型 = 2002 ---灯光设备， 显示开断，电源

        # 返回数据
        rtnList = []
        for index,oneData in enumerate(dataSets):
            if index < limit*(pageIndex - 1) or index >= limit*pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = oneData.id
            oneOrgDict['code'] = oneData.code
            oneOrgDict['name'] = oneData.name
            oneOrgDict['ipaddress'] = oneData.ipaddress
            oneOrgDict['mac'] = oneData.mac
            oneOrgDict['orgcode'] = oneData.orgcode_id
            oneOrgDict['orgname'] = oneData.orgcode.name

            oneOrgDict['devtype'] = oneData.devtype
            oneOrgDict['devtypename'] = "智能取纸售卖一体机"

            oneOrgDict['devstate'] = oneData.state
            oneOrgDict['managename'] = oneData.managename
            oneOrgDict["managephone"] = oneData.managephone
            oneOrgDict["longitude"] = oneData.longitude
            oneOrgDict["latitude"] = oneData.latitude

            oneOrgDict["resource"] = 0

            customTemplate = "<div id='%s_1' onmouseover='$.viewResource(\"%s\",\"%s\",\"%s_1\")' onmouseout='$.closeResourceTips()' style='width: 30px;height: 30px;text-align:center'>" \
                                      '<img src="/static/images/custom.png" width="30px" height="30px" /> ' + "</div>"

            customTemplate = customTemplate % (oneData.code,oneData.managename, oneData.managephone,oneData.code)


            locationTemplate = "<div id='%s_2' onclick='$.openMap()' onmouseover='$.viewLocation(\"%s\",\"%s\",\"%s_2\")' onmouseout='$.closeResourceTips()' style='width: 20px;height: 30px;text-align:center;cursor:pointer'>" \
                                      '<img src="/static/images/location.png" width="20px" height="30px" /> ' + "</div>"

            locationTemplate = locationTemplate.decode("utf-8")
            locationTemplate = locationTemplate % (oneData.code,oneData.longitude, oneData.latitude,oneData.code)
            oneOrgDict["position"] = locationTemplate


            oneOrgDict["mangeinfo"] =customTemplate
            oneOrgDict['statename'] = DeviceApi.getDevStateInfo(oneData)

            #
            # # 智能终端才有
            # if typeCode < 2000:
            #     # 终端状态
            #     playerState = PaperDevicestat.objects.filter(terminalcode = oneData).order_by("-recordtime").first()
            #     if not playerState:
            #         oneOrgDict['cpu'] = "0"
            #         oneOrgDict['disk'] = "0"
            #         oneOrgDict['memory'] = "0"
            #         oneOrgDict["resource"] = "<div style='width: 5px;height: 10px;background: #cf3a02'></div>" + "<div style='width: 5px;height: 10px;background: green'></div>" + "<div style='width: 5px;height: 10px;background: #1E9FFF'></div>"
            #         oneOrgDict['lastupdatetime'] = oneData.lastlogintime
            #     else:
            #         oneOrgDict['cpu'] = playerState.cpu
            #         oneOrgDict['disk'] = playerState.disk
            #         oneOrgDict['memory'] = playerState.memory
            #         oneOrgDict["resource"] = "<div id='%s_0' onmouseover='$.viewResource(0,%d,\"%s_0\")' onmouseout='$.closeResourceTips()' style='width: %dpx;height: 10px;background: #cf3a02 ;'></div>"%(oneData.code,playerState.cpu,oneData.code,playerState.cpu) \
            #                                  + "<div id='%s_1' onmouseover='$.viewResource(1,%d,\"%s_1\")' onmouseout='$.closeResourceTips()' style='width: %dpx;height: 10px;background: green'></div>"%(oneData.code,playerState.disk,oneData.code,playerState.disk ) \
            #                                  + "<div id='%s_2' onmouseover='$.viewResource(2,%d,\"%s_2\")' onmouseout='$.closeResourceTips()' style='width: %dpx;height: 10px;background: #1E9FFF'></div>"%(oneData.code,playerState.memory,oneData.code,playerState.memory)
            #         oneOrgDict['lastupdatetime'] = playerState.recordtime
            #
            #
            # grpMap = SmartGroupDeviceMap.objects.filter(devicecode=oneData).first()
            #
            # if not grpMap:
            #     oneOrgDict["groupname"] = "未绑定"
            #     oneOrgDict["groupcode"] = None
            # else:
            #     oneOrgDict["groupname"] = grpMap.groupcode.name
            #     oneOrgDict["groupcode"] = grpMap.groupcode.code
            #
            # powerMap = SmartPowerPortMap.objects.filter(devcode=oneData).first()
            # if not powerMap:
            #     oneOrgDict["powername"] = "未绑定"
            #     oneOrgDict["powercode"] = None
            #     oneOrgDict["powerport"] = "未设置"
            #     oneOrgDict["state"] = "未设置"
            #     oneOrgDict["state"] = "未设置"
            #
            #     oneOrgDict["statename"] =  '<i class="layui-icon" style="font-size: 24px">&#xe64d;</i>   '
            # else:
            #     oneOrgDict["powername"] = u"%s(%d号端子)"% (powerMap.powercode.name , powerMap.port)
            #     oneOrgDict["powercode"] = powerMap.powercode.code
            #     oneOrgDict["powerport"] = powerMap.port
            #     oneOrgDict["state"] = "未设置"
            #
            #     portStat = powerMap.powercode.portstates[powerMap.port - 1]
            #     if int(portStat) == 0:
            #         oneOrgDict["statename"] = "<div style='width: 20px;height: 20px;background: #6c6c6c;border-radius: 10px'></div>"
            #     else:
            #         oneOrgDict[
            #             "statename"] = "<div style='width: 20px;height: 20px;background: #009100;border-radius: 10px'></div>"
            #     # 检查端子是否接通
            #     # oneOrgDict["statename"] = "<div style='width: 20px;height: 20px;background: #009100;border-radius: 10px'></div>"

            rtnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(dataSets)
        dictRtn["data"] = rtnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def DeviceInfo(request,cmd):
        '''
        LED查询
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到设备查询指令%s"%cmd.encode('utf-8'), request)
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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        # userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not acntHandle or not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)


        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        # ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        devHandles = PaperDevices.objects.filter(code=allParams["devcode"])
        devHandle = devHandles.filter(~Q(state = 0)).first()

        # 检查当前账号是否具有当前权限
        if not devHandle:
            LoggerHandle.writeLogDevelope("当前设备数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前设备数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        oneOrgDict = {}
        oneOrgDict['id'] = devHandle.id
        oneOrgDict['code'] = devHandle.code
        oneOrgDict['name'] = devHandle.name


        oneOrgDict['ipaddress'] = devHandle.ipaddress
        oneOrgDict['mac'] = devHandle.mac
        # oneOrgDict['port'] = devHandle.port


        oneOrgDict['managename'] = devHandle.managename
        oneOrgDict['managephone'] = devHandle.managephone
        oneOrgDict['orgcode'] = devHandle.orgcode.code

        if len(devHandle.orgcode.name) > 7:
            oneOrgDict['orgname'] = devHandle.orgcode.name[:7] + "..."
        else:
            oneOrgDict['orgname'] = devHandle.orgcode.name

        oneOrgDict['lastlogintime'] = devHandle.lastlogintime
        oneOrgDict['state'] = devHandle.state
        oneOrgDict['longitude'] = devHandle.longitude
        oneOrgDict['latitude'] = devHandle.latitude

        oneOrgDict['devtype'] = devHandle.devtype
        oneOrgDict['typename'] = "智能取纸售卖一体机"
        #
        # # 查询设备资源时间流图
        # devStatsQuerySet = PaperDevicestat.objects.filter(terminalcode=devHandle).order_by("-recordtime")[:10]
        #
        # devStats = []
        # for oneSet in devStatsQuerySet:
        #     devStats.append(oneSet)
        #
        # # devStats = devStats.sort()
        # devStats = sorted(devStats, cmp=lambda x, y: -cmp(y.recordtime,x.recordtime))
        #
        # statList = []
        # for one in devStats:
        #     oneStat = {}
        #     oneStat["cpu"] = one.cpu
        #     oneStat["memory"] = one.memory
        #     oneStat["disk"] = one.disk
        #     oneStat["recordtime"] = one.recordtime
        #     statList.append(oneStat)
        #
        #     if len(statList) > 10:
        #         break
        #
        # oneOrgDict['stats'] = statList

        # 返回登录结果
        lResut = json.dumps(oneOrgDict)
        return HttpResponse(lResut)

    @staticmethod
    def DeviceControl(request,cmd):
        '''
        播放器删除
        :param request:
        :return:
        '''
        return
        LoggerHandle.writeLogDevelope("收到播放器删除指令%s"%cmd.encode('utf-8'), request)
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
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)


        # 检查logioncode是否为权力机构
        acntHandle = SmartAccount.objects.filter(account = allParams["logincode"]).first()

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

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code = allParams["orgsign"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 暂不做单位联合查询---理论上不会出问题
        playCode = allParams["code"]
        playerHandle = PaperDevices.objects.filter(code = playCode).first()
        # 检查播放器是否存在
        if not playerHandle:
            LoggerHandle.writeLogDevelope("播放器数据不存在或已被删除", request)
            loginResut = json.dumps({"ErrorInfo": "播放器数据不存在或已被删除", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        commitDataList = []


        # # 删除license绑定关系
        # licData = ByAdLicense.objects.filter(terminalcode = playerHandle).first()
        # if licData:
        #     licData.terminalcode = None
        #     commitDataList.append(CommitData(licData, 0))
        #
        # # 删除播放盒绑定关系
        # boxMapData = ByAdBoxPlayerMap.objects.filter(playercode = playerHandle).first()
        # if boxMapData:
        #     commitDataList.append(CommitData(boxMapData, 1))

        # 删除播放器状态数据
        stateData = PaperDevicestat.objects.filter(terminalcode = playerHandle).first()
        if stateData:
            commitDataList.append(CommitData(stateData, 1))

        # 清空下载状态数据
        # downloadData = ByAdPlayerDownload.objects.filter(terminalcode = playerHandle)
        # commitDataList.append(CommitData(stateData, 1))

        # 设置播放器未删除状态
        playerHandle.state = 0
        commitDataList.append(CommitData(playerHandle, 0))

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
        loginResut = json.dumps({"ErrorInfo": "终端登记成功，请联系管理员授权", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def SetDevPosition(request,cmd):
        '''
         LED查询
         :param request:
         :return:
         '''
        LoggerHandle.writeLogDevelope("收到设备查询指令%s" % cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

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

        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"], allParams["orgsign"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = PaperOrgs.objects.filter(code=allParams["orgsign"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        devHandle = PaperDevices.objects.filter(code=allParams["devcode"], state=1).first()

        # 检查当前账号是否具有当前权限
        if not devHandle:
            LoggerHandle.writeLogDevelope("当前设备数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前设备数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        commitDataList = []

        # 设置播放器未删除状态
        devHandle.leftx = int(allParams["leftx"])
        devHandle.lefty = int(allParams["lefty"])
        devHandle.width = int(allParams["width"])
        devHandle.height = int(allParams["height"])

        commitDataList.append(CommitData(devHandle, 0))

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

    ########################################################################################
    @staticmethod
    def goLightList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增播放盒页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/light_list.html'), dict)

    @staticmethod
    def goLightAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开终端列表页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/light_add.html'), dict)

    @staticmethod
    def goLightEdit(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开灯光编辑页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/light_edit.html'), dict)


    @staticmethod
    def goTerminalLedList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开LED终端列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/group_list.html'), dict)

    @staticmethod
    def goTerminalAddLed(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/group_add.html'), dict)

    @staticmethod
    def goTerminalEditLed(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/group_edit.html'), dict)


    @staticmethod
    def goPowerList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开LED终端列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/power_list.html'), dict)

    @staticmethod
    def goPowerAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/power_add.html'), dict)

    @staticmethod
    def goPowerEdit(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/power_edit.html'), dict)


    @staticmethod
    def goTerminalList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/base_device.html'), dict)

    @staticmethod
    def goTerminalEdit(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/device_edit.html'), dict)


    @staticmethod
    def goLedList(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开LED终端列表页面", request)
        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/led_list.html'), dict)

    @staticmethod
    def goLedAdd(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/led_add.html'), dict)

    @staticmethod
    def goLedEdit(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开新增LED终端页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/led_edit.html'), dict)

    @staticmethod
    def goGroupBind(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开绑定页面", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/group_bind.html'), dict)

    @staticmethod
    def goDeviceView(request):
        dict = {}
        LoggerHandle.writeLogDevelope("设备查阅", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/device_view.html'), dict)

    @staticmethod
    def goGoodsView(request):
        dict = {}
        LoggerHandle.writeLogDevelope("商品管理", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/goods_manage.html'), dict)

    @staticmethod
    def goAddGoods(request):
        dict = {}
        LoggerHandle.writeLogDevelope("添加商品", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/goods_add.html'), dict)

    @staticmethod
    def goOrderView(request):
        dict = {}
        LoggerHandle.writeLogDevelope("订单管理", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/order_manage.html'), dict)


