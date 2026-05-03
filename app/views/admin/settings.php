<?php require '../layouts/header.php'; ?>

<div class="card" style="max-width: 720px;">
    <div class="card-header">
        <h3>Work Schedule &amp; Company</h3>
    </div>
    <p class="text-muted mb-2" style="font-size: 13px;">
        Set the attendance window. Time-in is only accepted between the
        <strong>start</strong> and <strong>end</strong> times. Anyone who times in
        <strong>after</strong> start + grace period is marked <em>late</em>.
    </p>

    <form id="settingsForm">
        <div class="form-row">
            <div class="form-group">
                <label>Work Start Time</label>
                <input type="time"
                       name="work_start_time"
                       class="form-control"
                       value="<?= htmlspecialchars(substr($settings['work_start_time'] ?? '09:00:00', 0, 5)) ?>"
                       required>
                <small class="text-muted">e.g. 08:00 = 8:00 AM</small>
            </div>
            <div class="form-group">
                <label>Work End Time</label>
                <input type="time"
                       name="work_end_time"
                       class="form-control"
                       value="<?= htmlspecialchars(substr($settings['work_end_time'] ?? '17:00:00', 0, 5)) ?>"
                       required>
                <small class="text-muted">e.g. 17:00 = 5:00 PM</small>
            </div>
            <div class="form-group">
                <label>Late Grace Period (minutes)</label>
                <input type="number"
                       name="late_grace_minutes"
                       class="form-control"
                       value="<?= (int)($settings['late_grace_minutes'] ?? 0) ?>"
                       min="0" max="240" required>
                <small class="text-muted">Allowance before being marked late</small>
            </div>
        </div>

        <div class="form-group">
            <label>Company Name</label>
            <input type="text"
                   name="company_name"
                   class="form-control"
                   value="<?= htmlspecialchars($settings['company_name'] ?? '') ?>"
                   required>
        </div>

        <button type="submit" class="btn btn-primary">Save Settings</button>
    </form>
</div>

<div class="card" style="max-width: 720px;">
    <div class="card-header">
        <h3>How "Late" is Determined</h3>
    </div>
    <p style="font-size: 14px; line-height: 1.7;">
        An employee is marked <span class="badge badge-late">late</span> if their
        time-in is recorded <strong>after</strong>
        <code><?= htmlspecialchars(substr($settings['work_start_time'] ?? '09:00:00', 0, 5)) ?></code>
        + <code><?= (int)($settings['late_grace_minutes'] ?? 0) ?></code> minutes.
        Otherwise they are marked <span class="badge badge-present">present</span>.
    </p>
    <p style="font-size: 14px; line-height: 1.7;">
        Official work hours:
        <strong><?= htmlspecialchars(substr($settings['work_start_time'] ?? '09:00:00', 0, 5)) ?></strong>
        &nbsp;&mdash;&nbsp;
        <strong><?= htmlspecialchars(substr($settings['work_end_time']   ?? '17:00:00', 0, 5)) ?></strong>
    </p>
    <p class="text-muted" style="font-size: 13px;">
        Existing attendance records are <strong>not</strong> recomputed when you
        change these values — only future time-ins are affected.
    </p>
</div>

<?php require '../layouts/footer.php'; ?>
