<?php
require_once ROOT_PATH . '/app/core/Model.php';

/**
 * INHERITANCE: extends Model.
 * POLYMORPHISM: concrete create()/update() overriding the abstract base.
 * ENCAPSULATION: internal fields private; exposed via setters/getters.
 */
class Attendance extends Model {
    private $id;
    private $userId;
    private $date;
    private $timeIn;
    private $timeOut;
    private $status = 'present';
    private $remarks;

    public function __construct() {
        parent::__construct();
        $this->table = 'attendance';
    }

    public function setId($v) { $this->id = (int)$v; return $this; }
    public function setUserId($v) { $this->userId = (int)$v; return $this; }
    public function setDate($v) { $this->date = $v; return $this; }
    public function setTimeIn($v) { $this->timeIn = $v; return $this; }
    public function setTimeOut($v) { $this->timeOut = $v; return $this; }
    public function setStatus($v) { $this->status = in_array($v, ['present','late','absent']) ? $v : 'present'; return $this; }
    public function setRemarks($v) { $this->remarks = $v; return $this; }

    public function getId() { return $this->id; }
    public function getUserId() { return $this->userId; }
    public function getDate() { return $this->date; }
    public function getTimeIn() { return $this->timeIn; }
    public function getTimeOut() { return $this->timeOut; }
    public function getStatus() { return $this->status; }

    public function create() {
        $sql = "INSERT INTO {$this->table} (user_id, date, time_in, status, remarks) VALUES (?, ?, ?, ?, ?)";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('issss', $this->userId, $this->date, $this->timeIn, $this->status, $this->remarks);
        if ($stmt->execute()) {
            $this->id = $stmt->insert_id;
            return true;
        }
        return false;
    }

    public function update() {
        $sql = "UPDATE {$this->table} SET time_in=?, time_out=?, status=?, remarks=? WHERE id=?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('ssssi', $this->timeIn, $this->timeOut, $this->status, $this->remarks, $this->id);
        return $stmt->execute();
    }

    // --- Domain operations ---
    public function timeIn($userId) {
        $today = date('Y-m-d');
        $now = date('Y-m-d H:i:s');

        $existing = $this->getTodayLog($userId);
        if ($existing && !empty($existing['time_in'])) {
            return ['status' => 'error', 'message' => 'You already timed in today.'];
        }

        $cutoff = strtotime($today . ' 09:00:00');
        $status = (time() > $cutoff) ? 'late' : 'present';

        if ($existing) {
            $sql = "UPDATE {$this->table} SET time_in = ?, status = ? WHERE id = ?";
            $stmt = $this->conn->prepare($sql);
            $stmt->bind_param('ssi', $now, $status, $existing['id']);
        } else {
            $sql = "INSERT INTO {$this->table} (user_id, date, time_in, status) VALUES (?, ?, ?, ?)";
            $stmt = $this->conn->prepare($sql);
            $stmt->bind_param('isss', $userId, $today, $now, $status);
        }

        if ($stmt->execute()) {
            return [
                'status' => 'success',
                'message' => 'Time-in recorded at ' . date('h:i A'),
                'time' => $now,
                'attendance_status' => $status
            ];
        }
        return ['status' => 'error', 'message' => 'Failed to record time-in.'];
    }

    public function timeOut($userId) {
        $now = date('Y-m-d H:i:s');
        $existing = $this->getTodayLog($userId);

        if (!$existing || empty($existing['time_in'])) {
            return ['status' => 'error', 'message' => 'You have not timed in yet today.'];
        }
        if (!empty($existing['time_out'])) {
            return ['status' => 'error', 'message' => 'You already timed out today.'];
        }

        $sql = "UPDATE {$this->table} SET time_out = ? WHERE id = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('si', $now, $existing['id']);

        if ($stmt->execute()) {
            return ['status' => 'success', 'message' => 'Time-out recorded at ' . date('h:i A'), 'time' => $now];
        }
        return ['status' => 'error', 'message' => 'Failed to record time-out.'];
    }

    public function getTodayLog($userId) {
        $today = date('Y-m-d');
        $sql = "SELECT * FROM {$this->table} WHERE user_id = ? AND date = ? LIMIT 1";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('is', $userId, $today);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public function getUserHistory($userId, $limit = 100) {
        $sql = "SELECT * FROM {$this->table} WHERE user_id = ? ORDER BY date DESC LIMIT ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('ii', $userId, $limit);
        $stmt->execute();
        $result = $stmt->get_result();
        $rows = [];
        while ($row = $result->fetch_assoc()) {
            $rows[] = $row;
        }
        return $rows;
    }

    public function getAllRecords($filters = []) {
        $sql = "SELECT a.*, u.fullname, u.username
                FROM {$this->table} a
                INNER JOIN users u ON a.user_id = u.id
                WHERE 1=1";
        $params = [];
        $types = '';

        if (!empty($filters['date_from'])) {
            $sql .= " AND a.date >= ?";
            $params[] = $filters['date_from']; $types .= 's';
        }
        if (!empty($filters['date_to'])) {
            $sql .= " AND a.date <= ?";
            $params[] = $filters['date_to']; $types .= 's';
        }
        if (!empty($filters['user_id'])) {
            $sql .= " AND a.user_id = ?";
            $params[] = $filters['user_id']; $types .= 'i';
        }
        if (!empty($filters['status'])) {
            $sql .= " AND a.status = ?";
            $params[] = $filters['status']; $types .= 's';
        }

        $sql .= " ORDER BY a.date DESC, a.time_in DESC";
        $stmt = $this->conn->prepare($sql);
        if (!empty($params)) {
            $stmt->bind_param($types, ...$params);
        }
        $stmt->execute();
        $result = $stmt->get_result();
        $rows = [];
        while ($row = $result->fetch_assoc()) {
            $rows[] = $row;
        }
        return $rows;
    }

    public function getStats($userId = null) {
        if ($userId) {
            $sql = "SELECT
                        COUNT(*) AS total,
                        SUM(status='present') AS present,
                        SUM(status='late') AS late,
                        SUM(status='absent') AS absent
                    FROM {$this->table} WHERE user_id = ?";
            $stmt = $this->conn->prepare($sql);
            $stmt->bind_param('i', $userId);
            $stmt->execute();
            return $stmt->get_result()->fetch_assoc();
        }
        $result = $this->conn->query("SELECT
                COUNT(*) AS total,
                SUM(status='present') AS present,
                SUM(status='late') AS late,
                SUM(status='absent') AS absent
            FROM {$this->table}");
        return $result->fetch_assoc();
    }

    public function getTodayStats() {
        $today = date('Y-m-d');
        $sql = "SELECT
                    COUNT(*) AS total_present,
                    SUM(status='late') AS total_late
                FROM {$this->table}
                WHERE date = ?";
        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param('s', $today);
        $stmt->execute();
        return $stmt->get_result()->fetch_assoc();
    }

    public static function calcDuration($timeIn, $timeOut) {
        if (empty($timeIn) || empty($timeOut)) return '—';
        $diff = strtotime($timeOut) - strtotime($timeIn);
        if ($diff <= 0) return '—';
        $h = floor($diff / 3600);
        $m = floor(($diff % 3600) / 60);
        return sprintf('%dh %dm', $h, $m);
    }
}
