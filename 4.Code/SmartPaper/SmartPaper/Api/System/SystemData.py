#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from include import *
import uuid,json
class SystemData(object):
    def __init__(self):
        self.name = None
        self.id = None

    @staticmethod
    def newTestObj():
        rtnObj = SystemData()
        rtnObj.name = "caojiaju"
        rtnObj.id = uuid.uuid1().__str__().replace("-", "")
        return rtnObj
    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

if __name__ == "__main__":
    obj1 = SystemData.newTestObj()
    obj2 = SystemData.newTestObj()
    print json.dumps(obj1,default=lambda  o :o.__dict__,sort_keys=True,indent=4)

