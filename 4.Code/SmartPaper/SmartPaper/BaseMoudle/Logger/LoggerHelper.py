#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,os,socket,time,logging
from SmartPaper.BaseMoudle.Util.UtilHelper import *

class LoggerHelper(object):
    ENGINESUPPORT = ['NET','DB','FILE']
    def __init__(self):
        self.level = None
        self.logEngine = []
        self.netCfg = None
        self.fileCfg = None
        self.dbCfg = None
        self.workdir = None

    @staticmethod
    def loadLoggerSetting(workdir):
        loggerHandle = LoggerHelper()
        loggerHandle.workdir = workdir

        # 读取配置文件
        cf = ConfigParser.ConfigParser()

        print("===5555=====>" + workdir)

        configFile = os.path.join(workdir, "config.ini")
        cf.read(configFile)

        logCfgDetails = cf.items('logconfig')

        # 基础信息
        for oneItem in logCfgDetails:
            if oneItem[0].upper() == "LEVEL":
                loggerHandle.level = oneItem[1]
                continue
            if oneItem[0].upper() == "ENGINE":
                loggerHandle.logEngine = oneItem[1].upper().split(',')
                continue

        # 网络日志
        netCfgDetails = cf.items('netlog')
        loggerHandle.netCfg = NetCfg.initCfg(netCfgDetails)

        # 数据库日志
        dbCfgDetails = cf.items('dblog')
        loggerHandle.dbCfg = DbLog.initCfg(netCfgDetails)

        # 文件日志
        fileCfgDetails = cf.items('filelog')
        loggerHandle.fileCfg = FileLog.initCfg(netCfgDetails)

        return  loggerHandle

    def startLogEvent(self):
        pass

    def getCmdAlias(self,cmd):
        from SmartPaperServer.settings import *

        if SYSTEM_CMDS.has_key(cmd.upper()):
            return SYSTEM_CMDS[cmd.upper()]
        return "未知指令".decode("utf-8")
    def writeLog(self , cmd ,request):
        # 命令行输出
        # consoleLogger.info("" + msg)
        if cmd.upper() == "QUERY_ADS":
            return

        # 记录到数据库
        from SmartPaper.models import *
        logDb = PaperRunlog()
        logDb.code = UtilHelper.newUuid()
        logDb.content = self.getCmdAlias(cmd)

        try:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                logDb.ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                logDb.ip = request.META['REMOTE_ADDR']
        except:
            pass

        logDb.logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logDb.operttype = UtilHelper.getCommand(request)  # 此处在SAAS模式下会有问题， 暂时这样
        try:
            logDb.orgcode = PaperOrgs.objects.filter(code = UtilHelper.getOrgCode(request)).first()
        except:
            logDb.orgcode = None
            pass

        try:
            logDb.ucode = PaperAccount.objects.filter(workno = request.COOKIES["OrgUserCode"]).first()

            if not logDb.ucode:
                logDb.uaccount = "Unknown"
                logDb.uname = "Unknown"
            else:
                logDb.uname = logDb.ucode.alias
                logDb.uaccount = logDb.ucode.workno
        except:
            pass

        try:
            logDb.save()
        except Exception,ex:
            pass

        pass

    def writeLogDevelope(self , msg,request):
        # 记录数据库日志
        # self.writeLog(msg,request)

        if "DEBUG" != self.level:
            return
        if "NET" not in self.logEngine:
            return

        msg = self.buildNetMsg(msg,request)

        # import threading
        # tmpThread = threading.Thread(target=self.netCfg.sendNetLog, args=(msg,))
        # tmpThread.setDaemon(True)
        # tmpThread.start()
        self.netCfg.sendNetLog(msg)
        pass
    def buildNetMsg(self,msg,request):
        # msg长度（不足10位，不足十位） 线程名称 | | TAG | | msg | | 时间

        msgFormat = "%s||%s||%s||%s" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'Server','博源广告系统',msg )
        return  msgFormat
class NetCfg(object):
    def __init__(self):
        self.host = None
        self.port = None
        self.comSocket = None

    @staticmethod
    def initCfg(datas):
        netCfg = NetCfg()
        # 基础信息
        for oneItem in datas:
            if oneItem[0].upper() == "HOST":
                netCfg.host = oneItem[1]
                continue
            if oneItem[0].upper() == "PORT":
                netCfg.port = int(oneItem[1])
                continue
        return netCfg

    def sendNetLog(self,msg):
        try:
            # if not self.comSocket:
            self.comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
            self.comSocket.connect((self.host, self.port))  # 要连接的IP与端口
            length = len(msg.decode('utf-8'))
            sendMsg = "%010d%s"%(length,msg)
            self.comSocket.send(sendMsg)  # 把命令发送给对端
        except Exception,ex:
            pass

        self.comSocket.close()  # 关闭连接

class DbLog(object):
    def __init__(self):
        self.keepdays = 0

    @staticmethod
    def initCfg(datas):
        dbCfg = DbLog()
        for oneItem in datas:
            if oneItem[0].upper() == "KEEPDAYS":
                dbCfg.keepdays = int(oneItem[1].toLower())
                continue

        return dbCfg

class FileLog(object):
    def __init__(self):
        self.maxSize = 5
        self.logFileFormat = None

    @staticmethod
    def initCfg(datas):
        fileCfg = FileLog()
        for oneItem in datas:
            if oneItem[0].upper() == "MAXSIZE":
                fileCfg.maxSize = int(oneItem[1].toLower())
                continue
            if oneItem[0].upper() == "LOGFILEFORMAT":
                fileCfg.logFileFormat = oneItem[1]
                continue

        return fileCfg


class LogLevel(object):
    DEBUG="DEBUG"
    RELEASE="RELEASE"