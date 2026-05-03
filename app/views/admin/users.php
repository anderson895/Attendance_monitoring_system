<?php require '../layouts/header.php'; ?>

<div class="card">
    <div class="card-header">
        <h3>Users</h3>
        <button id="addUserBtn" class="btn btn-primary btn-sm">+ Add User</button>
    </div>
    <div class="table-wrap">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="usersBody">
                <tr><td colspan="7" class="text-center text-muted">Loading...</td></tr>
            </tbody>
        </table>
    </div>
</div>

<!-- User modal -->
<div id="userModal" class="modal-backdrop">
    <div class="modal">
        <div class="modal-header">
            <h3 id="userFormTitle">Add User</h3>
            <button class="modal-close" type="button">&times;</button>
        </div>
        <form id="userForm">
            <div class="modal-body">
                <input type="hidden" name="id" id="userId">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="fullname" id="userFullname" class="form-control" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" name="username" id="userUsername" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" name="email" id="userEmail" class="form-control" required>
                    </div>
                </div>
                <div class="form-group" id="userPasswordGroup">
                    <label>Password</label>
                    <input type="password" name="password" id="userPassword" class="form-control">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Role</label>
                        <select name="role" id="userRole" class="form-control">
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Status</label>
                        <select name="status" id="userStatus" class="form-control">
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-primary">Save</button>
            </div>
        </form>
    </div>
</div>

<?php require '../layouts/footer.php'; ?>
