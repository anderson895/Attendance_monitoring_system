<?php
require_once ROOT_PATH . '/app/core/Controller.php';

class HomeController extends Controller {
    public function index() {
        if (isset($_SESSION['user_id'])) {
            $this->redirect($_SESSION['role'] === 'admin' ? 'admin/dashboard' : 'user/dashboard');
        }
        $this->redirect('auth/login');
    }
}
