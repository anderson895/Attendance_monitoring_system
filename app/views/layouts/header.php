<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($title ?? 'Attendance Monitoring System') ?></title>
    <link rel="stylesheet" href="<?= BASE_URL ?>assets/css/style.css">
    <script>window.BASE_URL = '<?= BASE_URL ?>';</script>
</head>
<body>
<div class="app">
    <aside class="sidebar">
        <div class="brand">
            ATTENDANCE
            <small><?= ucfirst($_SESSION['role'] ?? '') ?> Panel</small>
        </div>
        <nav>
            <?php
                $current = $_GET['url'] ?? '';
                $isAdmin = ($_SESSION['role'] ?? '') === 'admin';
                $links = $isAdmin ? [
                    'admin/dashboard'  => 'Dashboard',
                    'admin/users'      => 'Users',
                    'admin/attendance' => 'Attendance Records'
                ] : [
                    'user/dashboard'  => 'Dashboard',
                    'user/attendance' => 'My Attendance',
                    'user/profile'    => 'Profile'
                ];
                foreach ($links as $href => $label) {
                    $active = strpos($current, $href) === 0 ? 'active' : '';
                    echo '<a class="' . $active . '" href="' . BASE_URL . $href . '">' . $label . '</a>';
                }
            ?>
            <a href="<?= BASE_URL ?>auth/logout">Logout</a>
        </nav>
    </aside>
    <div class="main">
        <div class="topbar">
            <h2><?= htmlspecialchars($title ?? '') ?></h2>
            <div class="user-box">
                <div class="avatar"><?= strtoupper(substr($_SESSION['fullname'] ?? '?', 0, 1)) ?></div>
                <div>
                    <strong><?= htmlspecialchars($_SESSION['fullname'] ?? '') ?></strong><br>
                    <small class="text-muted">@<?= htmlspecialchars($_SESSION['username'] ?? '') ?></small>
                </div>
            </div>
        </div>
        <div class="content">
