# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class PaperAccount(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32,unique=True)  # Field name made lowercase.
    account = models.CharField(db_column='Account', max_length=18, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=32, blank=True, null=True)  # Field name made lowercase.
    workno = models.CharField(db_column='WorkNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=64, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('PaperOrgs', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_account'


class PaperDevControls(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32)  # Field name made lowercase.
    ctrltime = models.CharField(db_column='CtrlTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    controlcommand = models.CharField(db_column='ControlCommand', max_length=200, blank=True, null=True)  # Field name made lowercase.
    dcode = models.ForeignKey('PaperDevices', models.DO_NOTHING, db_column='DCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_dev_controls'


class PaperDevGoodsMap(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32)  # Field name made lowercase.
    dcode = models.ForeignKey('PaperDevices', models.DO_NOTHING, db_column='DCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    gcode = models.ForeignKey('PaperGoods', models.DO_NOTHING, db_column='GCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    lockcount = models.IntegerField(db_column='LockCount', blank=True, null=True)  # Field name made lowercase.
    trackindex = models.IntegerField(db_column='TrackIndex', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_dev_goods_map'


class PaperDevices(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32,unique=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IpAddress', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mac = models.CharField(db_column='Mac', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastlogintime = models.CharField(db_column='LastLoginTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('PaperOrgs', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.

    managename = models.CharField(db_column='MName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    managephone = models.CharField(db_column='MPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Logitude', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    devtype = models.CharField(db_column='DevType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_devices'


class PaperFunctions(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    funcid = models.IntegerField(db_column='FuncId', unique=True, blank=True, null=True)  # Field name made lowercase.
    dopage = models.CharField(db_column='DoPage', max_length=128, blank=True, null=True)  # Field name made lowercase.
    freeflag = models.IntegerField(db_column='FreeFlag', blank=True, null=True)  # Field name made lowercase.
    pcode = models.ForeignKey('self', models.DO_NOTHING, db_column='PCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_functions'


class PaperGoods(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32,unique=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=64, blank=True, null=True)  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=200, blank=True, null=True)  # Field name made lowercase.
    simage = models.CharField(db_column='Simage', max_length=64, blank=True, null=True)  # Field name made lowercase.
    limage = models.CharField(max_length=64, blank=True, null=True)
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('PaperOrgs', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_goods'


class PaperOrders(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32)  # Field name made lowercase.
    dcode = models.ForeignKey(PaperDevices, models.DO_NOTHING, db_column='DCode', blank=True, null=True)  # Field name made lowercase.
    gcode = models.ForeignKey(PaperGoods, models.DO_NOTHING, db_column='GCode', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    tradetime = models.CharField(db_column='TradeTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    paytime = models.CharField(db_column='PayTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.CharField(db_column='OrgCode', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_orders'


class PaperOrgs(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32, unique=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    contactname = models.CharField(db_column='ContactName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    contactphone = models.CharField(db_column='ContactPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regdate = models.CharField(db_column='RegDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    logo = models.CharField(db_column='Logo', max_length=64, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    # parentcode = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentCode', blank=True, null=True)  # Field name made lowercase.
    parentcode = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentCode', blank=True, null=True,
                                   to_field="code", related_name="children")  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'paper_orgs'


class PaperRoleFunc(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    flag = models.CharField(db_column='Flag', max_length=16, blank=True, null=True)  # Field name made lowercase.
    rcode = models.ForeignKey('PaperRoles', models.DO_NOTHING, db_column='RCode', blank=True, null=True)  # Field name made lowercase.
    fcode = models.ForeignKey(PaperFunctions, models.DO_NOTHING, db_column='FCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_role_func'


class PaperRoles(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    # orgcode = models.ForeignKey(PaperOrgs, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True)  # Field name made lowercase.
    orgcode = models.ForeignKey('PaperOrgs', models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,
                                to_field="code")  # Field name made lowercase.

    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_roles'


class PaperRunlog(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    orgcode = models.ForeignKey(PaperOrgs, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    # operttype = models.IntegerField(db_column='OpertType', blank=True, null=True)  # Field name made lowercase.
    operttype = models.CharField(db_column='OpertType', max_length=32, blank=True, null=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ucode = models.CharField(db_column='UCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    terminalcode = models.CharField(db_column='TerminalCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    logtime = models.CharField(db_column='LogTime', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_runlog'


class PaperUserRole(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    acode = models.ForeignKey(PaperAccount, models.DO_NOTHING, db_column='ACode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    rcode = models.ForeignKey(PaperRoles, models.DO_NOTHING, db_column='RCode', blank=True, null=True,to_field="code")  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_user_role'


class PaperVersion(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    orgcode = models.ForeignKey(PaperOrgs, models.DO_NOTHING, db_column='OrgCode', blank=True, null=True,to_field="code")  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=20, blank=True, null=True)  # Field name made lowercase.
    regtime = models.CharField(db_column='RegTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_version'

class PaperDevicesEvent(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    mac = models.CharField(db_column='Mac', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eventtime = models.CharField(db_column='EventTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eventid = models.CharField(db_column='EventId', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'paper_devices_event'

class PaperApplyFreePaper(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    # DevCode = models.CharField(db_column='Mac', max_length=20, blank=True, null=True)  # Field name made lowercase.
    devcode = models.ForeignKey('PaperDevices', models.DO_NOTHING, db_column='DevCode', blank=True,
                              null=True,to_field="code")  # Field name made lowercase.
    devmac = models.CharField(db_column='DevMac', max_length=20, blank=True, null=True)  # Field name made lowercase.
    applytime = models.CharField(db_column='ApplyTime', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'paper_apply_freepaper'

class PaperWxCustom(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    headimage = models.CharField(db_column='HeadImage', max_length=2000, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_wx_custom'

class PaperWxTicket(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='Ticket', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    signtime = models.CharField(db_column='SignTime', max_length=32, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.CharField(db_column='TimeStamp', max_length=32, blank=True,null=True)  # Field name made lowercase.
    noncestr = models.CharField(db_column='NonceStr', max_length=20, blank=True,null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=64, blank=True, null=True)  # Field name made lowercase.
    appid = models.CharField(db_column='AppId', max_length=64, blank=True, null=True)  # Field name made lowercase.
    timeoutsecond = models.IntegerField(db_column='TimeOutSecond', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paper_wx_ticket'