<?php
require_once ROOT_PATH . '/app/core/Controller.php';

class AdminController extends Controller {

    public function __construct() {
        $this->requireAdmin();
    }

    public function index() {
        $this->dashboard();
    }

    public function dashboard() {
        $userModel = $this->model('User');
        $attModel = $this->model('Attendance');
        $data = [
            'title' => 'Admin Dashboard',
            'totalUsers' => $userModel->countUsers(),
            'today' => $attModel->getTodayStats(),
            'stats' => $attModel->getStats(),
            'recent' => array_slice($attModel->getAllRecords(), 0, 8)
        ];
        $this->view('admin/dashboard', $data);
    }

    public function users() {
        $this->view('admin/users', ['title' => 'Manage Users']);
    }

    public function attendance() {
        $userModel = $this->model('User');
        $this->view('admin/attendance', [
            'title' => 'Attendance Records',
            'users' => $userModel->getAll()
        ]);
    }

    // ---- AJAX: list users ----
    public function listUsers() {
        $this->requireAjax();
        $userModel = $this->model('User');
        $this->json(['status' => 'success', 'data' => $userModel->getAll()]);
    }

    public function getUser() {
        $this->requireAjax();
        $id = (int)$this->input('id');
        $userModel = $this->model('User');
        $user = $userModel->findById($id);
        if (!$user) {
            $this->json(['status' => 'error', 'message' => 'User not found']);
        }
        unset($user['password']);
        $this->json(['status' => 'success', 'data' => $user]);
    }

    public function saveUser() {
        $this->requireAjax();
        $userModel = $this->model('User');

        $id       = (int)$this->input('id', 0);
        $fullname = trim($this->input('fullname', ''));
        $username = trim($this->input('username', ''));
        $email    = trim($this->input('email', ''));
        $password = $this->input('password', '');
        $role     = $this->input('role', 'user');
        $status   = $this->input('status', 'active');

        if ($fullname === '' || $username === '' || $email === '') {
            $this->json(['status' => 'error', 'message' => 'Fullname, username and email are required']);
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $this->json(['status' => 'error', 'message' => 'Invalid email address']);
        }
        if ($id === 0 && strlen($password) < 6) {
            $this->json(['status' => 'error', 'message' => 'Password must be at least 6 characters']);
        }
        if ($userModel->usernameExists($username, $id)) {
            $this->json(['status' => 'error', 'message' => 'Username already taken']);
        }
        if ($userModel->emailExists($email, $id)) {
            $this->json(['status' => 'error', 'message' => 'Email already registered']);
        }

        $userModel->setFullname($fullname)
                  ->setUsername($username)
                  ->setEmail($email)
                  ->setRole($role)
                  ->setStatus($status);

        if (!empty($password)) {
            $userModel->setPassword($password);
        }

        if ($id > 0) {
            $userModel->setId($id);
            $ok = $userModel->update();
            $msg = $ok ? 'User updated' : 'Failed to update user';
        } else {
            $ok = $userModel->create();
            $msg = $ok ? 'User created' : 'Failed to create user';
        }
        $this->json(['status' => $ok ? 'success' : 'error', 'message' => $msg]);
    }

    public function deleteUser() {
        $this->requireAjax();
        $id = (int)$this->input('id');
        if ($id === (int)$_SESSION['user_id']) {
            $this->json(['status' => 'error', 'message' => 'You cannot delete your own account']);
        }
        $userModel = $this->model('User');
        $ok = $userModel->delete($id);
        $this->json([
            'status' => $ok ? 'success' : 'error',
            'message' => $ok ? 'User deleted' : 'Failed to delete user'
        ]);
    }

    // ---- AJAX: list attendance ----
    public function listAttendance() {
        $this->requireAjax();
        $attModel = $this->model('Attendance');
        $filters = [
            'date_from' => $this->input('date_from'),
            'date_to'   => $this->input('date_to'),
            'user_id'   => $this->input('user_id'),
            'status'    => $this->input('status')
        ];
        $rows = $attModel->getAllRecords($filters);
        foreach ($rows as &$r) {
            $r['duration'] = Attendance::calcDuration($r['time_in'], $r['time_out']);
        }
        $this->json(['status' => 'success', 'data' => $rows]);
    }

    public function deleteAttendance() {
        $this->requireAjax();
        $id = (int)$this->input('id');
        $attModel = $this->model('Attendance');
        $ok = $attModel->delete($id);
        $this->json([
            'status' => $ok ? 'success' : 'error',
            'message' => $ok ? 'Record deleted' : 'Failed to delete'
        ]);
    }
}
