/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : cfppaper

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2018-09-27 17:05:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `django_migrations`
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_account`
-- ----------------------------
DROP TABLE IF EXISTS `paper_account`;
CREATE TABLE `paper_account` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `Account` varchar(18) DEFAULT NULL,
  `Password` varchar(32) DEFAULT NULL,
  `WorkNo` varchar(20) DEFAULT NULL,
  `Alias` varchar(64) DEFAULT NULL,
  `Mobile` varchar(20) DEFAULT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  `RegDate` varchar(10) DEFAULT NULL,
  `State` int(11) DEFAULT NULL,
  `Type` int(11) DEFAULT '0',
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_AcntOrgRelation` (`OrgCode`),
  CONSTRAINT `FK_AcntOrgRelation` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_account
-- ----------------------------
INSERT INTO `paper_account` VALUES ('1', 'cadd0280bb1111e8bfc1989096c1d848', '15680585185', '81dc9bdb52d04dc20036dbd8313ed055', 'z10990', '郭先生', '15680585185', 'cadd0280bb1111e8bfc1989096c1d848', '2018-09-22', '1', '1');

-- ----------------------------
-- Table structure for `paper_devices`
-- ----------------------------
DROP TABLE IF EXISTS `paper_devices`;
CREATE TABLE `paper_devices` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `IpAddress` varchar(20) DEFAULT NULL,
  `Mac` varchar(20) DEFAULT NULL,
  `LastLoginTime` varchar(20) DEFAULT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  `State` int(11) DEFAULT NULL,
  `Name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_DeviceOrgRelation` (`OrgCode`),
  CONSTRAINT `FK_DeviceOrgRelation` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_devices
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_dev_controls`
-- ----------------------------
DROP TABLE IF EXISTS `paper_dev_controls`;
CREATE TABLE `paper_dev_controls` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `CtrlTime` varchar(20) DEFAULT NULL,
  `Type` int(11) DEFAULT NULL,
  `ControlCommand` varchar(200) DEFAULT NULL,
  `DCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_ControlDevCodeRelation` (`DCode`),
  CONSTRAINT `FK_ControlDevCodeRelation` FOREIGN KEY (`DCode`) REFERENCES `paper_devices` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_dev_controls
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_dev_goods_map`
-- ----------------------------
DROP TABLE IF EXISTS `paper_dev_goods_map`;
CREATE TABLE `paper_dev_goods_map` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `DCode` varchar(32) DEFAULT NULL,
  `GCode` varchar(32) DEFAULT NULL,
  `Count` int(11) DEFAULT NULL,
  `LockCount` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_DevGoodsGCode` (`GCode`),
  KEY `FK_DeviceGoodsDevCode` (`DCode`),
  CONSTRAINT `FK_DevGoodsGCode` FOREIGN KEY (`GCode`) REFERENCES `paper_goods` (`Code`),
  CONSTRAINT `FK_DeviceGoodsDevCode` FOREIGN KEY (`DCode`) REFERENCES `paper_devices` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_dev_goods_map
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_functions`
-- ----------------------------
DROP TABLE IF EXISTS `paper_functions`;
CREATE TABLE `paper_functions` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `Name` varchar(64) DEFAULT NULL,
  `FuncId` int(11) DEFAULT NULL,
  `DoPage` varchar(128) DEFAULT NULL,
  `FreeFlag` int(11) DEFAULT '0',
  `PCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  UNIQUE KEY `Index_2` (`FuncId`),
  KEY `FK_FunctionSelfRelation` (`PCode`),
  CONSTRAINT `FK_FunctionSelfRelation` FOREIGN KEY (`PCode`) REFERENCES `paper_functions` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_functions
-- ----------------------------
INSERT INTO `paper_functions` VALUES ('1', '0062be213bbb11e89b2c0215f76570b3', '单位管理', '10001', '', '1', null);
INSERT INTO `paper_functions` VALUES ('12', '1d41a2593bbc11e89b2c0215f76570b3', '角色管理', '10002', null, '1', null);
INSERT INTO `paper_functions` VALUES ('13', '1d5186c83bbc11e89b2c0215f76570b3', '账户管理', '10003', null, '1', null);
INSERT INTO `paper_functions` VALUES ('14', '1d5857513bbc11e89b2c0215f76570b3', '基础设备', '10004', null, '1', null);
INSERT INTO `paper_functions` VALUES ('18', '210a28ca415011e8b3470215f76570b3', '电源管理', '10005', null, '1', null);
INSERT INTO `paper_functions` VALUES ('19', '21d8315e415011e8b3470215f76570b3', '灯光管理', '10006', null, '1', null);
INSERT INTO `paper_functions` VALUES ('21', '560cef34415011e8b3470215f76570b3', '策略管理', '10008', null, '1', null);
INSERT INTO `paper_functions` VALUES ('22', '565bf7f6415011e8b3470215f76570b3', '分区管理', '10007', null, '1', null);
INSERT INTO `paper_functions` VALUES ('23', '9fc6e571415011e8b3470215f76570b3', '日志查询', '10009', null, '1', null);

-- ----------------------------
-- Table structure for `paper_goods`
-- ----------------------------
DROP TABLE IF EXISTS `paper_goods`;
CREATE TABLE `paper_goods` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `Name` varchar(64) DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `Model` varchar(64) DEFAULT NULL,
  `Info` varchar(200) DEFAULT NULL,
  `Simage` varchar(64) DEFAULT NULL,
  `limage` varchar(64) DEFAULT NULL,
  `State` int(11) DEFAULT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_GoodsOrgRelation` (`OrgCode`),
  CONSTRAINT `FK_GoodsOrgRelation` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_goods
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_orders`
-- ----------------------------
DROP TABLE IF EXISTS `paper_orders`;
CREATE TABLE `paper_orders` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `DCode` varchar(32) DEFAULT NULL,
  `GCode` varchar(32) DEFAULT NULL,
  `Price` float DEFAULT NULL,
  `Count` int(11) DEFAULT NULL,
  `TradeTime` varchar(20) DEFAULT NULL,
  `PayTime` varchar(20) DEFAULT NULL,
  `State` int(11) DEFAULT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_GoodsDeviceCodeRelation` (`DCode`),
  KEY `FK_OrderGoodsCodeRelation` (`GCode`),
  CONSTRAINT `FK_GoodsDeviceCodeRelation` FOREIGN KEY (`DCode`) REFERENCES `paper_devices` (`Code`),
  CONSTRAINT `FK_OrderGoodsCodeRelation` FOREIGN KEY (`GCode`) REFERENCES `paper_goods` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_orders
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_orgs`
-- ----------------------------
DROP TABLE IF EXISTS `paper_orgs`;
CREATE TABLE `paper_orgs` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `Name` varchar(64) DEFAULT NULL,
  `ContactName` varchar(64) DEFAULT NULL,
  `ContactPhone` varchar(20) DEFAULT NULL,
  `RegDate` varchar(10) DEFAULT NULL,
  `Logo` varchar(64) DEFAULT NULL,
  `State` int(11) DEFAULT NULL,
  `ParentCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Index_1` (`Code`),
  KEY `FK_OrgSelfRelation` (`ParentCode`),
  CONSTRAINT `FK_OrgSelfRelation` FOREIGN KEY (`ParentCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_orgs
