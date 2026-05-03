<?php require ROOT_PATH . '/app/views/layouts/header.php'; ?>

<div class="card">
    <div class="card-header">
        <h3>My Attendance History</h3>
    </div>
    <div class="table-wrap">
        <table class="table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Time In</th>
                    <th>Time Out</th>
                    <th>Duration</th>
                    <th>Status</th>
                    <th>Remarks</th>
                </tr>
            </thead>
            <tbody id="myHistoryBody">
                <tr><td colspan="6" class="text-center text-muted">Loading...</td></tr>
            </tbody>
        </table>
    </div>
</div>

<?php require ROOT_PATH . '/app/views/layouts/footer.php'; ?>
