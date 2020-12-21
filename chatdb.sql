-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: chatdb
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` bigint NOT NULL,
  `byuser` bigint DEFAULT NULL,
  `class` varchar(32) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,1,'XII-A','test');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignmentinfo`
--

DROP TABLE IF EXISTS `assignmentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignmentinfo` (
  `id` bigint DEFAULT NULL,
  `assignmentid` bigint DEFAULT NULL,
  `userid` bigint DEFAULT NULL,
  `status` int DEFAULT NULL,
  `attachment` blob,
  `attachmentname` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignmentinfo`
--

LOCK TABLES `assignmentinfo` WRITE;
/*!40000 ALTER TABLE `assignmentinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignmentinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments`
--

DROP TABLE IF EXISTS `assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignments` (
  `id` bigint DEFAULT NULL,
  `class` varchar(32) DEFAULT NULL,
  `content` varchar(512) DEFAULT NULL,
  `attachment` blob,
  `attachmentname` varchar(128) DEFAULT NULL,
  `submission` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments`
--

LOCK TABLES `assignments` WRITE;
/*!40000 ALTER TABLE `assignments` DISABLE KEYS */;
/*!40000 ALTER TABLE `assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attachments`
--

DROP TABLE IF EXISTS `attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attachments` (
  `id` bigint DEFAULT NULL,
  `file` blob,
  `filename` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachments`
--

LOCK TABLES `attachments` WRITE;
/*!40000 ALTER TABLE `attachments` DISABLE KEYS */;
/*!40000 ALTER TABLE `attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channelmembers`
--

DROP TABLE IF EXISTS `channelmembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channelmembers` (
  `id` bigint NOT NULL,
  `channelId` bigint DEFAULT NULL,
  `userid` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channelmembers`
--

LOCK TABLES `channelmembers` WRITE;
/*!40000 ALTER TABLE `channelmembers` DISABLE KEYS */;
INSERT INTO `channelmembers` VALUES (1,1,1),(2,1,2),(3,2,1),(4,2,2),(5,3,1),(6,4,1),(7,4,2),(8,5,1),(9,5,3);
/*!40000 ALTER TABLE `channelmembers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `channels` (
  `id` bigint NOT NULL,
  `name` varchar(25) NOT NULL,
  `flags` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (1,'general',0),(2,'test-channel',0),(3,'third-channel',0),(4,'DM_A_B',1),(5,'DM_P_Q',1);
/*!40000 ALTER TABLE `channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatmessages`
--

DROP TABLE IF EXISTS `chatmessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatmessages` (
  `Id` bigint NOT NULL,
  `User` bigint DEFAULT NULL,
  `Content` varchar(200) NOT NULL,
  `Channel` bigint DEFAULT NULL,
  `attachment` bigint DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatmessages`
--

LOCK TABLES `chatmessages` WRITE;
/*!40000 ALTER TABLE `chatmessages` DISABLE KEYS */;
INSERT INTO `chatmessages` VALUES (1,1,'Hi',1,NULL),(2,1,'Hello',1,NULL),(3,2,'Hey',1,NULL),(32524543636,1,'abc',2,NULL),(1870121742568132608,1,'testing',1,NULL),(1870121806799704064,1,'is this working?',1,NULL),(1870125598546989056,1,'',1,NULL),(1870135778324123648,1,'test',1,NULL),(1870136005990944768,1,'Is this working',1,NULL),(1870136078422380544,1,'yes yes yes its working',1,NULL),(1870136103202328576,1,'test',1,NULL),(1870136122412240896,1,'test',1,NULL),(1870136332421042176,1,'working?',1,NULL),(1870136390235328512,1,'working?',1,NULL),(1870136774710398976,1,'test',1,NULL),(1870136834328236032,1,'cool',1,NULL),(1870137107146739712,1,'test',1,NULL),(1870137138348167168,1,'kui7i',1,NULL),(1870429778771841024,1,'test',1,NULL),(1870429799554617344,1,'ayaya',1,NULL),(1870429814402453504,1,'this works',1,NULL),(1870434234154487808,1,'ayy',1,NULL),(1870434853535748096,1,'yolo',1,NULL),(1870435592358203392,1,'tet',1,NULL),(1870436517219012608,1,'ayy',1,NULL),(1870446206107389952,1,'yeet',1,NULL),(1870818844591919104,1,'this works',2,NULL),(1870818884379086848,1,'yes',3,NULL),(1870818954855976960,1,'ayy',2,NULL),(1870818996161482752,1,'yee',2,NULL),(1870819115694952448,1,'user',3,NULL),(1870820232457752576,2,'user',2,NULL),(1870820258881867776,2,'me',2,NULL);
/*!40000 ALTER TABLE `chatmessages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatusers`
--

DROP TABLE IF EXISTS `chatusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatusers` (
  `Id` bigint NOT NULL,
  `Username` varchar(256) DEFAULT NULL,
  `password` varchar(256) DEFAULT NULL,
  `permissions` smallint DEFAULT NULL,
  `class` varchar(32) DEFAULT NULL,
  `avatar` blob,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatusers`
--

LOCK TABLES `chatusers` WRITE;
/*!40000 ALTER TABLE `chatusers` DISABLE KEYS */;
INSERT INTO `chatusers` VALUES (1,'Krishiv',NULL,NULL,'XII-A',NULL),(2,'TestUser',NULL,NULL,'XII-A',NULL);
/*!40000 ALTER TABLE `chatusers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dmrequests`
--

DROP TABLE IF EXISTS `dmrequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dmrequests` (
  `id` bigint NOT NULL,
  `toUser` bigint DEFAULT NULL,
  `byUser` bigint DEFAULT NULL,
  `requestcontent` varchar(512) DEFAULT NULL,
  `expires` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dmrequests`
--

LOCK TABLES `dmrequests` WRITE;
/*!40000 ALTER TABLE `dmrequests` DISABLE KEYS */;
/*!40000 ALTER TABLE `dmrequests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokens` (
  `id` bigint DEFAULT NULL,
  `token` varchar(256) DEFAULT NULL,
  `expires` date DEFAULT NULL,
  `user` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens`
--

LOCK TABLES `tokens` WRITE;
/*!40000 ALTER TABLE `tokens` DISABLE KEYS */;
INSERT INTO `tokens` VALUES (1,'abc','2020-12-24',1);
/*!40000 ALTER TABLE `tokens` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-15 22:47:35
