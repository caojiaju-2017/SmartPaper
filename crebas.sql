/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018-09-18 11:30:00                          */
/*==============================================================*/


drop index Index_1 on paper_account;

drop table if exists paper_account;

drop index Index_1 on paper_dev_controls;

drop table if exists paper_dev_controls;

drop index Index_1 on paper_dev_goods_map;

drop table if exists paper_dev_goods_map;

drop index Index_1 on paper_devices;

drop table if exists paper_devices;

drop index Index_2 on paper_functions;

drop index Index_code on paper_functions;

drop table if exists paper_functions;

drop index Index_1 on paper_goods;

drop table if exists paper_goods;

drop index Index_1 on paper_orders;

drop table if exists paper_orders;

drop index Index_1 on paper_orgs;

drop table if exists paper_orgs;

drop index Index_code on paper_role_func;

drop table if exists paper_role_func;

drop index Index_2 on paper_roles;

drop index Index_code on paper_roles;

drop table if exists paper_roles;

drop index Index_code on paper_runlog;

drop table if exists paper_runlog;

drop index Index_code on paper_user_role;

drop table if exists paper_user_role;

drop index Index_code on paper_version;

drop table if exists paper_version;

/*==============================================================*/
/* Table: paper_account                                         */
/*==============================================================*/
create table paper_account
(
   Id                   int not null,
   Code                 varchar(32) not null,
   Account              varchar(18),
   Password             varchar(20),
   WorkNo               varchar(20),
   Alias                varchar(64),
   Mobile               varchar(20),
   OrgCode              varchar(32),
   RegDate              varchar(10),
   State                int,
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_account
(
   Code
);

/*==============================================================*/
/* Table: paper_dev_controls                                    */
/*==============================================================*/
create table paper_dev_controls
(
   Id                   int not null,
   Code                 varchar(32) not null,
   CtrlTime             Varchar(20),
   Type                 int,
   ControlCommand       varchar(200),
   DCode                varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_dev_controls
(
   Code
);

/*==============================================================*/
/* Table: paper_dev_goods_map                                   */
/*==============================================================*/
create table paper_dev_goods_map
(
   Id                   int not null,
   Code                 varchar(32) not null,
   DCode                varchar(32),
   GCode                varchar(32),
   Count                int,
   LockCount            int,
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_dev_goods_map
(
   Code
);

/*==============================================================*/
/* Table: paper_devices                                         */
/*==============================================================*/
create table paper_devices
(
   Id                   int not null,
   Code                 varchar(32) not null,
   IpAddress            Varchar(20),
   Mac                  varchar(20),
   LastLoginTime        varchar(20),
   OrgCode              varchar(32),
   State                int,
   Name                 varchar(64),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_devices
(
   Code
);

/*==============================================================*/
/* Table: paper_functions                                       */
/*==============================================================*/
create table paper_functions
(
   Id                   int not null auto_increment,
   Code                 varchar(32) not null,
   Name                 varchar(64),
   FuncId               int,
   DoPage               varchar(128),
   FreeFlag             int default 0,
   PCode                varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_functions
(
   Code
);

/*==============================================================*/
/* Index: Index_2                                               */
/*==============================================================*/
create unique index Index_2 on paper_functions
(
   FuncId
);

/*==============================================================*/
/* Table: paper_goods                                           */
/*==============================================================*/
create table paper_goods
(
   Id                   int not null,
   Code                 varchar(32) not null,
   Name                 Varchar(64),
   Price                float,
   Model                Varchar(64),
   Info                 varchar(200),
   Simage               varchar(64),
   limage               varchar(64),
   State                int,
   OrgCode              varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_goods
(
   Code
);

/*==============================================================*/
/* Table: paper_orders                                          */
/*==============================================================*/
create table paper_orders
(
   Id                   int not null,
   Code                 varchar(32) not null,
   DCode                Varchar(32),
   GCode                Varchar(32),
   Price                float,
   Count                int,
   TradeTime            varchar(20),
   PayTime              varchar(20),
   State                int,
   OrgCode              varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_orders
(
   Code
);

/*==============================================================*/
/* Table: paper_orgs                                            */
/*==============================================================*/
create table paper_orgs
(
   Id                   int not null,
   Code                 varchar(32) not null,
   Name                 varchar(64),
   ContactName          varchar(64),
   ContactPhone         varchar(20),
   RegDate              varchar(10),
   Logo                 varchar(64),
   State                int,
   ParentCode           varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_1                                               */
/*==============================================================*/
create index Index_1 on paper_orgs
(
   Code
);

/*==============================================================*/
/* Table: paper_role_func                                       */
/*==============================================================*/
create table paper_role_func
(
   Id                   int not null,
   Code                 varchar(32) not null,
   Flag                 varchar(12),
   RCode                varchar(32),
   FCode                varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_role_func
(
   Code
);

/*==============================================================*/
/* Table: paper_roles                                           */
/*==============================================================*/
create table paper_roles
(
   Id                   int not null,
   Code                 varchar(32) not null,
   OrgCode              varchar(32),
   Name                 varchar(64),
   Content              varchar(2000),
   State                int default 1,
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_roles
(
   Code
);

/*==============================================================*/
/* Index: Index_2                                               */
/*==============================================================*/
create unique index Index_2 on paper_roles
(
   Code
);

/*==============================================================*/
/* Table: paper_runlog                                          */
/*==============================================================*/
create table paper_runlog
(
   Id                   int not null,
   Code                 varchar(32) not null,
   OrgCode              varchar(32),
   OpertType            int,
   Content              varchar(200),
   IP                   varchar(15),
   UCode                varchar(32),
   TerminalCode         varchar(32) default '1',
   LogTime              varchar(20),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_runlog
(
   Code
);

/*==============================================================*/
/* Table: paper_user_role                                       */
/*==============================================================*/
create table paper_user_role
(
   Id                   int not null,
   Code                 varchar(32) not null,
   ACode                varchar(32),
   RCode                varchar(32),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_user_role
(
   Code
);

/*==============================================================*/
/* Table: paper_version                                         */
/*==============================================================*/
create table paper_version
(
   Id                   int not null,
   Code                 varchar(32) not null,
   OrgCode              varchar(32),
   Type                 int default 1,
   Version              varchar(20),
   RegTime              varchar(20),
   Name                 varchar(36),
   primary key (Id)
);

/*==============================================================*/
/* Index: Index_code                                            */
/*==============================================================*/
create unique index Index_code on paper_version
(
   Code
);

alter table paper_account add constraint FK_AcntOrgRelation foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_dev_controls add constraint FK_ControlDevCodeRelation foreign key (DCode)
      references paper_devices (Code) on delete restrict on update restrict;

alter table paper_dev_goods_map add constraint FK_DevGoodsGCode foreign key (GCode)
      references paper_goods (Code) on delete restrict on update restrict;

alter table paper_dev_goods_map add constraint FK_DeviceGoodsDevCode foreign key (DCode)
      references paper_devices (Code) on delete restrict on update restrict;

alter table paper_devices add constraint FK_DeviceOrgRelation foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_functions add constraint FK_FunctionSelfRelation foreign key (PCode)
      references paper_functions (Code) on delete restrict on update restrict;

alter table paper_goods add constraint FK_GoodsOrgRelation foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_orders add constraint FK_GoodsDeviceCodeRelation foreign key (DCode)
      references paper_devices (Code) on delete restrict on update restrict;

alter table paper_orders add constraint FK_OrderGoodsCodeRelation foreign key (GCode)
      references paper_goods (Code) on delete restrict on update restrict;

alter table paper_orgs add constraint FK_OrgSelfRelation foreign key (ParentCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_role_func add constraint FK_FuncRoleRoleCode foreign key (RCode)
      references paper_roles (Code) on delete restrict on update restrict;

alter table paper_role_func add constraint FK_RoleFuncFuncCode foreign key (FCode)
      references paper_functions (Code) on delete restrict on update restrict;

alter table paper_roles add constraint FK_RoleOrgRelation foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_runlog add constraint FK_RunlogOrgCode foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

alter table paper_user_role add constraint FK_RoleAcntRelRolecode foreign key (RCode)
      references paper_roles (Code) on delete restrict on update restrict;

alter table paper_user_role add constraint FK_RoleAcntRelation foreign key (ACode)
      references paper_account (Code) on delete restrict on update restrict;

alter table paper_version add constraint FK_VersionOrgCode foreign key (OrgCode)
      references paper_orgs (Code) on delete restrict on update restrict;

