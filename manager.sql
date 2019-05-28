-- MySQL dump 10.13  Distrib 5.6.21, for osx10.8 (x86_64)
-- 
-- Host: localhost    Database : manager
-- ------------------------------------------------------
-- Server version	5.6.21
-- root管理员账号root1234   管理员密码a123456


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 
-- Table structure for table `tb_manager`
-- 
DROP TABLE IF EXISTS `tb_manager`;
CREATE TABLE `tb_manager` (
	`manager_id` bigint(20) NOT NULL AUTO_INCREMENT,
	`manager_account` varchar(40) DEFAULT NULL,
	`manager_level` varchar(10) DEFAULT NULL,
	`manager_password` varchar(256) DEFAULT NULL,
	PRIMARY KEY(`manager_id`)
	) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8;
	
	
-- 
-- Dumping data for table `tb_manager`
-- 
LOCK TABLES `tb_manager` WRITE;
INSERT INTO `tb_manager` VALUES('1', 'root1234', 'root管理员', 'pbkdf2:sha1:1000$yyA2IvmG$246ea3e3b5fd122ee6fcea4b48971174b4edcf97');
UNLOCK TABLES;


--
-- Create validateManagerlogin Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_validateManagerlogin`(
IN p_account VARCHAR(40)
)
BEGIN
select manager_id,manager_password from tb_manager where manager_account = p_account;
END;;
DELIMITER ;


--
-- Create Manager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_createManager`(
IN p_account VARCHAR(40),
IN p_password VARCHAR(256)
)
BEGIN
if (select exists(select 1 from tb_manager where manager_account = p_account)) THEN
select '账户已存在！';

ELSE
insert into tb_manager(manager_account,manager_level,manager_password)
values(p_account,'普通管理员',p_password);

END IF;
END;;
DELIMITER ;


--
-- Create deleteManager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_deleteManager`(
IN p_id bigint(20)
)
BEGIN
delete from tb_manager where manager_id = p_id;
END;;
DELIMITER ;


--
-- Create getallManager Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getallManager`()
BEGIN
select manager_id,manager_account,manager_level from tb_manager;
END;;
DELIMITER ;


--
-- Create getManager_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getManager_byid`(
IN p_id bigint(20)
)
BEGIN
select manager_id,manager_account,manager_level from tb_manager where manager_id = p_id;
END;;
DELIMITER ;


--
-- Create getManagerpsw_byid Procedure
--
DELIMITER ;;
CREATE DEFINER = `root`@`localhost` PROCEDURE `sp_getManagerpsw_byid`(
IN p_id bigint(20)
)
BEGIN
select manager_password from tb_manager where manager_id = p_id;
END;;
DELIMITER ;