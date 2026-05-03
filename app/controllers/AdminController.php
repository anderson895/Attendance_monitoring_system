<?php
require_once 'app/core/Controller.php';

class AdminController extends Controller {

    public function __construct() {
        $this->requireAdmin();
    }

    public function index() {
        $this->dashboard();
    }

    public function dashboard() {
        $this->view('admin/dashboard', ['title' => 'Admin Dashboard']);
    }

    public function dashboardStats() {
        $this->requireAjax();
        $userModel = $this->model('User');
        $attModel  = $this->model('Attendance');
        $recent    = array_slice($attModel->getAllRecords(), 0, 8);
        $this->json([
            'status' => 'success',
            'data' => [
                'totalUsers' => $userModel->countUsers(),
                'today'      => $attModel->getTodayStats(),
                'stats'      => $attModel->getStats(),
                'recent'     => $recent
            ]
        ]);
    }

    public function users() {
        $this->view('admin/users', ['title' => 'Manage Users']);
    }

    public function attendance() {
        $this->view('admin/attendance', ['title' => 'Attendance Records']);
    }

    public function settings() {
        $this->view('admin/settings', ['title' => 'System Settings']);
    }

    public function getSettings() {
        $this->requireAjax();
        $settingModel = $this->model('Setting');
        $this->json(['status' => 'success', 'data' => $settingModel->getAll()]);
    }

    public function saveSettings() {
        $this->requireAjax();
        $settingModel = $this->model('Setting');

        $workStart = $this->input('work_start_time', '09:00');
        $workEnd   = $this->input('work_end_time', '17:00');
        $grace     = (int)$this->input('late_grace_minutes', 0);
        $company   = trim($this->input('company_name', ''));

        // Normalize HH:MM into HH:MM:SS
        if (preg_match('/^\d{2}:\d{2}$/', $workStart)) { $workStart .= ':00'; }
        if (preg_match('/^\d{2}:\d{2}$/', $workEnd))   { $workEnd   .= ':00'; }

        if (!preg_match('/^\d{2}:\d{2}:\d{2}$/', $workStart)) {
            $this->json(['status' => 'error', 'message' => 'Invalid work start time format']);
        }
        if (!preg_match('/^\d{2}:\d{2}:\d{2}$/', $workEnd)) {
            $this->json(['status' => 'error', 'message' => 'Invalid work end time format']);
        }
        if (strtotime($workEnd) <= strtotime($workStart)) {
            $this->json(['status' => 'error', 'message' => 'End time must be after start time']);
        }
        if ($grace < 0 || $grace > 240) {
            $this->json(['status' => 'error', 'message' => 'Grace period must be 0–240 minutes']);
        }
        if ($company === '') {
            $this->json(['status' => 'error', 'message' => 'Company name is required']);
        }

        $settingModel->set('work_start_time', $workStart);
        $settingModel->set('work_end_time', $workEnd);
        $settingModel->set('late_grace_minutes', (string)$grace);
        $settingModel->set('company_name', $company);

        $this->json(['status' => 'success', 'message' => 'Settings saved']);
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
