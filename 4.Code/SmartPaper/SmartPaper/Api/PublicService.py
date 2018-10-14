#!/usr/bin/env python
# -*- coding: utf-8 -*-
from include import *

SignKey = 'Sign'
def checkSign(request):
    global SignKey
    '''
    检查签名是否合法
    :param dicts:  参数字典
    :param signString: 请求者传递的签名信息
    :return:True 签名正确   False  签名不正确
    '''

    # 获取Post参数
    postDict=getPostData(request)

    # 获取Get参数
    getDict = getGetParamData(request)

    # 合并参数
    dictMerged = dict(postDict, **getDict)

    # 剔除签名键值
    if not dictMerged.has_key(SignKey):
        return False
    sign =dictMerged[SignKey]
    del dictMerged[SignKey]

    # 开始签名
    sortDicts = sorted(dictMerged.iteritems(),key=lambda  asd:asd[0])
    signStr = ""
    for oneParam in sortDicts:
        signStr = signStr + "%s=%s"%(oneParam[0],oneParam[1])

    signStr = signStr + HsShareData.SigCode

    md5M = md5.new()
    md5M.update(signStr)
    signData =md5M.hexdigest()

    if signData == sign:
        return True

    return True

def isLogin(request):
    '''
    检查请求中是否包含账号信息
    :param request:
    :return:
    '''
    return True

def getPostData(request):
    '''
    获取post参数
    :param request:
    :return:
    '''
    postDataList = {}
    dataListTemp = {}
    if request.method == 'POST':
        for key in request.POST:
            postDataList[key] = request.POST.getlist(key)[0]

    import json
    if not postDataList or len(postDataList) == 0:
        try:
            bodyTxt = request.body
            dataListTemp = json.loads(bodyTxt)
        except Exception,ex:
            pass

    for onePairKey in dataListTemp.keys():
        postDataList[onePairKey.lower()] = dataListTemp[onePairKey]
    return  postDataList

def getGetParamData(request):
    '''
    提取请求Get参数
    :param request:
    :return:
    '''
    urlFullPath = request.get_full_path()
    values = urlFullPath.split('?')[-1]

    getParamsDataList={}
    for key_value in values.split('&'):
        onePairs = key_value.split('=')

        if len(onePairs) != 2:
            continue
        getParamsDataList[onePairs[0].lower()] = onePairs[1]
    return  getParamsDataList

# def commitCustomDataByTranslate(objHandles):
#     '''
#     提交数据修改-事务
#     :param objHandles:
#     :return:
#     '''
#     with transaction.atomic():
#         for oneObject in objHandles:
#             if not oneObject.dbHandle:
#                 continue
#
#             try:
#                 if oneObject.operatorType == 0:
#                     oneObject.dbHandle.save()
#                 elif oneObject.operatorType == 1:
#                     oneObject.dbHandle.delete()
#             except Exception,ex:
#                 return  False
#
#     return True

def getName(type, ltype):
    '''
    :param type: 名字类别 0 表示年级 1 表示年级 2 表示科目
    :param ltype:type=0:1表示高中 2 表示初中 3 表示小学；type=1：1初年级，2中年级，3高年级 ；type=2:1语文 2数学 3英语 4其他
    :return:
    '''
    ltype = int(ltype)
    if type == 0:
        if ltype == 1:
            return "高中"
        elif ltype == 2:
            return "初中"
        elif ltype == 3:
            return "小学"
        elif ltype == 4:
            return "幼教"            
    elif type == 1:
        if ltype == 1:
            return "一年级"
        elif ltype == 2:
            return "二年级"
        elif ltype == 3:
            return "三年级"
        elif ltype == 4:
            return "四年级"
        elif ltype == 5:
            return "五年级"
        elif ltype == 6:
            return "六年级"
        elif ltype == 7:
            return "七年级"
        elif ltype == 8:
            return "八年级"
        elif ltype == 9:
            return "九年级"
        elif ltype == 10:
            return "高一"
        elif ltype == 11:
            return "高二"
        elif ltype == 12:
            return "高三"
    elif type == 2:
        if ltype == 1:
            return "语文"
        elif ltype == 2:
            return "数学"
        elif ltype == 3:
            return "英语"
        elif ltype == 4:
            return "物理"
        elif ltype == 5:
            return "化学"
        elif ltype == 6:
            return "历史"
        elif ltype == 7:
            return "地理"
        elif ltype == 8:
            return "生物"        
        elif ltype == 9:
            return "其它"                                                                      
    else:
        return "其他"
    pass

def getNameId(type, name):
    '''
    :param type: 名字类别 0 表示年级 1 表示年级 2 表示科目
    :param ltype:type=0:1表示高中 2 表示初中 3 表示小学；type=1：1初年级，2中年级，3高年级 ；type=2:1语文 2数学 3英语 4其他
    :return:
    '''
    name = name.encode('utf-8')
    if type == 0:
        if name == "高中":
            return 1
        elif name == "初中":
            return 2
        elif name == "小学":
            return 3
        elif name == "幼教":
            return 4
    elif type == 1:
        if name == "一年级":
            return 1
        elif name == "二年级":
            return 2
        elif name == "三年级":
            return 3
        elif name == "四年级":
            return 4
        elif name == "五年级":
            return 5
        elif name == "六年级":
            return 6
        elif name == "其它":
            return 7

    elif type == 2:
        if name == "语文":
            return 1
        elif name == "数学":
            return 2
        elif name == "英语":
            return 3
        elif name == "物理":
            return 4
        elif name == "化学":
            return 5
        elif name == "历史":
            return 6
        elif name == "地理":
            return 7
        elif name == "生物":
            return 8
        elif name == "其他":
            return 9                                                                        
    else:
        return -1

    return -1

def queryResource(subjectid,filterS):
    resDatas =  HsResources.objects.all().order_by('-code')
    rtnDatas = []
    for oneData in resDatas:
        # if gradeid != -1 and int(oneData.resgrade) != gradeid:
        #     continue
        # elif gclassid != -1 and int(oneData.reslevel) != gclassid:
        #     continue
        if subjectid != -1 and int(oneData.resclass) != subjectid:
            continue

        if filterS and len(filterS) > 0:
            if  (filterS in oneData.restitle) or (filterS in oneData.resinfo) :
                rtnDatas.append(oneData)
            else:
                continue
        else:
            rtnDatas.append(oneData)

    return rtnDatas

def getRadomName(size):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
    sa = []
    for i in range(size):
        sa.append(random.choice(seed))
    salt = ''.join(sa)