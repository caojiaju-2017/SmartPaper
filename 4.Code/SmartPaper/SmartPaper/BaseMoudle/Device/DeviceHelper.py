#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

from SmartPaper.BaseMoudle.Device.PowerHelper import *

class DeviceHelper(object):
    @staticmethod
    def DevicePowerOff(dev):
        if not dev:
            return False,"设备对象异常"

        #
        powerMap = SmartPowerPortMap.objects.filter(devcode=dev).first()
        if not powerMap:
            return  False , "设备未关联电源"

        if not powerMap.powercode or powerMap.powercode.state != 1:
            return  False, "设备关联电源异常或被删除"

        return PowerHelper.closePort(powerMap.powercode, powerMap.port)
    @staticmethod
    def DevicePowerOn(dev):
        if not dev:
            return False,"设备对象异常"

        #
        powerMap = SmartPowerPortMap.objects.filter(devcode=dev).first()
        if not powerMap:
            return  False , "设备未关联电源"

        if not powerMap.powercode or powerMap.powercode.state != 1:
            return  False, "设备关联电源异常或被删除"

        return PowerHelper.openPort(powerMap.powercode, powerMap.port)

    @staticmethod
    def DeviceShutdown(dev):
        pass

    @staticmethod
    def DeviceRestart(dev):
        pass