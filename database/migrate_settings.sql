-- =====================================================================
-- Migration: add settings table (run this if you already installed earlier)
-- =====================================================================
USE `attendance_monitoring_system`;

CREATE TABLE IF NOT EXISTS `settings` (
    `setting_key`   VARCHAR(64) NOT NULL PRIMARY KEY,
    `setting_value` VARCHAR(255) NOT NULL,
    `updated_at`    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO `settings` (`setting_key`, `setting_value`) VALUES
('work_start_time',    '09:00:00'),
('work_end_time',      '17:00:00'),
('late_grace_minutes', '0'),
('company_name',       'My Company');

-- For users that already ran the earlier migration without work_end_time:
INSERT INTO `settings` (`setting_key`, `setting_value`)
VALUES ('work_end_time', '17:00:00')
ON DUPLICATE KEY UPDATE setting_value = setting_value;
