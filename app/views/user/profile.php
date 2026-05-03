<?php require '../layouts/header.php'; ?>

<div class="card" style="max-width: 640px;">
    <div class="card-header">
        <h3>My Profile</h3>
    </div>
    <form id="profileForm">
        <div class="form-group">
            <label>Username</label>
            <input type="text" id="profUsername" class="form-control" disabled>
        </div>
        <div class="form-group">
            <label>Full Name</label>
            <input type="text" name="fullname" id="profFullname" class="form-control" required>
        </div>
        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" id="profEmail" class="form-control" required>
        </div>
        <div class="form-group">
            <label>New Password (leave blank to keep current)</label>
            <input type="password" name="password" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">Update Profile</button>
    </form>
</div>

<?php require '../layouts/footer.php'; ?>
