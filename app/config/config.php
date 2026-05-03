<?php
/**
 * Global configuration constants.
 * BASE_URL is auto-detected so the app works in any subfolder under XAMPP.
 */
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'attendance_monitoring_system');

// Time-in cutoff. Anyone who times in after this is marked 'late'.
// Format: 'HH:MM:SS' (24-hour). Default 09:00:00 = 9 AM.
define('LATE_CUTOFF', '09:00:00');

$scriptDir = str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME']));
$scriptDir = rtrim($scriptDir, '/');
define('BASE_URL', ($scriptDir === '' ? '/' : $scriptDir . '/'));

date_default_timezone_set('Asia/Manila');

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
