-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2025 at 02:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `penitipan_barang`
--

-- --------------------------------------------------------

--
-- Table structure for table `barang`
--

CREATE TABLE `barang` (
  `id_pemilik` int(11) NOT NULL,
  `nama_pemilik` varchar(255) NOT NULL,
  `nama_barang` varchar(255) NOT NULL,
  `jenis_barang` enum('Barang Belanjaan','Barang Pribadi','','') NOT NULL,
  `waktu_dititip` datetime NOT NULL,
  `foto_barang` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang`
--

INSERT INTO `barang` (`id_pemilik`, `nama_pemilik`, `nama_barang`, `jenis_barang`, `waktu_dititip`, `foto_barang`) VALUES
(82, 'aryazzz', 'gelangzzz', 'Barang Belanjaan', '2025-02-20 17:57:15', 'mulmed.jpg'),
(83, 'yoka', 'cincin', 'Barang Pribadi', '2025-02-20 17:58:20', 'animasi.jpg'),
(84, 'fayi', 'laptop', 'Barang Belanjaan', '2025-02-20 17:58:37', 'mulmed.jpg'),
(85, 'titi', 'kalung', 'Barang Pribadi', '2025-02-20 17:59:04', 'pronten.jpg'),
(86, 'dewi', 'baju', 'Barang Belanjaan', '2025-02-20 17:59:18', 'baner.jpg'),
(87, 'zetta', 'rambut', 'Barang Pribadi', '2025-02-20 17:59:33', 'uiux.jpg'),
(88, 'kobo', 'hiu', 'Barang Belanjaan', '2025-02-20 17:59:44', 'mulmed.jpg'),
(89, 'gojo', 'kacamata', 'Barang Belanjaan', '2025-02-20 18:00:00', 'mulmed.jpg'),
(90, 'anya', 'pita', 'Barang Pribadi', '2025-02-20 18:00:14', 'animasi.jpg'),
(91, 'damian', 'bunga', 'Barang Belanjaan', '2025-02-20 18:00:32', 'uiux.jpg'),
(92, 'sinta', 'buku', 'Barang Belanjaan', '2025-02-20 18:00:45', 'bran.jpg'),
(93, 'ferdinan', 'pensil', 'Barang Pribadi', '2025-02-20 18:01:08', 'baner.jpg'),
(94, 'pratama', 'HandPhone', 'Barang Pribadi', '2025-02-20 18:01:28', 'uiux.jpg'),
(96, 'Udin', 'Tas', 'Barang Pribadi', '2025-02-20 18:03:08', 'animasi.jpg'),
(97, 'gilang', 'Tas', 'Barang Pribadi', '2025-02-20 18:03:33', 'uiux.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id_pemilik`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barang`
--
ALTER TABLE `barang`
  MODIFY `id_pemilik` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
