-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2024 at 05:33 PM
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
-- Database: `mj`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `a_id` int(11) NOT NULL,
  `a_student_id` int(11) NOT NULL,
  `a_status` varchar(60) NOT NULL,
  `a_reason` text DEFAULT NULL,
  `a_date` date NOT NULL,
  `a_approval` varchar(60) DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`a_id`, `a_student_id`, `a_status`, `a_reason`, `a_date`, `a_approval`) VALUES
(13, 1, 'Present', NULL, '2024-11-22', 'Pending'),
(14, 1, 'Present', NULL, '2024-11-21', 'Pending'),
(15, 1, 'Present', NULL, '2024-11-20', 'Pending'),
(16, 3, 'Absent', 'awdawdawd', '2024-11-22', 'Pending'),
(17, 1, 'Absent', 'I have a sick', '2024-11-23', 'Pending'),
(18, 3, 'Present', NULL, '2024-11-23', 'Approved'),
(19, 6, 'Present', NULL, '2024-11-23', 'Pending'),
(20, 3, 'Present', NULL, '2024-11-24', 'Approved'),
(21, 1, 'Absent', 'may lagnat', '2024-11-24', 'Declined'),
(22, 25, 'Present', NULL, '2024-11-24', 'Approved'),
(23, 27, 'Absent', 'may trangkaso', '2024-10-24', 'Pending'),
(24, 27, 'Present', NULL, '2024-11-24', 'Approved'),
(25, 27, 'Present', NULL, '2024-11-27', 'Approved'),
(26, 28, 'Present', NULL, '2024-12-05', 'Approved'),
(27, 8, 'Absent', 'fever', '2024-12-06', 'Declined');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(60) NOT NULL,
  `mname` varchar(60) DEFAULT NULL,
  `lname` varchar(60) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` enum('Student','Instructor') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `mname`, `lname`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'Gabi', '', 'Ackerman', 'student', 'student', 'Student', '2024-11-23 12:20:38'),
(2, 'Joshua', 'Anderson', 'Padilla', 'andy', 'andy', 'Instructor', '2024-11-23 05:25:26'),
(3, 'April', 'Jane', 'De Leon', 'april', 'april', 'Student', '2024-11-23 02:29:50'),
(4, 'juan', 'list', 'time', 'onepeace', '', 'Student', '2024-11-23 15:15:36'),
(5, 'test', 'testt', 'test', 'test', '', 'Student', '2024-11-23 15:20:31'),
(6, 'angela', 'denise', 'flores', 'angenise24', 'angenise24', 'Student', '2024-11-23 15:28:55'),
(8, 'joshua', 'anderson', 'padilla', 'joshua', 'joshua', 'Student', '2024-11-23 16:05:47'),
(9, 'justin', 'justin', 'justin', 'justin', 'justin', 'Student', '2024-11-23 16:08:15'),
(10, 'sample', 'sample', 'sample', 'sample', 'sample', 'Student', '2024-11-23 16:11:38'),
(21, 'juan1', NULL, 'juanjuan', 'juan', 'juan', 'Student', '2024-11-24 04:29:03'),
(22, 'QWERT', 'QWERT', 'QWERT', 'QWERT', 'QWERT', 'Student', '2024-11-24 04:01:48'),
(25, 'pasko', 'pasko', 'pasko', 'pasko', 'pasko', 'Student', '2024-11-24 04:18:08'),
(27, 'eudora', NULL, 'alucard', 'eudora', 'eudora', 'Student', '2024-11-24 14:01:04'),
(28, 'pedro', 's', 'padilla', 'pedro', 'pedro', 'Student', '2024-12-05 07:35:07'),
(29, 'anthony', NULL, 'racal', 'anthony', 'jennings', 'Student', '2024-12-05 16:30:31');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`a_id`),
  ADD KEY `a_student_id` (`a_student_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `a_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`a_student_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
