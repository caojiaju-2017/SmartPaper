#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from include import *
import uuid,json
from SmartPaper.models import *
class OrgTree(object):
    def __init__(self,code,name):
        self.name = name
        self.id = code
        self.children=[]


    @staticmethod
    def newTestObj():
        rtnObj = OrgTree()
        rtnObj.name = "caojiaju"
        rtnObj.id = uuid.uuid1().__str__().replace("-", "")
        rtnObj.children = []
        return rtnObj
    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    @staticmethod
    def getOrgLists(org):
        rtnList = []
        rtnList.append(org)

        rtnList = rtnList +  OrgTree.getOrgTreeObjects(org)
        return  rtnList
    @staticmethod
    def getOrgTreeObjects(org):
        rtnList = []
        if not org:
            return None

        childrens = org.children.all()
        for index in range(len(childrens)):
            child = childrens[index]

            if child and child.state == 1:
                rtnList.append(child)

                rtnList = rtnList + OrgTree.getOrgTreeObjects(child)


        return rtnList

    @staticmethod
    def getUserOrg(logincode):
        # 查询账户信息
        accountHandle = PaperAccount.objects.filter(account=logincode,state=1).first()

        # 如果账户不存在，则验证工号
        if not accountHandle :
            accountHandle = PaperAccount.objects.filter(workno=logincode, state=1).first()

        if not accountHandle:
            return None,None
        return accountHandle.orgcode,accountHandle

    @staticmethod
    def getManageUse(orgsign):
        orgAdminAccount = SmartAccount.objects.filter(orgcode_id=orgsign,type = 1).first()

        return  orgAdminAccount

    @staticmethod
    def getRootOrg(orgHandle):
        if not orgHandle:
            return None

        while orgHandle.parentcode and orgHandle.parentcode != orgHandle:
            orgHandle = orgHandle.parentcode

        return orgHandle

    @staticmethod
    def getRootOrgByCode(orgCode):
        myOrg = PaperOrgs.objects.filter(code = orgCode,state=1).first()
        return OrgTree.getRootOrg(myOrg)


    @staticmethod
    def isSubOrg(currentOrg, parentOrg):
        # 如果两单位相同，则认为包含
        if currentOrg.code == parentOrg.code:
            return True

        # 遍历待检查的单位的所有上级单位
        while currentOrg and currentOrg.parentcode != None and currentOrg.parentcode != currentOrg:
            if currentOrg.code == parentOrg.code:
                return True
            currentOrg = currentOrg.parentcode


        if currentOrg.code == parentOrg.code:
            return True
        return  False

    @staticmethod
    def checkTerminalsWasInclude(currentOrg, rangesTemp):
        # 初始检查
        for oneRange in rangesTemp:
            if oneRange.scode == currentOrg.code:
                return True

        # 遍历待检查的单位的所有上级单位
        while currentOrg and currentOrg.parentcode != None and currentOrg.parentcode != currentOrg:
            currentOrg = currentOrg.parentcode

            for oneRange in rangesTemp:
                if oneRange.scode == currentOrg.code:
                    return True

        return  False

    @staticmethod
    def getParentOrgLists(currentOrg):
        '''
        获取当前单位所有上级单位
        :param currentOrg:
        :return:
        '''
        rtnList = []
        rtnList.append(currentOrg)

        while currentOrg and currentOrg.parentcode != None and currentOrg.parentcode != currentOrg:
            currentOrg = currentOrg.parentcode
            rtnList.append(currentOrg)

        return  rtnList


if __name__ == "__main__":
    obj1 = OrgTree.newTestObj()
    obj2 = OrgTree.newTestObj()
    obj1.children.append(obj2)
    print json.dumps(obj1,default=lambda  o :o.__dict__,sort_keys=True,indent=4)

