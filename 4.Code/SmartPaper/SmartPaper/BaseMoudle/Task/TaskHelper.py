#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *
from apscheduler.schedulers.background import BackgroundScheduler
from SmartPaper.Api.Privilege.OrgTree import *
from SmartPaper.BaseMoudle.Device.DeviceHelper import *
# import logging
logging.basicConfig()
# 视频转码 、ftp资源上传
# 应用范围：  LED节目推送 、 数据库备份、LED在线状态监测、中行挂牌数据
class TaskHelper(object):
    taskScheduler = None
    powerStateJob = None
    timeScheduleJob = None
    @staticmethod
    def startTask():
        TaskHelper.taskScheduler = BackgroundScheduler()

        # 后台ftp广告发布
        # TaskHelper.powerStateJob = TaskHelper.taskScheduler.add_job(TaskHelper.startPowerStateCheck, 'interval', minutes=1, id='check_power_state')

        # TaskHelper.timeScheduleJob = TaskHelper.taskScheduler.add_job(TaskHelper.startScheduleCheck, 'interval', minutes=1, id='power_schedule')

        TaskHelper.taskScheduler.start()
        pass

    @staticmethod
    def startPowerStateCheck():
        # 查询当期广告数据 ---- saas模式会有问题
        TaskHelper.powerStateJob.pause()


        TaskHelper.powerStateJob.resume()
