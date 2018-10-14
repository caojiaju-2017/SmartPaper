#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

class PowerHelper(object):
    @staticmethod
    def openPort(power,port):
        if not power:
            return  False,"电源异常"

        if port > power.ctrlportnumber or port < 1:
            return  False,"指定的端口数据不正确"

        # 执行关闭动作
        portString = ""
        for index in range(port):
            if index + 1 == port:
                portString = portString  + "1"
            else:
                portString = portString + "9"

            if index + 1 >= port :
                break
        portString = portString + "9"
        commandUrl = "http://%s:%d/powerControl?ports=%s" % (power.ipaddress,power.port, portString)
        r = requests.get(commandUrl)

        resultRet = r.content

        if resultRet == "Success":
            # 更新电源状态
            try:
                statesValue = power.portstates
                statesValue = str(statesValue)
                statesValue = "%s1%s" % (statesValue[:port - 1], statesValue[port:])
                power.portstates = statesValue
                power.save()
            except Exception ,ex:
                pass
            return True,r.content
        else:
            return False,"电源返回操作异常，请检查串口连接是否正常"

    @staticmethod
    def closePort(power,port):
        if not power:
            return  False,"电源异常"

        if port > power.ctrlportnumber or port < 1:
            return  False,"指定的端口数据不正确"

        # 执行关闭动作
        portString = ""
        for index in range(port):
            if index + 1 == port:
                portString = portString + "0"
            else:
                portString = portString + "9"

            if index + 1 >= port:
                break

        portString = portString + "9"
        commandUrl = "http://%s:%d/powerControl?ports=%s" % (power.ipaddress, power.port, portString)

        r = requests.get(commandUrl)
        resultRet = r.content
        if resultRet == "Success":
            try:
                statesValue = power.portstates
                statesValue = str(statesValue)
                statesValue = "%s0%s" % (statesValue[:port - 1], statesValue[port:])
                power.portstates = statesValue
                power.save()
            except Exception,ex:
                pass
            return True,r.content
        else:
            return False,"电源返回操作异常，请检查串口连接是否正常"