-- ----------------------------
INSERT INTO `paper_orgs` VALUES ('1', 'cadd0280bb1111e8bfc1989096c1d848', '长江实业有限责任公司', '郭先生', '15203695201', '2018-09-23', null, '1', null);

-- ----------------------------
-- Table structure for `paper_roles`
-- ----------------------------
DROP TABLE IF EXISTS `paper_roles`;
CREATE TABLE `paper_roles` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  `Name` varchar(64) DEFAULT NULL,
  `Content` varchar(2000) DEFAULT NULL,
  `State` int(11) DEFAULT '1',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  UNIQUE KEY `Index_2` (`Code`),
  KEY `FK_RoleOrgRelation` (`OrgCode`),
  CONSTRAINT `FK_RoleOrgRelation` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_roles
-- ----------------------------
INSERT INTO `paper_roles` VALUES ('1', 'd4bdb79e745711e89da4989096c1d848', 'cadd0280bb1111e8bfc1989096c1d848', 'test', '法撒旦范德萨', '1');

-- ----------------------------
-- Table structure for `paper_role_func`
-- ----------------------------
DROP TABLE IF EXISTS `paper_role_func`;
CREATE TABLE `paper_role_func` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `Flag` varchar(16) DEFAULT NULL,
  `RCode` varchar(32) DEFAULT NULL,
  `FCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  KEY `FK_FuncRoleRoleCode` (`RCode`),
  KEY `FK_RoleFuncFuncCode` (`FCode`),
  CONSTRAINT `FK_FuncRoleRoleCode` FOREIGN KEY (`RCode`) REFERENCES `paper_roles` (`Code`),
  CONSTRAINT `FK_RoleFuncFuncCode` FOREIGN KEY (`FCode`) REFERENCES `paper_functions` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_role_func
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_runlog`
-- ----------------------------
DROP TABLE IF EXISTS `paper_runlog`;
CREATE TABLE `paper_runlog` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  `OpertType` int(11) DEFAULT NULL,
  `Content` varchar(200) DEFAULT NULL,
  `IP` varchar(15) DEFAULT NULL,
  `UCode` varchar(32) DEFAULT NULL,
  `TerminalCode` varchar(32) DEFAULT '1',
  `LogTime` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  KEY `FK_RunlogOrgCode` (`OrgCode`),
  CONSTRAINT `FK_RunlogOrgCode` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_runlog
-- ----------------------------

-- ----------------------------
-- Table structure for `paper_user_role`
-- ----------------------------
DROP TABLE IF EXISTS `paper_user_role`;
CREATE TABLE `paper_user_role` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `ACode` varchar(32) DEFAULT NULL,
  `RCode` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  KEY `FK_RoleAcntRelRolecode` (`RCode`),
  KEY `FK_RoleAcntRelation` (`ACode`),
  CONSTRAINT `FK_RoleAcntRelation` FOREIGN KEY (`ACode`) REFERENCES `paper_account` (`Code`),
  CONSTRAINT `FK_RoleAcntRelRolecode` FOREIGN KEY (`RCode`) REFERENCES `paper_roles` (`Code`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_user_role
-- ----------------------------
INSERT INTO `paper_user_role` VALUES ('3', '6e311b61745e11e889d2989096c1d848', 'cadd0280bb1111e8bfc1989096c1d848', 'd4bdb79e745711e89da4989096c1d848');

-- ----------------------------
-- Table structure for `paper_version`
-- ----------------------------
DROP TABLE IF EXISTS `paper_version`;
CREATE TABLE `paper_version` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(32) NOT NULL,
  `OrgCode` varchar(32) DEFAULT NULL,
  `Type` int(11) DEFAULT '1',
  `Version` varchar(20) DEFAULT NULL,
  `RegTime` varchar(20) DEFAULT NULL,
  `Name` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Index_code` (`Code`),
  KEY `FK_VersionOrgCode` (`OrgCode`),
  CONSTRAINT `FK_VersionOrgCode` FOREIGN KEY (`OrgCode`) REFERENCES `paper_orgs` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of paper_version
-- ----------------------------
