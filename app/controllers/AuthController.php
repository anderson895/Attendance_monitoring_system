<?php
require_once ROOT_PATH . '/app/core/Controller.php';

class AuthController extends Controller {
    private $auth;

    public function __construct() {
        $this->auth = $this->model('Auth');
    }

    public function index() {
        $this->login();
    }

    public function login() {
        if ($this->auth->check()) {
            $this->redirect($_SESSION['role'] === 'admin' ? 'admin/dashboard' : 'user/dashboard');
        }
        $this->view('auth/login', ['title' => 'Login']);
    }

    public function register() {
        if ($this->auth->check()) {
            $this->redirect('user/dashboard');
        }
        $this->view('auth/register', ['title' => 'Register']);
    }

    // ---- AJAX endpoints ----
    public function doLogin() {
        $this->requireAjax();
        $username = trim($this->input('username', ''));
        $password = $this->input('password', '');

        if ($username === '' || $password === '') {
            $this->json(['status' => 'error', 'message' => 'Please fill in all fields']);
        }
        $result = $this->auth->attempt($username, $password);
        if ($result['status'] === 'success') {
            $result['redirect'] = BASE_URL . $result['redirect'];
        }
        $this->json($result);
    }

    public function doRegister() {
        $this->requireAjax();
        $userModel = $this->model('User');

        $fullname = trim($this->input('fullname', ''));
        $username = trim($this->input('username', ''));
        $email    = trim($this->input('email', ''));
        $password = $this->input('password', '');
        $confirm  = $this->input('confirm_password', '');

        if ($fullname === '' || $username === '' || $email === '' || $password === '') {
            $this->json(['status' => 'error', 'message' => 'All fields are required']);
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $this->json(['status' => 'error', 'message' => 'Invalid email address']);
        }
        if (strlen($password) < 6) {
            $this->json(['status' => 'error', 'message' => 'Password must be at least 6 characters']);
        }
        if ($password !== $confirm) {
            $this->json(['status' => 'error', 'message' => 'Passwords do not match']);
        }
        if ($userModel->usernameExists($username)) {
            $this->json(['status' => 'error', 'message' => 'Username already taken']);
        }
        if ($userModel->emailExists($email)) {
            $this->json(['status' => 'error', 'message' => 'Email already registered']);
        }

        $userModel->setFullname($fullname)
                  ->setUsername($username)
                  ->setEmail($email)
                  ->setPassword($password)
                  ->setRole('user')
                  ->setStatus('active');

        if ($userModel->create()) {
            $this->json(['status' => 'success', 'message' => 'Account created. You may now log in.']);
        }
        $this->json(['status' => 'error', 'message' => 'Failed to create account']);
    }

    public function logout() {
        $this->auth->logout();
        $this->redirect('auth/login');
    }
}
