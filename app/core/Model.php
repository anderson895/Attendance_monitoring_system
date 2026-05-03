<?php
require_once 'app/core/Database.php';

/**
 * ABSTRACTION pillar
 * ------------------
 * Abstract base Model defines the contract every model must follow
 * (create/update) and hides the low-level mysqli plumbing from children.
 */
abstract class Model {
    protected $conn;
    protected $table;
    protected $primaryKey = 'id';

    public function __construct() {
        $this->conn = Database::getInstance()->getConnection();
    }

    abstract public function create();
    abstract public function update();

    public function findById($id) {
        $sql = "SELECT * FROM {$this->table} WHERE {$this->primaryKey} = ? LIMIT 1";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('i', $id);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function delete($id) {
        $sql = "DELETE FROM {$this->table} WHERE {$this->primaryKey} = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('i', $id);
        return $stmt->execute();
    }

    public function all($orderBy = 'id DESC') {
        $sql = "SELECT * FROM {$this->table} ORDER BY {$orderBy}";
        $result = $this->conn->query($sql);
        $rows = [];
        while ($row = $result->fetch_assoc()) {
            $rows[] = $row;
        }
        return $rows;
    }

    public function count($where = '1=1') {
        $result = $this->conn->query("SELECT COUNT(*) AS total FROM {$this->table} WHERE {$where}");
        return (int)$result->fetch_assoc()['total'];
    }
}
