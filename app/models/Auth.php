<?php
require_once ROOT_PATH . '/app/models/User.php';

/**
 * Auth service. Encapsulates session-based authentication.
 * Composes User (HAS-A) rather than inheriting it.
 */
class Auth {
    private $userModel;

    public function __construct() {
        $this->userModel = new User();
    }

    public function attempt($username, $password) {
        $row = $this->userModel->findByUsername($username);
        if (!$row) {
            return ['status' => 'error', 'message' => 'Invalid username or password'];
        }
        if ($row['status'] === 'inactive') {
            return ['status' => 'error', 'message' => 'Your account is inactive. Contact admin.'];
        }
        if (!password_verify($password, $row['password'])) {
            return ['status' => 'error', 'message' => 'Invalid username or password'];
        }
        $_SESSION['user_id'] = $row['id'];
        $_SESSION['username'] = $row['username'];
        $_SESSION['fullname'] = $row['fullname'];
        $_SESSION['role'] = $row['role'];
        return [
            'status' => 'success',
            'message' => 'Welcome, ' . $row['fullname'],
            'redirect' => $row['role'] === 'admin' ? 'admin/dashboard' : 'user/dashboard'
        ];
    }

    public function logout() {
        $_SESSION = [];
        if (ini_get('session.use_cookies')) {
            $p = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000, $p['path'], $p['domain'], $p['secure'], $p['httponly']);
        }
        session_destroy();
    }

    public function check() { return isset($_SESSION['user_id']); }
    public function isAdmin() { return $this->check() && $_SESSION['role'] === 'admin'; }
    public function id() { return $_SESSION['user_id'] ?? null; }
}
