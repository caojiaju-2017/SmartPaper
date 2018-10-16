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

class GoodsApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)

        if command == "GOODS_ADD".upper():
            return GoodsApi.GoodsAdd(req,command)
        elif command == "GOODS_LIST".upper():
            return GoodsApi.GoodsList(req,command)
        elif command == "GOODS_QUERY".upper():
            return GoodsApi.GoodsQuery(req, command)
        elif command == "SET_GOODS".upper():
            return GoodsApi.SetGoods(req, command)


    @staticmethod
    def SetGoods(request,cmd):
        '''
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到商品删除指令%s" % cmd.encode('utf-8'), request)
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

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()
        if not acntHandle.orgcode:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)

        # 检查灯光是否存在
        goodsObject = PaperGoods.objects.filter(code=allParams["code"], state=1).first()
        if not goodsObject:
            loginResut = json.dumps({"ErrorInfo": "设备数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 如果已经注册--- 直接返回成功
        goodsObject.state = int(allParams["state"])
        # goodsObject.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        try:
            goodsObject.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("设置商品失败", request)
            loginResut = json.dumps({"ErrorInfo": "修改商品失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def GoodsQuery(request,cmd):
        '''
        商品查询
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("收到商品查询指令%s"%cmd.encode('utf-8'), request)
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
        goodsHandles = PaperGoods.objects.filter(code=allParams["code"])
        devHandle = goodsHandles.filter(~Q(state = 0)).first()

        # 检查当前账号是否具有当前权限
        if not devHandle:
            LoggerHandle.writeLogDevelope("当前商品数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前商品数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        oneOrgDict = {}
        oneOrgDict['goodsname'] = devHandle.name
        oneOrgDict['goodsprice'] = devHandle.price
        oneOrgDict['orgcode'] = devHandle.orgcode.code
        oneOrgDict['previewimage'] = "/static/GoodsImage/%s.jpg"%allParams["code"]

        # 返回登录结果
        lResut = json.dumps(oneOrgDict)
        return HttpResponse(lResut)

    @staticmethod
    def GoodsList(request,cmd):
        '''
        查询终端列表
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("查询商品列表%s" % cmd.encode('utf-8'), request)

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

        userOrg, acntHandle = OrgTree.getUserOrg(allParams["logincode"])
        if not userOrg:
            LoggerHandle.writeLogDevelope("用户单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "用户单位数据异常", "ErrorId": 20008, "Result": {}})
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

        goodsList = None
        for oneOrg in currentAllOrgs:
            if not goodsList :
                goodsList = PaperGoods.objects.filter(orgcode=oneOrg).order_by("-id")
            else:
                goodsList = goodsList | PaperGoods.objects.filter(orgcode=oneOrg).order_by("-id")

        goodsList = goodsList.filter(~Q(state = 0))

        dataSets = []
        # 数据刷选
        for index, oneRecord in enumerate(goodsList):
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
            oneOrgDict['price'] = oneData.price
            oneOrgDict['model'] = oneData.model
            oneOrgDict['info'] = oneData.info
            oneOrgDict['simage'] = oneData.simage

            oneOrgDict['limage'] = oneData.limage
            oneOrgDict['state'] = oneData.state

            oneOrgDict['orgcode'] = oneData.orgcode.code
            oneOrgDict['orgname'] = oneData.orgcode.name



            imageTemplate = "<div id='%s_1' style='width: 100px;height: 80px;text-align:center'>" \
                                      '<img src="/static/GoodsImage/%s.jpg" width="80px" height="80px" /> ' + "</div>"
            imageTemplate = imageTemplate % (oneData.code,oneData.code)
            oneOrgDict['goodsimage'] = imageTemplate

            oneOrgDict["savecount"] = 0  #此处需要计算
            #
            # customTemplate = "<div id='%s_1' onmouseover='$.viewResource(\"%s\",\"%s\",\"%s_1\")' onmouseout='$.closeResourceTips()' style='width: 30px;height: 30px;text-align:center'>" \
            #                           '<img src="/static/images/custom.png" width="30px" height="30px" /> ' + "</div>"
            #
            # customTemplate = customTemplate % (oneData.code,oneData.managename, oneData.managephone,oneData.code)
            #
            #
            # locationTemplate = "<div id='%s_2' onclick='$.openMap()' onmouseover='$.viewLocation(\"%s\",\"%s\",\"%s_2\")' onmouseout='$.closeResourceTips()' style='width: 20px;height: 30px;text-align:center;cursor:pointer'>" \
            #                           '<img src="/static/images/location.png" width="20px" height="30px" /> ' + "</div>"
            #
            # locationTemplate = locationTemplate.decode("utf-8")
            # locationTemplate = locationTemplate % (oneData.code,oneData.longitude, oneData.latitude,oneData.code)
            # oneOrgDict["position"] = locationTemplate
            #
            #
            # oneOrgDict["mangeinfo"] =customTemplate
            # oneOrgDict['statename'] = DeviceApi.getDevStateInfo(oneData)

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
    @csrf_exempt
    def uploadGoodsData(request):
        code = None
        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)
        allParams = {}
        allParams.update(getParams)
        allParams.update(postParams)
        # allParams = dict(getParams.items() + postParams.items())

        if not allParams.has_key("goodsname") or \
                not allParams.has_key("goodsprice") or \
                not allParams.has_key("orgcode") or \
                not allParams.has_key("logincode"):
            loginResut = json.dumps({"ErrorInfo": "参数错误", "ErrorId": 2999, "Result": {}})
            return HttpResponse(loginResut)

        acntHandle = PaperAccount.objects.filter(account=allParams["logincode"]).first()

        existCode = allParams["code"]
        orgcode = allParams["orgcode"]

        newGoods = True
        if not existCode or existCode == "" or len(existCode) != 32:
            newGoods = True
        else:
            newGoods = False

        existGoodsHandle = None
        # 检查商品是否存在
        if not newGoods:
            existGoodsHandle = PaperGoods.objects.filter(code = existCode).first()
            if not existGoodsHandle:
                return HttpResponse("Goods Exception !")
        else:
            existGoodsHandle = PaperGoods()
            existGoodsHandle.code = UtilHelper.UtilHelper.newUuid()
            existGoodsHandle.state = 1

        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
            pass
        else:
            fileInfo = UtilHelper.UtilHelper.GetFileNameAndExt(myFile.name)
            shortName = fileInfo[0]
            fileExtName = ""
            if len(fileInfo) == 2:
                fileExtName = fileInfo[1]

            savePath = GoodsApi.getStoragePath()

            fileUUID = existGoodsHandle.code

            lastSavePath = os.path.join(savePath,fileUUID + ".jpg")

            destination = open(lastSavePath, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        # 写入数据库
        existGoodsHandle.name = allParams["goodsname"]
        existGoodsHandle.orgcode_id = orgcode
        existGoodsHandle.price = allParams["goodsprice"]
        # existGoodsHandle.version = postParams["versioncode"]
        existGoodsHandle.regtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        try:
            existGoodsHandle.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("文件记录失败", request)
            loginResut = json.dumps({"ErrorInfo": "文件记录失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        dict={}
        dict["code"] = 0

        lResut = json.dumps(dict)
        return HttpResponse(lResut)

    @staticmethod
    def getStoragePath():
        fileType = 0
        filePath = os.path.join(STATIC_ROOT,"GoodsImage")

        # 判断目录是否存在
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        return filePath

    @staticmethod
    def goGoodsSetting(request):
        dict = {}
        LoggerHandle.writeLogDevelope("订单管理", request)

        return render(request, os.path.join(STATIC_TMP,'OrgHome/Device/set_goods.html'), dict)
