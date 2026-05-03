<?php
require_once 'app/core/Model.php';

/**
 * INHERITANCE pillar: User extends Model.
 * ENCAPSULATION pillar: properties are private; mutated only through setters.
 * POLYMORPHISM pillar: provides concrete create()/update() that override
 *                      the abstract methods declared in Model.
 */
class User extends Model {
    private $id;
    private $fullname;
    private $username;
    private $email;
    private $password;
    private $role = 'user';
    private $status = 'active';

    public function __construct() {
        parent::__construct();
        $this->table = 'users';
    }

    // --- Encapsulation: setters (fluent) ---
    public function setId($v) { $this->id = (int)$v; return $this; }
    public function setFullname($v) { $this->fullname = trim($v); return $this; }
    public function setUsername($v) { $this->username = trim($v); return $this; }
    public function setEmail($v) { $this->email = trim($v); return $this; }
    public function setPassword($v) { $this->password = $v; return $this; }
    public function setRole($v) { $this->role = in_array($v, ['admin','user']) ? $v : 'user'; return $this; }
    public function setStatus($v) { $this->status = in_array($v, ['active','inactive']) ? $v : 'active'; return $this; }

    // --- Encapsulation: getters ---
    public function getId() { return $this->id; }
    public function getFullname() { return $this->fullname; }
    public function getUsername() { return $this->username; }
    public function getEmail() { return $this->email; }
    public function getRole() { return $this->role; }
    public function getStatus() { return $this->status; }

    // --- Polymorphism: concrete overrides ---
    public function create() {
        $sql = "INSERT INTO {$this->table} (fullname, username, email, password, role, status)
                VALUES (?, ?, ?, ?, ?, ?)";
        $stmt = $this->conn->prepare($sql);
        $hashed = password_hash($this->password, PASSWORD_BCRYPT);
        $stmt->bind_param('ssssss', $this->fullname, $this->username, $this->email, $hashed, $this->role, $this->status);
        if ($stmt->execute()) {
            $this->id = $stmt->insert_id;
            return true;
        }
        return false;
    }

    public function update() {
        if (!empty($this->password)) {
            $hashed = password_hash($this->password, PASSWORD_BCRYPT);
            $sql = "UPDATE {$this->table} SET fullname=?, username=?, email=?, password=?, role=?, status=? WHERE id=?";
            $stmt = $this->conn->prepare($sql);
            $stmt->bind_param('ssssssi', $this->fullname, $this->username, $this->email, $hashed, $this->role, $this->status, $this->id);
        } else {
            $sql = "UPDATE {$this->table} SET fullname=?, username=?, email=?, role=?, status=? WHERE id=?";
            $stmt = $this->conn->prepare($sql);
            $stmt->bind_param('sssssi', $this->fullname, $this->username, $this->email, $this->role, $this->status, $this->id);
        }
        return $stmt->execute();
    }

    // --- Domain queries ---
    public function findByUsername($username) {
        $sql = "SELECT * FROM {$this->table} WHERE username = ? LIMIT 1";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('s', $username);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function getAll() {
        $sql = "SELECT id, fullname, username, email, role, status, created_at FROM {$this->table} ORDER BY id DESC";
        $result = $this->conn->query($sql);
        $rows = [];
        while ($row = $result->fetch_assoc()) {
            $rows[] = $row;
        }
        return $rows;
    }

    public function usernameExists($username, $excludeId = 0) {
        $sql = "SELECT id FROM {$this->table} WHERE username = ? AND id != ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('si', $username, $excludeId);
        $stmt->execute();
        return $stmt->get_result()->num_rows > 0;
    }

    public function emailExists($email, $excludeId = 0) {
        $sql = "SELECT id FROM {$this->table} WHERE email = ? AND id != ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('si', $email, $excludeId);
        $stmt->execute();
        return $stmt->get_result()->num_rows > 0;
    }

    public function countUsers() {
        return $this->count("role = 'user'");
    }
}
