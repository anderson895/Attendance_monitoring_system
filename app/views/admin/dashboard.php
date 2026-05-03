<?php require '../layouts/header.php'; ?>

<div class="stats-grid">
    <div class="stat-card">
        <div class="label">Total Users</div>
        <div class="value" id="statTotalUsers">0</div>
        <div class="desc">Registered staff</div>
    </div>
    <div class="stat-card success">
        <div class="label">Present Today</div>
        <div class="value" id="statPresentToday">0</div>
        <div class="desc">Logged in today</div>
    </div>
    <div class="stat-card warning">
        <div class="label">Late Today</div>
        <div class="value" id="statLateToday">0</div>
        <div class="desc">After work start</div>
    </div>
    <div class="stat-card info">
        <div class="label">Total Records</div>
        <div class="value" id="statTotalRecords">0</div>
        <div class="desc">All-time entries</div>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>Recent Activity</h3>
        <a href="admin/attendance" class="btn btn-sm btn-secondary" id="linkViewAllAttendance">View All</a>
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
            <tbody id="recentActivityBody">
                <tr><td colspan="5" class="text-center text-muted">Loading...</td></tr>
            </tbody>
        </table>
    </div>
</div>

<?php require '../layouts/footer.php'; ?>
