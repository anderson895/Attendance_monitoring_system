-- =====================================================================
-- Attendance Monitoring System - Database Schema
-- =====================================================================
-- Import this file via phpMyAdmin or the MySQL CLI:
--   mysql -u root -p < attendance_monitoring_system.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `attendance_monitoring_system`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `attendance_monitoring_system`;

-- ---------------------------------------------------------------------
-- Table: users
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS `attendance`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
    `id`         INT AUTO_INCREMENT PRIMARY KEY,
    `fullname`   VARCHAR(100) NOT NULL,
    `username`   VARCHAR(50)  NOT NULL UNIQUE,
    `email`      VARCHAR(100) NOT NULL UNIQUE,
    `password`   VARCHAR(255) NOT NULL,
    `role`       ENUM('admin','user') NOT NULL DEFAULT 'user',
    `status`     ENUM('active','inactive') NOT NULL DEFAULT 'active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Table: attendance
-- ---------------------------------------------------------------------
CREATE TABLE `attendance` (
    `id`         INT AUTO_INCREMENT PRIMARY KEY,
    `user_id`    INT NOT NULL,
    `date`       DATE NOT NULL,
    `time_in`    DATETIME DEFAULT NULL,
    `time_out`   DATETIME DEFAULT NULL,
    `status`     ENUM('present','late','absent') NOT NULL DEFAULT 'present',
    `remarks`    VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `unique_user_date` (`user_id`, `date`),
    CONSTRAINT `fk_attendance_user`
        FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- Seed accounts
-- ---------------------------------------------------------------------
-- admin    / admin123
-- employee / employee123
-- (bcrypt hashes generated with PHP password_hash, PASSWORD_BCRYPT)
-- ---------------------------------------------------------------------
INSERT INTO `users` (`fullname`, `username`, `email`, `password`, `role`, `status`) VALUES
('System Administrator', 'admin',    'admin@example.com',
    '$2y$10$bU6q7fL.jRnU13NQtqQHeuzhGb5qc6zbCUlK68i/MmM2.GiOEzQWe', 'admin', 'active'),
('Sample Employee',      'employee', 'employee@example.com',
    '$2y$10$sBFvCK7Sx5lAf90zOPpJveXlbPk26gLI.YD./RHQVNKfzQFxlp5gy', 'user',  'active');
