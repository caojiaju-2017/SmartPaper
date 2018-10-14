#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading,datetime,md5,os

class CommitData(object):
    def __init__(self,dbhandle,type):
        self.dbHandle = dbhandle
        self.operatorType = type  # save  dele