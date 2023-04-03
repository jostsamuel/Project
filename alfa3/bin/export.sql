/* Autor: Jošt Samuel
/* Nazev: Databazova aplikace pro obchod


-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: obchod
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `customerorders`
--

DROP TABLE IF EXISTS `customerorders`;
/*!50001 DROP VIEW IF EXISTS `customerorders`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `customerorders` AS SELECT 
 1 AS `CustomerName`,
 1 AS `OrderID`,
 1 AS `DateTime_OrderPlaced`,
 1 AS `TotalAmount`,
 1 AS `Enum_PaymentMethod`,
 1 AS `Bool_Shipped`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Phone` varchar(255) NOT NULL,
  `Address` text NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitems`
--

DROP TABLE IF EXISTS `orderitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitems` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Quantity` int NOT NULL,
  `FK_ProductID` int NOT NULL,
  `FK_OrderID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_ProductID` (`FK_ProductID`),
  KEY `FK_OrderID` (`FK_OrderID`),
  CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`FK_ProductID`) REFERENCES `products` (`ID`),
  CONSTRAINT `orderitems_ibfk_2` FOREIGN KEY (`FK_OrderID`) REFERENCES `orders` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitems`
--

LOCK TABLES `orderitems` WRITE;
/*!40000 ALTER TABLE `orderitems` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `DateTime_OrderPlaced` datetime NOT NULL,
  `TotalAmount` float NOT NULL,
  `Enum_PaymentMethod` enum('CreditCard','PayPal','BankTransfer') NOT NULL,
  `Bool_Shipped` tinyint(1) NOT NULL,
  `FK_CustomerID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_CustomerID` (`FK_CustomerID`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`FK_CustomerID`) REFERENCES `customers` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `productreviews`
--

DROP TABLE IF EXISTS `productreviews`;
/*!50001 DROP VIEW IF EXISTS `productreviews`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `productreviews` AS SELECT 
 1 AS `ProductName`,
 1 AS `Description`,
 1 AS `Rating`,
 1 AS `DateTime_Submitted`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` text,
  `Price` float NOT NULL,
  `Quantity` int NOT NULL,
  `Enum_Category` enum('Electronics','Fashion','Home','Outdoors') NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Description` text NOT NULL,
  `Rating` float NOT NULL,
  `DateTime_Submitted` datetime NOT NULL,
  `FK_ProductID` int NOT NULL,
  `FK_CustomerID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_ProductID` (`FK_ProductID`),
  KEY `FK_CustomerID` (`FK_CustomerID`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`FK_ProductID`) REFERENCES `products` (`ID`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`FK_CustomerID`) REFERENCES `customers` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'obchod'
--

--
-- Dumping routines for database 'obchod'
--

--
-- Final view structure for view `customerorders`
--

/*!50001 DROP VIEW IF EXISTS `customerorders`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `customerorders` AS select concat(`customers`.`FirstName`,' ',`customers`.`LastName`) AS `CustomerName`,`orders`.`ID` AS `OrderID`,`orders`.`DateTime_OrderPlaced` AS `DateTime_OrderPlaced`,`orders`.`TotalAmount` AS `TotalAmount`,`orders`.`Enum_PaymentMethod` AS `Enum_PaymentMethod`,`orders`.`Bool_Shipped` AS `Bool_Shipped` from (`orders` join `customers` on((`orders`.`FK_CustomerID` = `customers`.`ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `productreviews`
--

/*!50001 DROP VIEW IF EXISTS `productreviews`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `productreviews` AS select `products`.`Name` AS `ProductName`,`reviews`.`Description` AS `Description`,`reviews`.`Rating` AS `Rating`,`reviews`.`DateTime_Submitted` AS `DateTime_Submitted` from (`reviews` join `products` on((`reviews`.`FK_ProductID` = `products`.`ID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-02 10:29:48
