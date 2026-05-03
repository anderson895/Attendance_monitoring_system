<?php require ROOT_PATH . '/app/views/layouts/header.php'; ?>

<div class="clock-card">
    <div class="time" id="liveClock">--:--:--</div>
    <div class="date" id="liveDate"></div>
    <div class="actions">
        <button id="btnTimeIn" class="btn btn-success" <?= ($today && !empty($today['time_in'])) ? 'disabled' : '' ?>>
            Time In
        </button>
        <button id="btnTimeOut" class="btn btn-warning" <?= (!$today || empty($today['time_in']) || !empty($today['time_out'])) ? 'disabled' : '' ?>>
            Time Out
        </button>
    </div>
</div>

<div id="todayLogBox" class="stats-grid">
    <div class="stat-card success">
        <div class="label">Today's Time In</div>
        <div class="value" id="todayTimeIn" style="font-size:22px;">
            <?= ($today && $today['time_in']) ? date('h:i A', strtotime($today['time_in'])) : '—' ?>
        </div>
    </div>
    <div class="stat-card warning">
        <div class="label">Today's Time Out</div>
        <div class="value" id="todayTimeOut" style="font-size:22px;">
            <?= ($today && $today['time_out']) ? date('h:i A', strtotime($today['time_out'])) : '—' ?>
        </div>
    </div>
    <div class="stat-card info">
        <div class="label">Status</div>
        <div class="value" id="todayStatus" style="font-size:22px;">
            <?php if ($today && $today['status']): ?>
                <span class="badge badge-<?= $today['status'] ?>"><?= $today['status'] ?></span>
            <?php else: ?>
                <span class="text-muted">No record yet</span>
            <?php endif; ?>
        </div>
    </div>
    <div class="stat-card">
        <div class="label">Total Days Present</div>
        <div class="value"><?= (int)($stats['present'] ?? 0) ?></div>
        <div class="desc"><?= (int)($stats['late'] ?? 0) ?> late · <?= (int)($stats['absent'] ?? 0) ?> absent</div>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>Recent Attendance</h3>
        <a href="<?= BASE_URL ?>user/attendance" class="btn btn-sm btn-secondary">View All</a>
    </div>
    <div class="table-wrap">
        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Time In</th>
                    <th>Time Out</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
            <?php if (empty($recent)): ?>
                <tr><td colspan="4" class="text-center text-muted">No attendance records yet</td></tr>
            <?php else: foreach ($recent as $r): ?>
                <tr>
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
