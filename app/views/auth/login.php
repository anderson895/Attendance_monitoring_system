<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — Attendance Monitoring System</title>
    <link rel="stylesheet" href="<?= BASE_URL ?>assets/css/style.css">
    <script>window.BASE_URL = '<?= BASE_URL ?>';</script>
</head>
<body>
<div class="auth-wrapper">
    <div class="auth-card">
        <h1>Welcome Back</h1>
        <p class="subtitle">Sign in to your account</p>

        <form id="loginForm">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" class="form-control" required autofocus>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Sign In</button>
        </form>

        <p class="switch-link">
            Don't have an account? <a href="<?= BASE_URL ?>auth/register">Register</a>
        </p>
    </div>
</div>
<div class="toast-stack"></div>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="<?= BASE_URL ?>assets/js/app.js"></script>
</body>
</html>
