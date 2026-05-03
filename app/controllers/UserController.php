<?php
require_once 'app/core/Controller.php';

class UserController extends Controller {

    public function __construct() {
        $this->requireLogin();
    }

    public function index() {
        $this->dashboard();
    }

    public function dashboard() {
        $attModel = $this->model('Attendance');
        $userId = (int)$_SESSION['user_id'];
        $data = [
            'title'  => 'My Dashboard',
            'today'  => $attModel->getTodayLog($userId),
            'stats'  => $attModel->getStats($userId),
            'recent' => array_slice($attModel->getUserHistory($userId), 0, 8)
        ];
        $this->view('user/dashboard', $data);
    }

    public function attendance() {
        $this->view('user/attendance', ['title' => 'My Attendance']);
    }

    public function profile() {
        $this->view('user/profile', ['title' => 'My Profile']);
    }

    public function myProfile() {
        $this->requireAjax();
        $userModel = $this->model('User');
        $me = $userModel->findById($_SESSION['user_id']);
        if ($me) { unset($me['password']); }
        $this->json(['status' => 'success', 'data' => $me]);
    }

    // ---- AJAX ----
    public function timeIn() {
        $this->requireAjax();
        $att = $this->model('Attendance');
        $this->json($att->timeIn((int)$_SESSION['user_id']));
    }

    public function timeOut() {
        $this->requireAjax();
        $att = $this->model('Attendance');
        $this->json($att->timeOut((int)$_SESSION['user_id']));
    }

    public function todayLog() {
        $this->requireAjax();
        $att = $this->model('Attendance');
        $userId = (int)$_SESSION['user_id'];
        $log = $att->getTodayLog($userId);
        $stats = $att->getStats($userId);
        $this->json([
            'status' => 'success',
            'data'   => $log,
            'stats'  => $stats
        ]);
    }

    public function history() {
        $this->requireAjax();
        $att = $this->model('Attendance');
        $rows = $att->getUserHistory((int)$_SESSION['user_id']);
        foreach ($rows as &$r) {
            $r['duration'] = Attendance::calcDuration($r['time_in'], $r['time_out']);
        }
        $this->json(['status' => 'success', 'data' => $rows]);
    }

    public function updateProfile() {
        $this->requireAjax();
        $userModel = $this->model('User');
        $id = (int)$_SESSION['user_id'];
        $current = $userModel->findById($id);
        if (!$current) {
            $this->json(['status' => 'error', 'message' => 'User not found']);
        }

        $fullname = trim($this->input('fullname', ''));
        $email    = trim($this->input('email', ''));
        $password = $this->input('password', '');

        if ($fullname === '' || $email === '') {
            $this->json(['status' => 'error', 'message' => 'Fullname and email are required']);
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $this->json(['status' => 'error', 'message' => 'Invalid email']);
        }
        if ($userModel->emailExists($email, $id)) {
            $this->json(['status' => 'error', 'message' => 'Email already in use']);
        }

        $userModel->setId($id)
                  ->setFullname($fullname)
                  ->setUsername($current['username'])
                  ->setEmail($email)
                  ->setRole($current['role'])
                  ->setStatus($current['status']);

        if (!empty($password)) {
            if (strlen($password) < 6) {
                $this->json(['status' => 'error', 'message' => 'Password must be at least 6 characters']);
            }
            $userModel->setPassword($password);
        }

        if ($userModel->update()) {
            $_SESSION['fullname'] = $fullname;
            $this->json(['status' => 'success', 'message' => 'Profile updated']);
        }
        $this->json(['status' => 'error', 'message' => 'Failed to update']);
    }
}
