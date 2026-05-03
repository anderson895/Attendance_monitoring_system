<?php require '../layouts/header.php'; ?>

<div class="card">
    <div class="card-header">
        <h3>Filter Records</h3>
    </div>
    <form id="attendanceFilters">
        <div class="form-row" style="grid-template-columns: repeat(4, 1fr);">
            <div class="form-group">
                <label>From</label>
                <input type="date" name="date_from" class="form-control">
            </div>
            <div class="form-group">
                <label>To</label>
                <input type="date" name="date_to" class="form-control">
            </div>
            <div class="form-group">
                <label>User</label>
                <select name="user_id" id="filterUserId" class="form-control">
                    <option value="">All users</option>
                </select>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select name="status" class="form-control">
                    <option value="">All</option>
                    <option value="present">Present</option>
                    <option value="late">Late</option>
                    <option value="absent">Absent</option>
                </select>
            </div>
        </div>
        <div class="flex">
            <button type="submit" class="btn btn-primary btn-sm">Apply</button>
            <button type="button" id="clearFilters" class="btn btn-secondary btn-sm">Clear</button>
        </div>
    </form>
</div>

<div class="card">
    <div class="card-header">
        <h3>Attendance Records</h3>
    </div>
    <div class="table-wrap">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>User</th>
                    <th>Date</th>
                    <th>Time In</th>
                    <th>Time Out</th>
                    <th>Duration</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody id="attendanceBody">
                <tr><td colspan="8" class="text-center text-muted">Loading...</td></tr>
            </tbody>
        </table>
    </div>
</div>

<?php require '../layouts/footer.php'; ?>
