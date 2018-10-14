# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# c:\Python27\python.exe manage.py inspectdb > SmartPaper/models.py
from __future__ import unicode_literals

from django.db import models


class SmartAccount(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=32)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=64, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('SmartOrganization', models.DO_NOTHING, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_account'


class ByAdAudit(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    channelcode = models.ForeignKey('ByAdChannel', models.DO_NOTHING, db_column='ChannelCode',to_field="code")  # Field name made lowercase.
    auditcode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='AuditCode',to_field="code")  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=200, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_audit'


class ByAdBoxPlayerMap(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    boxcode = models.ForeignKey('ByAdProxyTermianl', models.DO_NOTHING, db_column='BoxCode',to_field="code")  # Field name made lowercase.
    way = models.CharField(db_column='Way', max_length=20, blank=True, null=True)  # Field name made lowercase.
    playercode = models.ForeignKey('SmartDevices', models.DO_NOTHING, db_column='PlayerCode', blank=True, null=True,to_field="code")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_box_player_map'


class ByAdChannel(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    acode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='ACode',to_field="code")  # Field name made lowercase.
    programcode = models.ForeignKey('ByAdPrograms', models.DO_NOTHING, db_column='ProgramCode',to_field="code")  # Field name made lowercase.
    releasetime = models.CharField(db_column='ReleaseTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    scode = models.ForeignKey('BySchedules', models.DO_NOTHING, db_column='SCode',to_field="code")  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('SmartOrganization', models.DO_NOTHING, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    range = models.IntegerField(db_column='Range', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_channel'


class ByAdChannelRange(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ccode = models.ForeignKey(ByAdChannel, models.DO_NOTHING, db_column='CCode', to_field="code")  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    scode = models.CharField(db_column='SCode', max_length=32)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_channel_range'


class ByAdConfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=64, blank=True, null=True)  # Field name made lowercase.
    keyname = models.CharField(db_column='KeyName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    keyvalue = models.CharField(db_column='KeyValue', max_length=256, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('SmartOrganization', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,
                                to_field="code")  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_config'

class ByAdVersion(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regtime = models.CharField(db_column='RegTime', max_length=20, blank=True,null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('SmartOrganization', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,
                                to_field="code")  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_version'

class ByAdDesignerApply(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    orgcode = models.ForeignKey('SmartOrganization', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    servicecode = models.ForeignKey('ByAdPrograms', models.DO_NOTHING, db_column='ServiceCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    usercode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='UserCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    result = models.CharField(db_column='Result', max_length=200, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_designer_apply'


class ByAdFunctions(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    pcode = models.ForeignKey('self', models.DO_NOTHING, db_column='PCode',to_field="code")  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    funcid = models.IntegerField(db_column='FuncId', blank=True, null=True)  # Field name made lowercase.
    dopage = models.CharField(db_column='DoPage', max_length=128, blank=True, null=True)  # Field name made lowercase.
    freeflag = models.IntegerField(db_column='FreeFlag', blank=True, null=True)  # Field name made lowercase.
    cmd = models.CharField(db_column='Cmd', max_length=20, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_functions'


class ByAdMaterials(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    zcode = models.ForeignKey('ByAdProgZone', models.DO_NOTHING, db_column='ZCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    mcode = models.CharField(db_column='MCode', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_materials'


class SmartOrganization(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    contactphone = models.CharField(db_column='ContactPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    logo = models.CharField(db_column='Logo', max_length=64, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    signstr = models.CharField(db_column='SignStr', max_length=32, blank=True, null=True)  # Field name made lowercase.
    parentcode = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentCode', blank=True, null=True,to_field="code", related_name="children")  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    terminalcount = models.IntegerField(db_column='TerminalCount', blank=True, null=True)  # Field name made lowercase.
    storagesize = models.IntegerField(db_column='StorageSize', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_organization'


class ByAdPlayerControl(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    weekid = models.IntegerField(db_column='WeekId', blank=True, null=True)  # Field name made lowercase.
    opentime = models.CharField(db_column='OpenTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    closetime = models.CharField(db_column='CloseTime', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_player_control'


class ByAdPlayerGroup(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='Code', unique=True,to_field="code")  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_player_group'


class SmartDevicesign(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    signcode = models.CharField(db_column='SignCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_player_sign'


class SmartDevices(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gcode = models.ForeignKey(ByAdPlayerGroup, models.DO_NOTHING, db_column='GCode',to_field="code")  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IpAddress', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mac = models.CharField(db_column='Mac', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    online = models.IntegerField(db_column='Online', blank=True, null=True)  # Field name made lowercase.
    pcode = models.ForeignKey(ByAdPlayerControl, models.DO_NOTHING, db_column='PCode',to_field="code")  # Field name made lowercase.
    terminalsign = models.CharField(db_column='TerminalSign', max_length=32)  # Field name made lowercase.
    lastcmd = models.CharField(db_column='LastCmd', max_length=32)  # Field name made lowercase.
    lastcmdresult = models.IntegerField(db_column='LastCmdResult', blank=True, null=True)  # Field name made lowercase.
    # orgcode = models.ForeignKey(SmartOrganization, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    lastlogintime = models.CharField(db_column='LastLoginTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=36)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    ledtype = models.IntegerField(db_column='LedType', blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    heigth = models.IntegerField(db_column='Heigth', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_players'


class ByAdProgZone(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    pcode = models.ForeignKey('ByAdPrograms', models.DO_NOTHING, db_column='PCode',to_field="code")  # Field name made lowercase.
    startx = models.IntegerField(db_column='StartX', blank=True, null=True)  # Field name made lowercase.
    starty = models.IntegerField(db_column='StartY', blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.

    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    backcolor = models.CharField(db_column='BackColor', max_length=7, blank=True, null=True)  # Field name made lowercase.
    speed = models.IntegerField(db_column='Speed', blank=True, null=True)  # Field name made lowercase.
    switchtype = models.IntegerField(db_column='SwitchType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_prog_zone'


class ByAdPrograms(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    tmpcode = models.CharField(db_column='TmpCode',  max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    totalseconds = models.IntegerField(db_column='TotalSeconds', blank=True, null=True)  # Field name made lowercase.
    acode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='ACode',to_field="code")  # Field name made lowercase.
    lastdate = models.CharField(db_column='LastDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    backimage = models.CharField(db_column='BackImage', max_length=32, blank=True, null=True)  # Field name made lowercase.
    backsound = models.CharField(db_column='BackSound', max_length=32, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_programs'


class ByAdProxyTermianl(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mac = models.CharField(db_column='MAC', max_length=32, blank=True, null=True)  # Field name made lowercase.
    workport = models.IntegerField(db_column='WorkPort', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    way = models.IntegerField(db_column='Way', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_proxy_termianl'


class ByAdRoleFunc(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    rcode = models.ForeignKey('ByAdRoles', models.DO_NOTHING, db_column='RCode',to_field="code")  # Field name made lowercase.
    fcode = models.ForeignKey(ByAdFunctions, models.DO_NOTHING, db_column='FCode',to_field="code",related_name='relatefuncs')  # Field name made lowercase.
    flag = models.CharField(db_column='Flag', max_length=12)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_role_func'


class ByAdRoles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_roles'


class ByAdRunlog(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    operttype = models.CharField(db_column='OpertType', max_length=32, blank=True, null=True)
    content = models.CharField(db_column='Content', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ucode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='UCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    uaccount= models.CharField(db_column='UAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    uname = models.CharField(db_column='UName', max_length=64, blank=True,
                                null=True)  # Field name made lowercase.
    terminal = models.CharField(db_column='Device', max_length=32, blank=True, null=True)  # Field name made lowercase.
    logtime = models.CharField(db_column='LogTime', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_runlog'


class ByAdSpecial(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    isopen = models.IntegerField(db_column='IsOpen', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_special'

class ByAdMaterialMap(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    specialcode = models.ForeignKey(ByAdSpecial, models.DO_NOTHING, db_column='SpecialCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    materialcode = models.CharField(db_column='MaterialCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    type= models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_material_special_map'


class ByAdTemplate(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    acode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='ACode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    lastdate = models.CharField(db_column='LastDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_template'


class ByAdTemplateZone(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    mcode = models.ForeignKey(ByAdTemplate, models.DO_NOTHING, db_column='MCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    startx = models.IntegerField(db_column='StartX', blank=True, null=True)  # Field name made lowercase.
    starty = models.IntegerField(db_column='StartY', blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_template_zone'


class ByAdTextMaterails(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    zcode = models.ForeignKey(ByAdProgZone, models.DO_NOTHING, db_column='ZCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    fontsize = models.IntegerField(db_column='FontSize', blank=True, null=True)  # Field name made lowercase.
    forecolor = models.CharField(db_column='ForeColor', max_length=9, blank=True, null=True)  # Field name made lowercase.
    fontfamily = models.CharField(db_column='FontFamily', max_length=32, blank=True, null=True)  # Field name made lowercase.
    speed = models.IntegerField(db_column='Speed', blank=True, null=True)  # Field name made lowercase.
    backcolor = models.CharField(db_column='BackColor', max_length=18, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_text_materails'


class ByAdUserRole(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    rcode = models.ForeignKey(ByAdRoles, models.DO_NOTHING, db_column='RCode',to_field="code")  # Field name made lowercase.
    acode = models.ForeignKey(SmartAccount, models.DO_NOTHING, db_column='ACode',to_field="code")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_ad_user_role'


class ByProgType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_prog_type'



class BySchedules(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode',to_field="code")  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    regtime = models.CharField(db_column='RegTime', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_schedules'

class ByScheduleDetailPre(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    scode = models.ForeignKey('BySchedules', on_delete=models.CASCADE,db_column='SCode',to_field="code")  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=20)  # Field name made lowercase.
    nomon = models.CharField(db_column='NOMon', max_length=20)  # Field name made lowercase.
    week = models.CharField(db_column='Week', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_schedule_detail_pre'


class ByScheduleDetail(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    scode = models.ForeignKey('ByScheduleDetailPre',  db_column='SCode',to_field="code",on_delete=models.CASCADE)  # Field name made lowercase.
    starttime = models.CharField(db_column='StartTime', max_length=20)  # Field name made lowercase.
    stoptime = models.CharField(db_column='StopTime', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_schedule_detail'


class ByScheduleType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_schedule_type'



class ByZoneType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'by_zone_type'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class ByAdMaterialAnimation(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    extname = models.CharField(db_column='ExtName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    diskcode = models.CharField(db_column='DiskCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_material_animation'


class ByAdMaterialFile(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.
    extname = models.CharField(db_column='ExtName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    diskcode = models.CharField(db_column='DiskCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_material_file'


class ByAdMaterialImage(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.
    extname = models.CharField(db_column='ExtName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    diskcode = models.CharField(db_column='DiskCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_material_image'


class ByAdMaterialVedio(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.
    extname = models.CharField(db_column='ExtName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    diskcode = models.CharField(db_column='DiskCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_material_vedio'
class ByAdMaterialSound(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.
    extname = models.CharField(db_column='ExtName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    diskcode = models.CharField(db_column='DiskCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_material_sound'
class ByAdLicense(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    licensecode = models.CharField(db_column='LicenseCode', unique=True, max_length=32)  # Field name made lowercase.
    terminalcode = models.ForeignKey(SmartDevices, models.DO_NOTHING, db_column='TerminalCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    orgcode = models.ForeignKey(SmartOrganization, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'by_ad_licenses'

class SmartDevicestat(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    terminalcode = models.ForeignKey(SmartDevices, models.DO_NOTHING, db_column='TerminalCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    cpu = models.IntegerField(db_column='Cpu', blank=True, null=True)  # Field name made lowercase.
    memory = models.IntegerField(db_column='Memory', blank=True, null=True)  # Field name made lowercase.
    disk = models.IntegerField(db_column='Disk', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.CharField(db_column='UpdateTime', max_length=20)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_player_stat'

class ByAdPlayerDownload(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    terminalcode = models.ForeignKey(SmartDevices, models.DO_NOTHING, db_column='TerminalCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    adcode = models.ForeignKey(ByAdChannel, models.DO_NOTHING, db_column='AdCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    updatetime = models.CharField(db_column='UpdateTime', max_length=20)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'by_ad_player_download'
