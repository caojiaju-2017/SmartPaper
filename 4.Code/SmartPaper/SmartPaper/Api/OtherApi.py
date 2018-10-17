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


appID = "wx75e53a9db8f89fce"
appsecret = "c45eefc37a8a0889fa4ebe020a9eb696"
api_key="e23458c671bd7d2b5dd9919f7a700a61"
access_token = None
ticket = None
mch_id = "1495716512"
nonce_str = "fsdfds"
notify_url="http://www.h-sen.com/paySuccess.html"

class OtherApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        LoggerHandle.writeLog(command, req)

        if command == "GOODS_ADD".upper():
            return OtherApi.GoodsAdd(req,command)
        elif command == "GOODS_LIST".upper():
            return OtherApi.GoodsList(req,command)

    @staticmethod
    @csrf_exempt
    def openWaitPage(request):
        hidden = 0
        try:
            hidden = int(request.GET.get('hidden'))
        except:
            hidden = 0
        renterDict = {}
        renterDict["hidden"] = hidden
        return render(request, 'wait.html', renterDict)

    @staticmethod
    @csrf_exempt
    def applyFreePaper(request):
        devCode = None
        try:
            devCode = request.GET.get('code')
        except:
            devCode = None

        devHandle = PaperDevices.objects.filter(code=devCode).first()
        applyHis = None
        if devHandle:
            applyHis = PaperApplyFreePaper.objects.filter(devcode = devHandle).first()

        # 如果存在申请记录
        if applyHis:
            # 判断是否超过1分钟
            oldTime = datetime.datetime.strptime(applyHis.applytime, '%Y-%m-%d %H:%M:%S')
            nowTime = datetime.datetime.now()

            if (nowTime - oldTime).seconds < 30:
                renterDict = {}
                renterDict["imagelab"] = "/static/images/failed.png"
                renterDict["info"] = "请求频繁，请稍后重试!"
                return render(request, 'get_free_paper.html', renterDict)
            else:
                pass

        if not applyHis:
            applyHis = PaperApplyFreePaper()
            applyHis.state = 0
            applyHis.devcode = devHandle
            applyHis.devmac = devHandle.mac
            applyHis.applytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            applyHis.state = 0
            applyHis.applytime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            applyHis.save()
        except Exception as ex:
            renterDict = {}
            renterDict["imagelab"] = "/static/images/faild.png"
            renterDict["info"] = "系统内部错误!"
            return render(request, 'get_free_paper.html', renterDict)

        renterDict = {}
        renterDict["imagelab"] = "/static/images/ok.png"
        renterDict["info"] = "请求成功，请稍后!"
        return render(request, 'get_free_paper.html', renterDict)


    @staticmethod
    @csrf_exempt
    def openShop(request):
        dict = {}

        # ===============测试代码==============================
        # 返回一些数据
        resArray = []
        allMaps = PaperGoods.objects.all()
        # resDatas = HsResources.objects.all().order_by('-code')[:10]
        ermaUrl = "http://" + request.META['HTTP_HOST']
        for oneRes in allMaps:
            resDict = {}
            resDict['goodscode'] =  "42c9625ed11611e882dd989096c1d848" #商品代码
            resDict['goodscount'] = 3
            resDict['trackindex'] = 1  # 轨道编号
            resDict['goodsname'] = oneRes.name
            resDict['goodsprice'] = oneRes.price
            resDict['goodsimage'] = "%s/static/GoodsImage/%s.jpg"% (ermaUrl,"42c9625ed11611e882dd989096c1d848")

            resArray.append(resDict)

        dict['Resource_Datas'] = resArray
        # ===============测试代码-end==========================
        try:
            code = request.GET.get('code')
            # 设备代码
            state = request.GET.get('state')
        except Exception, e:
            # print u"获取code和stat参数错误"
            return render(request, 'shop.html', dict)

        dict["code"] = code
        dict["state"] = state

        # 获取token
        # https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
        try:
            url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
            params = {
                'appid': appID,
                'secret': appsecret,
                'code': code,
                'grant_type': 'authorization_code'
            }
            res = requests.get(url, params=params).json()

            access_token = res["access_token"]  # 只是呈现给大家看,可以删除这行
            openid = res["openid"]  # 只是呈现给大家看,可以删除这行

            dict["access_token"] = access_token
            dict["openid"] = openid
        except Exception, e:
            # print u"获取access_token参数错误"
            return render(request, 'shop.html', dict)

        a = 1
        wxInfo = {}
        # 4.拉取用户信息
        #  //http：GET（请使用https协议） https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        try:
            user_info_url = u'https://api.weixin.qq.com/sns/userinfo'
            params = {
                'access_token': access_token,
                'openid': openid,
            }
            res = requests.get(user_info_url, params=params).json()
            print res
            nameUser = res['nickname'].encode('iso8859-1').decode('utf-8')
            openid = openid.encode('utf-8')
            nameUser = nameUser.encode('utf-8')
            imgUrl = res['headimgurl'].encode('utf-8')

            wxInfo["OpenId"] = openid
            wxInfo["WxName"] = nameUser
            wxInfo["HeadImg"] = imgUrl

            # 添加到客户表
            existCustomHandle = PaperWxCustom.objects.filter(wxaccount=openid).first()
            if not existCustomHandle:
                newCustom = PaperWxCustom()
                newCustom.wxaccount = openid
                newCustom.name = nameUser
                newCustom.headimage = imgUrl
            else:
                newCustom = existCustomHandle
                newCustom.name = nameUser
                newCustom.headimage = imgUrl

            newCustom.save()
        except Exception, e:
            return render(request, 'shop.html', dict)

        # 返回一些数据
        resArray = []
        devHandle = PaperDevices.objects.filter(code=state).first()
        allMaps = PaperDevGoodsMap.objects.filter(dcode=devHandle)
        # resDatas = HsResources.objects.all().order_by('-code')[:10]
        ermaUrl = "http://" + request.META['HTTP_HOST']
        for oneRes in allMaps:
            resDict = {}
            resDict['goodscode'] =  oneRes.gcode.code #商品代码
            resDict['goodscount'] = oneRes.count
            resDict['trackindex'] = oneRes.trackindex  # 轨道编号
            resDict['goodsname'] = oneRes.gcode.name
            resDict['goodsprice'] = oneRes.gcode.price
            resDict['goodsimage'] = "%s/static/GoodsImage/%s.jpg"% oneRes.gcode.code

            resArray.append(resDict)

        dict['wxInfo'] = json.dumps(wxInfo)
        dict['Resource_Datas'] = resArray
        return render(request, 'shop.html', dict)
