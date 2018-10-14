#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import transaction
import os
import ConfigParser

class DBHelper(object):
    @staticmethod
    def getDbConfig():
        # 读取配置文件
        cf = ConfigParser.ConfigParser()
        configFile = os.path.join(os.getcwd(), "config.ini")
        cf.read(configFile)

        dbCfgDetails = cf.items('dbconfig')
        DATABASES = {}

        # 构建字典
        dbCfg = {}
        for oneItem in dbCfgDetails:
            dbCfg[oneItem[0]] = oneItem[1]

        DATABASES['default'] = dbCfg

        return  DATABASES

    # 事务提交变更
    @staticmethod
    def commitCustomDataByTranslate(objHandles):
        with transaction.atomic():
            for oneObject in objHandles:
                if  not oneObject  or  not oneObject.dbHandle:
                    continue
                try:
                    if oneObject.operatorType == 0:
                        oneObject.dbHandle.save()
                    elif oneObject.operatorType == 1:
                        oneObject.dbHandle.delete()
                except Exception,ex:
                    transaction.rollback()
                    return  False

        return True