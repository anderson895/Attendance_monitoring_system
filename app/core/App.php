<?php
/**
 * Front Controller / Router.
 * Parses the URL into Controller / Method / Params and dispatches.
 * Default route: home/index
 */
class App {
    private $controller = 'HomeController';
    private $method = 'index';
    private $params = [];

    public function __construct() {
        $url = $this->parseUrl();

        if (!empty($url[0])) {
            $candidate = ucfirst($url[0]) . 'Controller';
            $file = ROOT_PATH . '/app/controllers/' . $candidate . '.php';
            if (file_exists($file)) {
                $this->controller = $candidate;
                unset($url[0]);
            }
        }

        require_once ROOT_PATH . '/app/controllers/' . $this->controller . '.php';
        $this->controller = new $this->controller();

        if (!empty($url[1])) {
            if (method_exists($this->controller, $url[1])) {
                $this->method = $url[1];
                unset($url[1]);
            }
        }

        $this->params = $url ? array_values($url) : [];
        call_user_func_array([$this->controller, $this->method], $this->params);
    }

    private function parseUrl() {
        if (isset($_GET['url'])) {
            $url = rtrim($_GET['url'], '/');
            $url = filter_var($url, FILTER_SANITIZE_URL);
            return explode('/', $url);
        }
        return [];
    }
}
