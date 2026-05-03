<?php
/**
 * Global configuration constants.
 * BASE_URL is auto-detected so the app works in any subfolder under XAMPP.
 */
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'attendance_monitoring_system');

$scriptDir = str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME']));
$scriptDir = rtrim($scriptDir, '/');
define('BASE_URL', ($scriptDir === '' ? '/' : $scriptDir . '/'));
define('ROOT_PATH', dirname(__DIR__, 1));

date_default_timezone_set('Asia/Manila');

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
