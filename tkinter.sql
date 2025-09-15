-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 04 juin 2024 à 00:40
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `tkinter1`
--

-- --------------------------------------------------------

--
-- Structure de la table `category`
--

CREATE TABLE `category` (
  `Id_category` int(11) UNSIGNED NOT NULL,
  `Nom_category` varchar(30) NOT NULL,
  `description_cat` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `category`
--

INSERT INTO `category` (`Id_category`, `Nom_category`, `description_cat`) VALUES
(13, 'vetement1', 'tout ce qui concerene les vetement'),
(14, 'nourriture', 'Tout ce qui concerne les nourriture'),
(15, 'fruits de mer', 'Tout ce qui concerne les fruits de mer'),
(16, 'boissons', 'Tout ce qui concerne les  boissons'),
(17, 'legumes', 'Tout ce qui concerne les  legumes'),
(18, 'fruits', 'Tout ce qui concerne les  fruits'),
(19, 'sports', 'Tout ce qui concerne les  sports'),
(25, 'siham4', 'jkwdwf');

-- --------------------------------------------------------

--
-- Structure de la table `detailsfacture`
--

CREATE TABLE `detailsfacture` (
  `id_detail` int(11) NOT NULL,
  `category` varchar(200) NOT NULL,
  `produits` varchar(200) NOT NULL,
  `stock` int(255) NOT NULL,
  `prix` int(255) NOT NULL,
  `id_facture` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `detailsfacture`
--

INSERT INTO `detailsfacture` (`id_detail`, `category`, `produits`, `stock`, `prix`, `id_facture`) VALUES
(7, 'fruits de mer', 'crustace', 1, 20, 25),
(10, 'fruits', 'poire', 1, 10, 26),
(11, 'fruits', 'pomme', 1, 10, 26),
(13, 'fruits de mer', 'poisson', 1, 20, 29),
(14, 'fruits', 'banan', 1, 10, 30),
(15, 'boissons', 'CocaCola', 2, 4, 30),
(16, 'nourriture', 'tacos', 1, 30, 30),
(17, 'vetement1', 'chemis', 1, 500, 30),
(18, 'fruits', 'poire', 1, 10, 31),
(19, 'fruits', 'geler', 2, 10, 31),
(20, 'boissons', 'Hawai', 3, 5, 31),
(21, 'sports', 'ballon baseball', 1, 300, 31),
(22, 'fruits', 'poire', 1, 10, 32),
(23, 'legumes', 'pommes de terre', 1, 3, 33),
(24, 'nourriture', 'salade', 1, 60, 33),
(25, 'legumes', 'carotte', 2, 3, 34),
(26, 'fruits', 'banan', 2, 10, 34),
(27, 'legumes', 'oignon', 1, 3, 35),
(28, 'fruits', 'poire', 1, 10, 36),
(29, 'legumes', 'pommes de terre', 1, 3, 36);

-- --------------------------------------------------------

--
-- Structure de la table `facture`
--

CREATE TABLE `facture` (
  `id_facture` int(11) NOT NULL,
  `date_facture` datetime NOT NULL DEFAULT current_timestamp(),
  `total` int(200) NOT NULL,
  `id_employer` int(200) NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `facture`
--

INSERT INTO `facture` (`id_facture`, `date_facture`, `total`, `id_employer`, `username`) VALUES
(25, '2024-05-24 19:16:22', 20, 57, 'sin '),
(26, '2024-05-25 12:44:12', 20, 57, 'sin '),
(29, '2024-05-26 02:08:29', 20, 57, 'sin '),
(30, '2024-05-26 02:09:02', 548, 57, 'sin '),
(31, '2024-05-26 02:11:16', 345, 57, 'sin '),
(32, '2024-05-26 02:17:58', 10, 59, 'rouaki'),
(33, '2024-05-26 19:48:09', 63, 59, 'rouaki'),
(34, '2024-05-27 17:55:02', 26, 73, 'mehdi'),
(35, '2024-05-27 17:57:31', 3, 73, 'mehdi'),
(36, '2024-05-28 00:18:12', 13, 52, '1');

-- --------------------------------------------------------

--
-- Structure de la table `inscription`
--

CREATE TABLE `inscription` (
  `id_employer` int(11) NOT NULL,
  `Email` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` int(15) NOT NULL,
  `genre` varchar(6) NOT NULL,
  `dateE` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `inscription`
--

INSERT INTO `inscription` (`id_employer`, `Email`, `username`, `password`, `genre`, `dateE`) VALUES
(52, '1', '1', 1, 'User', '22:10:52'),
(75, '12', 'mohsine3', 123, 'Admin', '00:05:08'),
(66, '7tyuy', 'sin', 123, 'Admin', '23:54:32'),
(68, 'adnan.ma', 'adnan', 123, 'Admin', '11:16:13'),
(81, 'ali', 'mohsin', 1, 'User', '01:52:55'),
(61, 'gsyfgsuif', 'dyfdeufgewf', 123, 'Admin', '20:44:27'),
(51, 'khalid@gmail.com', 'khalid', 123, 'Admin', '13:53:49'),
(67, 'ljiuhvghhhhh', 'ngv', 423094897, 'User', '01:03:16'),
(73, 'mehdi@gmail.com', 'mehdi', 123, 'User', '17:52:01'),
(49, 'mm@gmail.com', 'mohsin1', 122, 'User', '11:55:28'),
(57, 'moh1', 'sin ', 123, 'Admin', '09:40:37'),
(65, 'moh123', 'moh', 123, 'User', '23:39:21'),
(59, 'mohsin3@gmail.com', 'rouaki', 123, 'User', '12:11:03'),
(48, 'mohsin@gmail.com', 'rouaki', 123, 'Admin', '17:50:52'),
(62, 'mohsinrouaki@gmail.c', 'mohsin', 432, 'User', '23:37:55'),
(43, 'mouhsineR@gmail.com', 'mouhsine rouaki', 123, 'User', '23:38:30'),
(60, 'oefhwefd', 'fruyfr', 123, 'Admin', '20:42:06'),
(54, 'osama1@gmail.com', 'osama1', 123, 'User', '23:20:39'),
(53, 'osama@gmail.com', 'osama', 123, 'User', '23:47:36'),
(42, 'rouaki@gmail.com', 'mohsin', 123, 'Admin', '23:35:52'),
(40, 'siham@gmail.com', 'siham', 123, 'User', '17:40:59'),
(69, 'uigyf', 'ui7yutr', 123, 'User', '17:39:28'),
(36, 'yassin@gmail.com', 'yassin', 123, 'User', '17:34:06');

-- --------------------------------------------------------

--
-- Structure de la table `product`
--

CREATE TABLE `product` (
  `ID_product` int(11) NOT NULL,
  `Nom_product` varchar(20) NOT NULL,
  `Nom_category` varchar(30) NOT NULL,
  `stock` int(40) NOT NULL,
  `prix` int(50) NOT NULL,
  `date` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `product`
--

INSERT INTO `product` (`ID_product`, `Nom_product`, `Nom_category`, `stock`, `prix`, `date`) VALUES
(1, 'pepsi', 'boissons', 194, 4, '17:03:17'),
(2, 'CocaCola', 'boissons', 84, 4, '17:03:59'),
(3, 'Hawai', 'boissons', 95, 5, '17:04:29'),
(4, 'banan', 'fruits', 81, 10, '17:04:53'),
(5, 'orange', 'fruits', 0, 10, '17:05:13'),
(6, 'pomme', 'fruits', 79, 10, '17:06:12'),
(7, 'poire', 'fruits', 84, 10, '17:06:44'),
(8, 'geler', 'fruits', 92, 10, '17:07:33'),
(9, 'poisson', 'fruits de mer', 181, 20, '17:09:29'),
(10, 'mollusque', 'fruits de mer', 154, 20, '17:09:49'),
(11, 'crustace', 'fruits de mer', 172, 20, '17:10:15'),
(12, 'carotte', 'legumes', 94, 3, '17:10:57'),
(13, 'pommes de terre', 'legumes', 75, 3, '17:11:14'),
(14, 'tommate', 'legumes', 0, 3, '17:11:35'),
(15, 'oignon', 'legumes', 90, 3, '17:12:29'),
(16, 'pizza', 'nourriture', 99, 30, '17:13:13'),
(17, 'tacos', 'nourriture', 95, 30, '17:13:24'),
(18, 'suchi', 'nourriture', 91, 80, '17:13:43'),
(19, 'salade', 'nourriture', 96, 60, '17:14:21'),
(20, 'ballon football', 'sports', 100, 300, '17:15:41'),
(21, 'ballon bascket', 'sports', 97, 300, '17:15:51'),
(22, 'ballon baseball', 'sports', 97, 300, '17:16:11'),
(23, 'ballon tennis', 'sports', 98, 200, '17:16:24'),
(24, 'chemis', 'vetement1', 99, 500, '17:16:57'),
(25, 'pantalons', 'vetement1', 200, 500, '17:17:08'),
(26, 'robes', 'vetement1', 500, 100, '17:17:25'),
(27, 'chaussure', 'vetement1', 500, 100, '17:17:44'),
(28, 'chapeaux', 'vetement1', 100, 100, '17:18:05'),
(29, 'accessoire', 'vetement1', 49, 100, '17:18:25');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`Id_category`) USING BTREE,
  ADD KEY `Nom_category` (`Nom_category`);

--
-- Index pour la table `detailsfacture`
--
ALTER TABLE `detailsfacture`
  ADD PRIMARY KEY (`id_detail`),
  ADD KEY `id_facture` (`id_facture`);

--
-- Index pour la table `facture`
--
ALTER TABLE `facture`
  ADD PRIMARY KEY (`id_facture`),
  ADD KEY `id_employer` (`id_employer`),
  ADD KEY `id_facture` (`id_facture`),
  ADD KEY `username` (`username`);

--
-- Index pour la table `inscription`
--
ALTER TABLE `inscription`
  ADD PRIMARY KEY (`Email`),
  ADD KEY `username` (`username`),
  ADD KEY `password` (`password`),
  ADD KEY `genre` (`genre`),
  ADD KEY `id_employer` (`id_employer`),
  ADD KEY `dateE` (`dateE`);

--
-- Index pour la table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`ID_product`),
  ADD KEY `category` (`Nom_category`),
  ADD KEY `Nom_product` (`Nom_product`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `category`
--
ALTER TABLE `category`
  MODIFY `Id_category` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT pour la table `detailsfacture`
--
ALTER TABLE `detailsfacture`
  MODIFY `id_detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT pour la table `facture`
--
ALTER TABLE `facture`
  MODIFY `id_facture` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT pour la table `inscription`
--
ALTER TABLE `inscription`
  MODIFY `id_employer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- AUTO_INCREMENT pour la table `product`
--
ALTER TABLE `product`
  MODIFY `ID_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `detailsfacture`
--
ALTER TABLE `detailsfacture`
  ADD CONSTRAINT `fk_facture1` FOREIGN KEY (`id_facture`) REFERENCES `facture` (`id_facture`);

--
-- Contraintes pour la table `facture`
--
ALTER TABLE `facture`
  ADD CONSTRAINT `fk_facture` FOREIGN KEY (`id_employer`) REFERENCES `inscription` (`id_employer`),
  ADD CONSTRAINT `fk_factureusername` FOREIGN KEY (`username`) REFERENCES `inscription` (`username`);

--
-- Contraintes pour la table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `fk_id_Ncat` FOREIGN KEY (`Nom_category`) REFERENCES `category` (`Nom_category`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
