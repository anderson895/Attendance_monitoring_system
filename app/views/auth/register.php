<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="pageTitle">Register</title>
    <link rel="stylesheet" href="<?= BASE_URL ?>assets/css/style.css">
    <script>window.BASE_URL = '<?= BASE_URL ?>';</script>
</head>
<body>
<div class="auth-wrapper">
    <div class="auth-card">
        <h1>Create your <span id="brandName">My Company</span> account</h1>
        <p class="subtitle">Register a new user account</p>

        <form id="registerForm">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" name="fullname" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" class="form-control" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>Confirm Password</label>
                    <input type="password" name="confirm_password" class="form-control" required>
                </div>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Create Account</button>
        </form>

        <p class="switch-link">
            Already have an account? <a href="<?= BASE_URL ?>auth/login">Sign In</a>
        </p>
    </div>
</div>
<div class="toast-stack"></div>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="<?= BASE_URL ?>assets/js/app.js"></script>
</body>
</html>
