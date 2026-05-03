<?php
/**
 * One-shot installer. Visit /attendance_monitoring_system/install.php once
 * to create the database, tables, and the default admin account.
 */
$host = 'localhost';
$user = 'root';
$pass = '';
$dbname = 'attendance_monitoring_system';

$conn = new mysqli($host, $user, $pass);
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error);
}

$messages = [];

if ($conn->query("CREATE DATABASE IF NOT EXISTS `$dbname` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")) {
    $messages[] = "Database <b>$dbname</b> ready.";
} else {
    die('Error creating database: ' . $conn->error);
}
$conn->select_db($dbname);

$users = "CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','user') NOT NULL DEFAULT 'user',
    status ENUM('active','inactive') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
if (!$conn->query($users)) die('Error: ' . $conn->error);
$messages[] = "Table <b>users</b> ready.";

$attendance = "CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    time_in DATETIME DEFAULT NULL,
    time_out DATETIME DEFAULT NULL,
    status ENUM('present','late','absent') NOT NULL DEFAULT 'present',
    remarks VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
if (!$conn->query($attendance)) die('Error: ' . $conn->error);
$messages[] = "Table <b>attendance</b> ready.";

$check = $conn->query("SELECT id FROM users WHERE username='admin'");
if ($check->num_rows === 0) {
    $hash = password_hash('admin123', PASSWORD_BCRYPT);
    $stmt = $conn->prepare("INSERT INTO users (fullname, username, email, password, role) VALUES (?, ?, ?, ?, 'admin')");
    $name = 'System Administrator';
    $uname = 'admin';
    $email = 'admin@example.com';
    $stmt->bind_param('ssss', $name, $uname, $email, $hash);
    $stmt->execute();
    $messages[] = "Default admin created &mdash; username: <b>admin</b>, password: <b>admin123</b>";
} else {
    $messages[] = "Admin account already exists.";
}

$check2 = $conn->query("SELECT id FROM users WHERE username='employee'");
if ($check2->num_rows === 0) {
    $hash = password_hash('employee123', PASSWORD_BCRYPT);
    $stmt = $conn->prepare("INSERT INTO users (fullname, username, email, password, role) VALUES (?, ?, ?, ?, 'user')");
    $name = 'Sample Employee';
    $uname = 'employee';
    $email = 'employee@example.com';
    $stmt->bind_param('ssss', $name, $uname, $email, $hash);
    $stmt->execute();
    $messages[] = "Sample employee created &mdash; username: <b>employee</b>, password: <b>employee123</b>";
}

$conn->close();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Install — Attendance Monitoring System</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<div class="auth-wrapper" style="background: linear-gradient(135deg,#16a34a,#0ea5e9);">
    <div class="auth-card" style="max-width:560px;">
        <h1>Installation Complete</h1>
        <p class="subtitle">All database tables and seed accounts are ready.</p>
        <ul style="padding-left:20px; line-height:2;">
            <?php foreach ($messages as $msg): ?>
                <li><?= $msg ?></li>
            <?php endforeach; ?>
        </ul>
        <div style="margin-top: 20px;">
            <a href="index.php" class="btn btn-primary btn-block">Go to Login</a>
        </div>
        <p class="switch-link" style="margin-top:18px;">
            <strong>Important:</strong> delete <code>install.php</code> after setup.
        </p>
    </div>
</div>
</body>
</html>
