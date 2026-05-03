<?php
require_once 'app/core/Controller.php';

class HomeController extends Controller {
    public function index() {
        if (isset($_SESSION['user_id'])) {
            $this->redirect($_SESSION['role'] === 'admin' ? 'admin/dashboard' : 'user/dashboard');
        }
        $this->redirect('auth/login');
    }

    public function companyName() {
        $this->requireAjax();
        $settingModel = $this->model('Setting');
        $name = $settingModel->get('company_name', 'My Company');
        $this->json(['status' => 'success', 'data' => ['company_name' => $name]]);
    }
}
