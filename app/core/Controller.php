<?php
/**
 * Base Controller.
 * Provides shared helpers: model loading, view rendering, JSON response,
 * and access control checks.
 */
class Controller {

    protected function model($name) {
        $path = ROOT_PATH . '/app/models/' . $name . '.php';
        if (!file_exists($path)) {
            throw new Exception("Model {$name} not found");
        }
        require_once $path;
        return new $name();
    }

    protected function view($view, $data = []) {
        $path = ROOT_PATH . '/app/views/' . $view . '.php';
        if (!file_exists($path)) {
            throw new Exception("View {$view} not found");
        }
        extract($data);
        require_once $path;
    }

    protected function json($data) {
        header('Content-Type: application/json');
        echo json_encode($data);
        exit;
    }

    protected function redirect($path) {
        header('Location: ' . BASE_URL . ltrim($path, '/'));
        exit;
    }

    protected function requireLogin() {
        if (!isset($_SESSION['user_id'])) {
            $this->redirect('auth/login');
        }
    }

    protected function requireAdmin() {
        $this->requireLogin();
        if ($_SESSION['role'] !== 'admin') {
            $this->redirect('user/dashboard');
        }
    }

    protected function requireAjax() {
        if (strtolower($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') !== 'xmlhttprequest') {
            http_response_code(403);
            $this->json(['status' => 'error', 'message' => 'AJAX requests only']);
        }
    }

    protected function input($key, $default = null) {
        return $_POST[$key] ?? $_GET[$key] ?? $default;
    }
}
