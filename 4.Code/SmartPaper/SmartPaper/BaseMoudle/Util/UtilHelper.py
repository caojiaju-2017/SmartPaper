#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid,os,datetime
import ftplib,platform

# import Image
class UtilHelper(object):
    @staticmethod
    def newUuid():
        '''
        新建UUID
        :return:
        '''
        return  uuid.uuid1().__str__().replace("-", "")
    @staticmethod
    def GetFileNameAndExt(filename):
        (filepath, tempfilename) = os.path.split(filename);
        (shotname, extension) = os.path.splitext(tempfilename);
        return shotname, extension
    @staticmethod
    def getGetParams(request):
        getParams = {}
        for oneParam in request.GET:
            # print "paramname=%s,paramvalue=%s"%(oneParam,request.GET.get(oneParam))
            getParams[oneParam.lower()] = request.GET.get(oneParam)
        return getParams
    @staticmethod
    def getPostParams(request):
        '''
        获取请求post参数
        :return:
        '''
        postDataList = {}
        if request.method == 'POST':
            for key in request.POST:
                try:
                    postDataList[key.lower()] = request.POST.getlist(key)[0]
                except:
                    pass

        import json
        if not postDataList or len(postDataList) == 0:
            try:
                bodyTxt = request.body
                postDataList = json.loads(bodyTxt)
            except Exception,ex:
                pass

        return  postDataList

    @staticmethod
    def getCommand(request):
        try:
            command = request.GET.get('command').upper()
            return command
        except:
            return None

    @staticmethod
    def getOrgCode(request):
        try:
            getParams = UtilHelper.getGetParams(request)
            if getParams.has_key("orgsign"):
                return getParams['orgsign']

            postParams = UtilHelper.getPostParams(request)
            if postParams.has_key("orgsign"):
                return postParams['orgsign']
        except:
            postParams = UtilHelper.getPostParams(request)
            if postParams.has_key("orgsign"):
                return postParams['orgsign']
            return None


    @staticmethod
    def getUserCode(request):
        try:
            ucode = request.GET.get('logincode').upper()
            return ucode
        except:
            return None

    @staticmethod
    def getMd5(stringValue):
        import md5
        m1 = md5.new()

        try:
            m1.update(stringValue.encode(encoding='utf-8'))
        except:
            m1.update(stringValue)
        return m1.hexdigest()

    @staticmethod
    def ftp_upload(host,port,username,password,filename,shortname,remotepath):
        ftp = ftplib.FTP()  # 实例化FTP对象
        ftp.connect(host,port=port)
        ftp.login(username, password)  # 登录

        # 获取当前路径
        print remotepath
        ftp.cwd(remotepath)

        '''以二进制形式上传文件'''
        file_remote = shortname
        file_local = filename
        bufsize = 1024  # 设置缓冲器大小
        fp = open(file_local, 'rb')
        ftp.storbinary('STOR ' + file_remote, fp, bufsize)
        fp.close()

    @staticmethod
    def getFtpUpload(confs):
        rtnList = []
        ftpHost = None
        ftpPort = None
        ftpUploadUser = None
        ftpUploadPassword = None
        ftpStoragePath = None
        for oneCfg in confs:
            if oneCfg.keyname == "FtpHost":
                ftpHost = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpPort":
                ftpPort = int(oneCfg.keyvalue)
            elif oneCfg.keyname == "FtpUUser":
                ftpUploadUser = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpUPassword":
                ftpUploadPassword = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpRoot":
                ftpStoragePath = oneCfg.keyvalue

        rtnList.append(ftpHost)
        rtnList.append(ftpPort)
        rtnList.append(ftpUploadUser)
        rtnList.append(ftpUploadPassword)
        rtnList.append(ftpStoragePath)
        return rtnList

    @staticmethod
    def getFtpDownload(confs):
        rtnDictFtpInfo = {}
        ftpHost = None
        ftpPort = None
        ftpDownloadUser = None
        ftpDownloadPassword = None
        ftpStoragePath = None
        for oneCfg in confs:
            if oneCfg.keyname == "FtpHost":
                ftpHost = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpPort":
                ftpPort = int(oneCfg.keyvalue)
            elif oneCfg.keyname == "FtpDUser":
                ftpDownloadUser = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpDPassword":
                ftpDownloadPassword = oneCfg.keyvalue
            elif oneCfg.keyname == "FtpRoot":
                ftpStoragePath = oneCfg.keyvalue

        # rtnList.append(ftpHost)
        # rtnList.append(ftpPort)
        # rtnList.append(ftpDownloadUser)
        # rtnList.append(ftpDownloadPassword)
        # rtnList.append(ftpStoragePath)

        rtnDictFtpInfo['host'] = ftpHost
        rtnDictFtpInfo['port'] = ftpPort
        rtnDictFtpInfo['user'] = ftpDownloadUser
        rtnDictFtpInfo['password'] = ftpDownloadPassword
        rtnDictFtpInfo['rootpath'] = ftpStoragePath

        return rtnDictFtpInfo
    # @staticmethod
    # def make_thumb(path, thumb_file, size):
    #     """生成缩略图"""
    #     img = Image.open(path)
    #     width, height = img.size
    #     # 裁剪图片成正方形
    #     if width > height:
    #         delta = (width - height) / 2
    #         box = (delta, 0, width - delta, height)
    #         region = img.crop(box)
    #     elif height > width:
    #         delta = (height - width) / 2
    #         box = (0, delta, width, height - delta)
    #         region = img.crop(box)
    #     else:
    #         region = img
    #
    #         # 缩放
    #     thumb = region.resize((size, size), Image.ANTIALIAS)
    #
    #     base, ext = os.path.splitext(os.path.basename(path))
    #     # filename = os.path.join(thumb_path, '%s_thumb.jpg' % (base,))
    #     # print filename
    #     # 保存
    #     thumb.save(thumb_file, quality=70)
    @staticmethod
    def getFtpInfo(orgcode):
        from SmartPaper.models import *
        from SmartPaper.Api.Privilege.OrgTree import *
        # 获取单位请单，只包含上级单位
        currentOrgHandle = SmartOrganization.objects.filter(code = orgcode).first()
        parentOrgs = OrgTree.getParentOrgLists(currentOrgHandle)

        # 获取单位绑定的播放盒，并查找播放盒ftp配置
        bindPlayBox = None
        # ....

        # 没有播放盒，则获取机构归属的根机构ftp配置信息
        ftpInfo = {}
        if not bindPlayBox:
            rootOrg  = OrgTree.getRootOrg(currentOrgHandle)
            confs = ByAdConfig.objects.filter(orgcode = rootOrg)

            ftpInfo = UtilHelper.getFtpDownload(confs)
        else:
            pass

        return  ftpInfo

    @staticmethod
    def UsePlatform():
      sysstr = platform.system()
      if(sysstr =="Windows"):
        return  0
      elif(sysstr == "Linux"):
        return 1
      else:
        return 2

    @staticmethod
    def checkTimeDistance(strTime, type):
        '''

        :param strTime:
        :param type:0 表示返回秒   1 表示返回分钟
        :return:
        '''
        try:
            dInput1 = datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()

            delta = now - dInput1

            if type == 0:
                return delta.seconds
            elif type == 1:
                return delta.seconds / 60
        except:
            pass
if __name__ == "__main__":
    print UtilHelper.checkTimeDistance("",0)