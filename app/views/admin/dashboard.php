<?php require ROOT_PATH . '/app/views/layouts/header.php'; ?>

<div class="stats-grid">
    <div class="stat-card">
        <div class="label">Total Users</div>
        <div class="value"><?= (int)$totalUsers ?></div>
        <div class="desc">Registered staff</div>
    </div>
    <div class="stat-card success">
        <div class="label">Present Today</div>
        <div class="value"><?= (int)($today['total_present'] ?? 0) ?></div>
        <div class="desc">Logged in today</div>
    </div>
    <div class="stat-card warning">
        <div class="label">Late Today</div>
        <div class="value"><?= (int)($today['total_late'] ?? 0) ?></div>
        <div class="desc">After 9:00 AM</div>
    </div>
    <div class="stat-card info">
        <div class="label">Total Records</div>
        <div class="value"><?= (int)($stats['total'] ?? 0) ?></div>
        <div class="desc">All-time entries</div>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>Recent Activity</h3>
        <a href="<?= BASE_URL ?>admin/attendance" class="btn btn-sm btn-secondary">View All</a>
    </div>
    <div class="table-wrap">
        <table class="table">
            <thead>
                <tr>
                    <th>User</th>
                    <th>Date</th>
                    <th>Time In</th>
                    <th>Time Out</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
            <?php if (empty($recent)): ?>
                <tr><td colspan="5" class="text-center text-muted">No recent activity</td></tr>
            <?php else: foreach ($recent as $r): ?>
                <tr>
                    <td>
                        <strong><?= htmlspecialchars($r['fullname']) ?></strong><br>
                        <small class="text-muted">@<?= htmlspecialchars($r['username']) ?></small>
                    </td>
                    <td><?= $r['date'] ?></td>
                    <td><?= $r['time_in'] ? date('h:i A', strtotime($r['time_in'])) : '—' ?></td>
                    <td><?= $r['time_out'] ? date('h:i A', strtotime($r['time_out'])) : '—' ?></td>
                    <td><span class="badge badge-<?= $r['status'] ?>"><?= $r['status'] ?></span></td>
                </tr>
            <?php endforeach; endif; ?>
            </tbody>
        </table>
    </div>
</div>

<?php require ROOT_PATH . '/app/views/layouts/footer.php'; ?>
