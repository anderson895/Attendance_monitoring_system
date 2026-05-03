<?php require '../layouts/header.php'; ?>

<div class="clock-card">
    <div class="time" id="liveClock">--:--:--</div>
    <div class="date" id="liveDate"></div>
    <div class="actions">
        <button id="btnTimeIn" class="btn btn-success" disabled>Time In</button>
        <button id="btnTimeOut" class="btn btn-warning" disabled>Time Out</button>
    </div>
</div>

<div id="todayLogBox" class="stats-grid">
    <div class="stat-card success">
        <div class="label">Today's Time In</div>
        <div class="value" id="todayTimeIn" style="font-size:22px;">—</div>
    </div>
    <div class="stat-card warning">
        <div class="label">Today's Time Out</div>
        <div class="value" id="todayTimeOut" style="font-size:22px;">—</div>
    </div>
    <div class="stat-card info">
        <div class="label">Status</div>
        <div class="value" id="todayStatus" style="font-size:22px;">
            <span class="text-muted">Loading...</span>
        </div>
    </div>
    <div class="stat-card">
        <div class="label">Total Days Present</div>
        <div class="value" id="statPresent">0</div>
        <div class="desc">
            <span id="statLate">0</span> late ·
            <span id="statAbsent">0</span> absent
        </div>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>Recent Attendance</h3>
        <a href="<?php echo BASE_URL; ?>user/attendance" class="btn btn-sm btn-secondary">View All</a>
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
            <tbody id="recentAttendanceBody">
                <tr>
                    <td colspan="4" class="text-center text-muted">Loading...</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

<?php require '../layouts/footer.php'; ?>
