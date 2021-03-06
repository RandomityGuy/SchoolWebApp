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
INSERT INTO `announcements` VALUES (1979958856402472960,1952670716730150912,'XII-A','Hello students'),(1979958856406667264,1952670716730150912,'null','Hello students'),(1979959423996661760,1952670716730150912,'XII-A','Exams start from Monday 8/3/21'),(1979959555915911168,1952670716730150912,'XII-A','School closes from beginning of april'),(1979959824913403904,1952670716730150912,'null','New Announcement'),(1979959892441698305,1952670716730150912,'null','Test Announcement');
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
INSERT INTO `channelmembers` VALUES (1,1,1),(2,1,2),(3,2,1),(4,2,2),(5,3,1),(6,4,1),(7,4,2),(8,5,1),(9,5,3),(10,1,1952670716730150912),(1953780850437001216,1953780850386669568,1952670716730150912),(1953780850453778432,1953780850386669568,1),(1953786424641851392,1953786424625074176,1952670716730150912),(1953786424641851393,1953786424625074176,2),(1954646067668717568,1954646067651940352,1952670716730150912),(1954646067668717569,1954646067651940352,1952670716730150912);
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
  `name` varchar(256) DEFAULT NULL,
  `flags` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (1,'general',0),(2,'test-channel',0),(3,'third-channel',0),(4,'DM_A_B',1),(5,'DM_P_Q',1),(1953780850386669568,'DM_1952670716730150912_1',1),(1953786424625074176,'DM_1952670716730150912_2',1),(1954646067651940352,'DM_1952670716730150912_1952670716730150912',1);
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
INSERT INTO `chatmessages` VALUES (1,1,'Hi',1,NULL),(2,1,'Hello',1,NULL),(3,2,'Hey',1,NULL),(32524543636,1,'abc',2,NULL),(1870121742568132608,1,'testing',1,NULL),(1870121806799704064,1,'is this working?',1,NULL),(1870125598546989056,1,'',1,NULL),(1870135778324123648,1,'test',1,NULL),(1870136005990944768,1,'Is this working',1,NULL),(1870136078422380544,1,'yes yes yes its working',1,NULL),(1870136103202328576,1,'test',1,NULL),(1870136122412240896,1,'test',1,NULL),(1870136332421042176,1,'working?',1,NULL),(1870136390235328512,1,'working?',1,NULL),(1870136774710398976,1,'test',1,NULL),(1870136834328236032,1,'cool',1,NULL),(1870137107146739712,1,'test',1,NULL),(1870137138348167168,1,'kui7i',1,NULL),(1870429778771841024,1,'test',1,NULL),(1870429799554617344,1,'ayaya',1,NULL),(1870429814402453504,1,'this works',1,NULL),(1870434234154487808,1,'ayy',1,NULL),(1870434853535748096,1,'yolo',1,NULL),(1870435592358203392,1,'tet',1,NULL),(1870436517219012608,1,'ayy',1,NULL),(1870446206107389952,1,'yeet',1,NULL),(1870818844591919104,1,'this works',2,NULL),(1870818884379086848,1,'yes',3,NULL),(1870818954855976960,1,'ayy',2,NULL),(1870818996161482752,1,'yee',2,NULL),(1870819115694952448,1,'user',3,NULL),(1870820232457752576,2,'user',2,NULL),(1870820258881867776,2,'me',2,NULL),(1953794737429417984,1952670716730150912,'test',1,NULL),(1953794968606871552,1952670716730150912,'test',1,NULL),(1953795481138237440,1952670716730150912,'hello',1,NULL),(1953795515049185280,1952670716730150912,'hello this working?',1,NULL),(1953795704484925440,1952670716730150912,'workingggg',1,NULL),(1953795718447763456,1952670716730150912,'yass',1,NULL),(1953795998732128256,1952670716730150912,'test',1,NULL),(1953796007909265408,1952670716730150912,'test2',1,NULL),(1953799395145289728,1952670716730150912,'hey',1,NULL),(1953799475034198016,1952670716730150912,'noice();',1,NULL),(1953799555430617088,1952670716730150912,'yes',1,NULL),(1953799621939695616,1952670716730150912,'its working',1,NULL),(1953799652428091392,1952670716730150912,'its working',1,NULL),(1953799672518807552,1952670716730150912,'its working',1,NULL),(1953800619131277312,1952670716730150912,'yas',1,NULL),(1953800651335143424,1952670716730150912,'yasssss',1,NULL),(1953800674865188864,1952670716730150912,'hye',1,NULL),(1953808116890079232,1952670716730150912,'abc',1,NULL),(1953808154546540544,1952670716730150912,'test',1,NULL),(1953808247190327296,1952670716730150912,'test',1,NULL),(1953808324847865856,1952670716730150912,'test',1,NULL),(1953808469828177920,1952670716730150912,'test',1,NULL),(1953808733842837504,1952670716730150912,'test',1,NULL),(1953808880714780672,1952670716730150912,'abc',1,NULL),(1953809169232564224,1952670716730150912,'hello',1,NULL),(1953809245912829952,1952670716730150912,'oh yes it works',1,NULL),(1953812263479676928,1952670716730150912,'hello',1,NULL),(1953812278369456128,1952670716730150912,'yess it works',1,NULL),(1953812467473846272,1952670716730150912,'yare yare',2,NULL),(1953812484074901504,1952670716730150912,'great',3,NULL),(1953812497354067968,1952670716730150912,'works',4,NULL),(1953812513456001024,1952670716730150912,'attention',5,NULL),(1953812526349291520,1952670716730150912,'bruh',1953786424625074176,NULL),(1953935586620477440,1952670716730150912,'hello',1,NULL),(1953935596305125376,1952670716730150912,'hey',1,NULL),(1953935606354677760,1952670716730150912,'works',1,NULL),(1953935618132283392,1952670716730150912,'bruh',1953780850386669568,NULL),(1953935652236169216,1952670716730150912,'omegalul',4,NULL);
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
INSERT INTO `chatusers` VALUES (1,'Krishiv',NULL,NULL,'XII-A',NULL),(2,'TestUser',NULL,NULL,'XII-A',NULL),(1952670716730150912,'ADMIN','$2b$12$GLNzXgFbYCicjXa8y2r8QunP5Hiud3/zoe5NAr5LdkvyAYcBvdCWK',511,NULL,NULL);
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
INSERT INTO `tokens` VALUES (1,'abc','2020-12-24',1),(1952674035137646592,'4d0b6cf2387d19f6ea17d68378f470e87b8b04ad5e678d43a2b074b56d8d2a9e3444ef78f89a47317db74af01eebce1f5e021bcbe8ab67e67dcb0c5b162c1902f949c82afd9abcc8b899b855321236b12fa3179d32d68d82325e82bfd151e93869d304b0b2d6bf5c817c09d7a54e63335ad770160a4403548b3fadc6861222d8','2021-01-21',1952670716730150912),(1979174730191736832,'4b45815f119e75306ca7377c76b1bc00dcf6164b38cebf3df68f339e8a56239735dded674a679fe33dd98f0c7ad9549d72b2f46ecb2428c8b3ef00751458d2244685a3312fdde9f0d92633c606cdd109bf1e432d945562bfe5bd23576d8925f4c19220c0613be7ebe8fc56a8ffceb9dd70526022820d8bd6f9e96273b0639856','2021-04-04',1952670716730150912);
/*!40000 ALTER TABLE `tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdetails`
--

DROP TABLE IF EXISTS `userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdetails` (
  `id` bigint DEFAULT NULL,
  `userid` bigint DEFAULT NULL,
  `data` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdetails`
--

LOCK TABLES `userdetails` WRITE;
/*!40000 ALTER TABLE `userdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `userdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `id` bigint DEFAULT NULL,
  `class` varchar(32) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `link` varchar(256) DEFAULT NULL,
  `path` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES (1,'a','abc','abc',''),(2,'b','def','abc','/folder1'),(3,'b','ghi','abc','/folder1'),(4,'b','jkl','abc','/folder2'),(5,'b','mno','abc','/folder1/folder2'),(6,'b','pqr','abc','/folder1/folder3'),(7,'b','stu','abc','/folder1/folder2'),(8,'b','vwz','abc','/folder1/folder2/folder3');
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-06 18:14:56
