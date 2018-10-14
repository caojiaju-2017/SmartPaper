#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import httplib
import urllib
import datetime
import threading
import md5
import random
import os
import inspect
import hashlib
import base64
import pickle
import socket
import sys
import platform
import time
import json
import uuid
import re
import et
import qrcode
import urllib2
import requests
import shutil
import zipfile
from django.template import Template, Context
from SmartPaperServer.settings import *

# DJANGO 引用
from django.shortcuts import render,render_to_response
from django.http import  HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.template import Template, Context
from django.http import StreamingHttpResponse

from SmartPaper.models import *
from SmartPaper.Api.PublicService import *

import logging
import json,uuid,time,base64,re,urllib
from django.shortcuts import render,render_to_response
from django.http import  HttpResponse,HttpResponseRedirect

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import qrcode,urllib2,requests
from django.db.models import F
from django.db.models import Q
from SmartPaper.models import *
import xml.etree.ElementTree as ET
from ctypes import *
import base64


from SmartPaper.BaseMoudle.Logger import *
