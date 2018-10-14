#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin

class OrgPageRoute(object):
    @staticmethod
    @xframe_options_exempt
    def goHelpX(request):
        dict = {}
        LoggerHandle.writeLogDevelope("打开帮助主页", request)
        return render(request, 'OrgHome/home.html', dict)

