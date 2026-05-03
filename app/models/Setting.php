<?php
require_once 'app/core/Model.php';

/**
 * Settings (key-value) model.
 * INHERITANCE: extends Model.
 * POLYMORPHISM: overrides create()/update() — keys instead of numeric ids.
 */
class Setting extends Model {
    private $key;
    private $value;

    public function __construct() {
        parent::__construct();
        $this->table = 'settings';
        $this->primaryKey = 'setting_key';
    }

    public function setKey($k) { $this->key = $k; return $this; }
    public function setValue($v) { $this->value = $v; return $this; }

    public function create() {
        $sql = "INSERT INTO {$this->table} (setting_key, setting_value) VALUES (?, ?)";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('ss', $this->key, $this->value);
        return $stmt->execute();
    }

    public function update() {
        $sql = "UPDATE {$this->table} SET setting_value = ? WHERE setting_key = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('ss', $this->value, $this->key);
        return $stmt->execute();
    }

    /** Get a single value by key (with optional fallback). */
    public function get($key, $default = null) {
        $sql = "SELECT setting_value FROM {$this->table} WHERE setting_key = ? LIMIT 1";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('s', $key);
        $stmt->execute();
        $row = $stmt->get_result()->fetch_assoc();
        return $row ? $row['setting_value'] : $default;
    }

    /** Get all settings as an associative array. */
    public function getAll() {
        $result = $this->conn->query("SELECT setting_key, setting_value FROM {$this->table}");
        $out = [];
        while ($row = $result->fetch_assoc()) {
            $out[$row['setting_key']] = $row['setting_value'];
        }
        return $out;
    }

    /** Upsert (insert or update) — convenient for save-from-form. */
    public function set($key, $value) {
        $sql = "INSERT INTO {$this->table} (setting_key, setting_value)
                VALUES (?, ?)
                ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value)";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('ss', $key, $value);
        return $stmt->execute();
    }
}
