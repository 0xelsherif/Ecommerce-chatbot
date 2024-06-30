-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2024 at 08:19 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce_chatbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Apple', '2024-06-18 04:24:41', '2024-06-18 04:24:41'),
(2, 'Dell', '2024-06-18 04:24:41', '2024-06-18 04:24:41'),
(3, 'HP', '2024-06-18 04:24:41', '2024-06-18 04:24:41'),
(4, 'Lenovo', '2024-06-18 04:24:41', '2024-06-18 04:24:41');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `created_at`, `updated_at`) VALUES
(1, 'Laptops', '2024-06-18 04:24:41', '2024-06-18 04:24:41'),
(2, 'Desktops', '2024-06-18 04:24:41', '2024-06-18 04:24:41'),
(3, 'Accessories', '2024-06-18 04:24:41', '2024-06-18 04:24:41');

-- --------------------------------------------------------

--
-- Table structure for table `chat_logs`
--

CREATE TABLE `chat_logs` (
  `id` int(11) NOT NULL,
  `session_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `response` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock_quantity`, `category_id`, `brand_id`, `created_at`, `updated_at`) VALUES
(1, 'MacBook Pro', 'Apple MacBook Pro 16-inch', 2399.00, 10, 1, 1, '2024-06-18 04:26:10', '2024-06-18 04:26:10'),
(2, 'Dell XPS 13', 'Dell XPS 13-inch', 999.00, 20, 1, 2, '2024-06-18 04:26:10', '2024-06-18 04:26:10'),
(3, 'HP Spectre x360', 'HP Spectre x360 14-inch', 1199.00, 15, 1, 3, '2024-06-18 04:26:10', '2024-06-18 04:26:10'),
(4, 'Lenovo ThinkPad X1', 'Lenovo ThinkPad X1 Carbon', 1299.00, 8, 1, 4, '2024-06-18 04:26:10', '2024-06-18 06:26:57'),
(13, 'Apple iPad Pro', 'Apple iPad Pro 11-inch', 799.00, 25, 3, 1, '2024-06-18 06:25:56', '2024-06-18 06:25:56'),
(14, 'Dell Inspiron Desktop', 'Processor Intel® Core™ i5 14400 OS Windows 11 Pro Graphics Intel® UHD Graphics 730 Memory 16 GB DDR5 Storage 512 GB SSD.', 549.00, 15, 2, 2, '2024-06-18 06:25:56', '2024-06-25 09:50:37'),
(15, 'HP Pavilion Desktop', 'HP Pavilion Desktop with AMD Ryzen', 649.00, 20, 2, 3, '2024-06-18 06:25:56', '2024-06-18 06:25:56');

-- --------------------------------------------------------

--
-- Table structure for table `product_images`
--

CREATE TABLE `product_images` (
  `id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_images`
--

INSERT INTO `product_images` (`id`, `product_id`, `image_url`, `created_at`) VALUES
(10, 1, 'https://pngimg.com/uploads/macbook/macbook_PNG8.png', '2024-06-25 09:38:43'),
(11, 2, 'https://pngimg.com/uploads/laptop/laptop_PNG5933.png', '2024-06-25 09:38:43'),
(12, 3, 'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c08873717.png?impolicy=Png_Res', '2024-06-25 09:38:43'),
(13, 4, 'https://p1-ofp.static.pub/fes/cms/2022/03/17/pw5jy11vn8u0jbi3rdu3aq1ij4bl15411237.png', '2024-06-25 09:38:43'),
(14, 13, 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-model-select-gallery-2-202405?wid=5120&hei=2880&fmt=p-jpg&qlt=95&.v=1713495958277', '2024-06-25 09:38:43'),
(16, 15, 'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c06271217.png', '2024-06-25 09:38:43'),
(17, 14, 'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/desktops/inspiron-desktops/inspiron-3020/media-gallery/updated/desktop-inspiron-3020-no-odd-blue-gallery-2.psd?fmt=png-alpha&pscan=auto&scl=1&wid=2589&hei=3457&qlt', '2024-06-25 09:53:25');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chat_logs`
--
ALTER TABLE `chat_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_id` (`session_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `brand_id` (`brand_id`);

--
-- Indexes for table `product_images`
--
ALTER TABLE `product_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `chat_logs`
--
ALTER TABLE `chat_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=879;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `product_images`
--
ALTER TABLE `product_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
