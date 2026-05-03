/* ===========================================================
   Attendance Monitoring System — Centralized jQuery / AJAX
   =========================================================== */

// BASE_URL is injected by the layout via <script>window.BASE_URL = '...'</script>
window.BASE_URL = window.BASE_URL || '/';

/* ----------- Company name (system-wide branding) ----------- */
window._basePageTitle = document.title;
function loadCompanyName() {
    ajaxGet('home/companyName').done(function (res) {
        if (res.status !== 'success' || !res.data) return;
        var name = res.data.company_name || 'My Company';
        $('#brandName').text(name);
        document.title = window._basePageTitle + ' — ' + name;
    });
}

/* ----------- Toast helper ----------- */
function toast(message, type) {
    type = type || 'info';
    if ($('.toast-stack').length === 0) {
        $('body').append('<div class="toast-stack"></div>');
    }
    var $t = $('<div class="toast ' + type + '">' + message + '</div>');
    $('.toast-stack').append($t);
    setTimeout(function () {
        $t.fadeOut(250, function () { $(this).remove(); });
    }, 3500);
}

/* ----------- Generic AJAX wrapper ----------- */
function ajaxPost(url, data) {
    return $.ajax({
        url: window.BASE_URL + url,
        type: 'POST',
        data: data,
        dataType: 'json',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
}
function ajaxGet(url, data) {
    return $.ajax({
        url: window.BASE_URL + url,
        type: 'GET',
        data: data,
        dataType: 'json',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
}

/* ----------- Modal helpers ----------- */
function openModal(id) { $('#' + id).addClass('show'); }
function closeModal(id) { $('#' + id).removeClass('show'); }

$(document).on('click', '.modal-close, [data-dismiss="modal"]', function () {
    $(this).closest('.modal-backdrop').removeClass('show');
});
$(document).on('click', '.modal-backdrop', function (e) {
    if (e.target === this) $(this).removeClass('show');
});

/* ===========================================================
   LOGIN
   =========================================================== */
$(document).on('submit', '#loginForm', function (e) {
    e.preventDefault();
    var $btn = $(this).find('button[type=submit]').prop('disabled', true).text('Signing in...');
    ajaxPost('auth/doLogin', $(this).serialize())
        .done(function (res) {
            if (res.status === 'success') {
                toast(res.message, 'success');
                setTimeout(function () { window.location.href = res.redirect; }, 400);
            } else {
                toast(res.message, 'error');
                $btn.prop('disabled', false).text('Sign In');
            }
        })
        .fail(function () {
            toast('Server error', 'error');
            $btn.prop('disabled', false).text('Sign In');
        });
});

/* ===========================================================
   REGISTER
   =========================================================== */
$(document).on('submit', '#registerForm', function (e) {
    e.preventDefault();
    var $btn = $(this).find('button[type=submit]').prop('disabled', true).text('Creating...');
    ajaxPost('auth/doRegister', $(this).serialize())
        .done(function (res) {
            toast(res.message, res.status);
            if (res.status === 'success') {
                setTimeout(function () { window.location.href = window.BASE_URL + 'auth/login'; }, 800);
            } else {
                $btn.prop('disabled', false).text('Create Account');
            }
        })
        .fail(function () {
            toast('Server error', 'error');
            $btn.prop('disabled', false).text('Create Account');
        });
});

/* ===========================================================
   LIVE CLOCK (user dashboard)
   =========================================================== */
function tickClock() {
    var $clock = $('#liveClock');
    var $date  = $('#liveDate');
    if (!$clock.length) return;
    var d = new Date();
    var h = d.getHours(), m = d.getMinutes(), s = d.getSeconds();
    var ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12; if (h === 0) h = 12;
    var pad = function (n) { return n < 10 ? '0' + n : n; };
    $clock.text(pad(h) + ':' + pad(m) + ':' + pad(s) + ' ' + ampm);
    $date.text(d.toDateString());
}
setInterval(tickClock, 1000);

/* ===========================================================
   TIME IN / TIME OUT
   =========================================================== */
$(document).on('click', '#btnTimeIn', function () {
    var $b = $(this).prop('disabled', true);
    ajaxPost('user/timeIn', {})
        .done(function (res) {
            toast(res.message, res.status);
            if (res.status === 'success') {
                refreshTodayLog();
                refreshRecentTable();
                loadMyHistory();
            }
        })
        .always(function () { $b.prop('disabled', false); });
});

$(document).on('click', '#btnTimeOut', function () {
    var $b = $(this).prop('disabled', true);
    ajaxPost('user/timeOut', {})
        .done(function (res) {
            toast(res.message, res.status);
            if (res.status === 'success') {
                refreshTodayLog();
                refreshRecentTable();
                loadMyHistory();
            }
        })
        .always(function () { $b.prop('disabled', false); });
});

/* Refresh the "Recent Attendance" table on the user dashboard */
function refreshRecentTable() {
    var $body = $('#recentAttendanceBody');
    if (!$body.length) return;
    ajaxGet('user/history').done(function (res) {
        var rows = (res.data || []).slice(0, 8);
        var html = '';
        if (!rows.length) {
            html = '<tr><td colspan="4" class="text-center text-muted">No attendance records yet</td></tr>';
        } else {
            rows.forEach(function (r) {
                html += '<tr>'
                    + '<td>' + r.date + '</td>'
                    + '<td>' + (r.time_in ? new Date(r.time_in.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + (r.time_out ? new Date(r.time_out.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + renderStatusBadge(r.status) + '</td>'
                    + '</tr>';
            });
        }
        $body.html(html);
    });
}

function refreshTodayLog() {
    if (!$('#todayLogBox').length) return;
    $('#linkViewAllMyAttendance').attr('href', window.BASE_URL + 'user/attendance');
    ajaxGet('user/todayLog').done(function (res) {
        if (res.status !== 'success') return;
        var d = res.data;
        var s = res.stats || {};
        var fmt = function (v) { return v ? new Date(v.replace(' ', 'T')).toLocaleTimeString() : '—'; };
        $('#todayTimeIn').text(d ? fmt(d.time_in) : '—');
        $('#todayTimeOut').text(d ? fmt(d.time_out) : '—');
        $('#todayStatus').html(d ? renderStatusBadge(d.status) : '<span class="text-muted">No record yet</span>');

        $('#statPresent').text(s.present || 0);
        $('#statLate').text(s.late || 0);
        $('#statAbsent').text(s.absent || 0);

        $('#btnTimeIn').prop('disabled', !!(d && d.time_in));
        $('#btnTimeOut').prop('disabled', !d || !d.time_in || !!d.time_out);
    });
}
function renderStatusBadge(s) {
    if (!s) return '';
    return '<span class="badge badge-' + s + '">' + s + '</span>';
}

/* ===========================================================
   USER ATTENDANCE HISTORY
   =========================================================== */
function loadMyHistory() {
    if (!$('#myHistoryBody').length) return;
    ajaxGet('user/history').done(function (res) {
        var rows = res.data || [];
        var html = '';
        if (!rows.length) {
            html = '<tr><td colspan="6" class="text-center text-muted">No attendance records yet</td></tr>';
        } else {
            rows.forEach(function (r) {
                html += '<tr>'
                    + '<td>' + r.date + '</td>'
                    + '<td>' + (r.time_in ? new Date(r.time_in.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + (r.time_out ? new Date(r.time_out.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + r.duration + '</td>'
                    + '<td>' + renderStatusBadge(r.status) + '</td>'
                    + '<td>' + (r.remarks || '—') + '</td>'
                    + '</tr>';
            });
        }
        $('#myHistoryBody').html(html);
    });
}

/* ===========================================================
   ADMIN — SETTINGS
   =========================================================== */
function loadSettingsForm() {
    if (!$('#settingsForm').length) return;
    ajaxGet('admin/getSettings').done(function (res) {
        if (res.status !== 'success') return;
        var s = res.data || {};
        var hhmm = function (t) { return (t || '').substring(0, 5); };
        $('#fldWorkStart').val(hhmm(s.work_start_time || '09:00:00'));
        $('#fldWorkEnd').val(hhmm(s.work_end_time || '17:00:00'));
        $('#fldGrace').val(parseInt(s.late_grace_minutes || 0, 10));
        $('#fldCompany').val(s.company_name || '');
        $('#infoStartTime').text(hhmm(s.work_start_time || '09:00:00'));
        $('#infoStartTime2').text(hhmm(s.work_start_time || '09:00:00'));
        $('#infoEndTime').text(hhmm(s.work_end_time || '17:00:00'));
        $('#infoGrace').text(parseInt(s.late_grace_minutes || 0, 10));
    });
}

$(document).on('submit', '#settingsForm', function (e) {
    e.preventDefault();
    var $btn = $(this).find('button[type=submit]').prop('disabled', true).text('Saving...');
    ajaxPost('admin/saveSettings', $(this).serialize())
        .done(function (res) {
            toast(res.message, res.status);
            if (res.status === 'success') {
                loadSettingsForm();
                loadCompanyName();
            }
        })
        .always(function () {
            $btn.prop('disabled', false).text('Save Settings');
        });
});

/* ===========================================================
   ADMIN — DASHBOARD STATS
   =========================================================== */
function loadAdminDashboard() {
    if (!$('#statTotalUsers').length) return;
    $('#linkViewAllAttendance').attr('href', window.BASE_URL + 'admin/attendance');
    ajaxGet('admin/dashboardStats').done(function (res) {
        if (res.status !== 'success') return;
        var d = res.data || {};
        var t = d.today || {};
        var s = d.stats || {};
        $('#statTotalUsers').text(d.totalUsers || 0);
        $('#statPresentToday').text(parseInt(t.total_present || 0, 10));
        $('#statLateToday').text(parseInt(t.total_late || 0, 10));
        $('#statTotalRecords').text(parseInt(s.total || 0, 10));

        var rows = d.recent || [];
        var html = '';
        if (!rows.length) {
            html = '<tr><td colspan="5" class="text-center text-muted">No recent activity</td></tr>';
        } else {
            rows.forEach(function (r) {
                html += '<tr>'
                    + '<td><strong>' + escapeHtml(r.fullname) + '</strong><br><small class="text-muted">@' + escapeHtml(r.username) + '</small></td>'
                    + '<td>' + r.date + '</td>'
                    + '<td>' + (r.time_in ? new Date(r.time_in.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + (r.time_out ? new Date(r.time_out.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + renderStatusBadge(r.status) + '</td>'
                    + '</tr>';
            });
        }
        $('#recentActivityBody').html(html);
    });
}

/* ===========================================================
   ADMIN — ATTENDANCE FILTER USER DROPDOWN
   =========================================================== */
function loadAttendanceUserFilter() {
    if (!$('#filterUserId').length) return;
    ajaxGet('admin/listUsers').done(function (res) {
        if (res.status !== 'success') return;
        var rows = res.data || [];
        var html = '<option value="">All users</option>';
        rows.forEach(function (u) {
            html += '<option value="' + u.id + '">' + escapeHtml(u.fullname) + '</option>';
        });
        $('#filterUserId').html(html);
    });
}

/* ===========================================================
   PROFILE UPDATE
   =========================================================== */
function loadProfileForm() {
    if (!$('#profileForm').length) return;
    ajaxGet('user/myProfile').done(function (res) {
        if (res.status !== 'success' || !res.data) return;
        var u = res.data;
        $('#profUsername').val(u.username || '');
        $('#profFullname').val(u.fullname || '');
        $('#profEmail').val(u.email || '');
    });
}

$(document).on('submit', '#profileForm', function (e) {
    e.preventDefault();
    ajaxPost('user/updateProfile', $(this).serialize()).done(function (res) {
        toast(res.message, res.status);
    });
});

/* ===========================================================
   ADMIN — USERS CRUD
   =========================================================== */
function loadUsers() {
    if (!$('#usersBody').length) return;
    ajaxGet('admin/listUsers').done(function (res) {
        var rows = res.data || [];
        var html = '';
        if (!rows.length) {
            html = '<tr><td colspan="7" class="text-center text-muted">No users</td></tr>';
        } else {
            rows.forEach(function (u) {
                html += '<tr>'
                    + '<td>#' + u.id + '</td>'
                    + '<td>' + escapeHtml(u.fullname) + '</td>'
                    + '<td>' + escapeHtml(u.username) + '</td>'
                    + '<td>' + escapeHtml(u.email) + '</td>'
                    + '<td><span class="badge badge-' + u.role + '">' + u.role + '</span></td>'
                    + '<td><span class="badge badge-' + u.status + '">' + u.status + '</span></td>'
                    + '<td class="actions">'
                    +   '<button class="btn btn-sm btn-primary editUser" data-id="' + u.id + '">Edit</button>'
                    +   '<button class="btn btn-sm btn-danger deleteUser" data-id="' + u.id + '">Delete</button>'
                    + '</td></tr>';
            });
        }
        $('#usersBody').html(html);
    });
}

$(document).on('click', '#addUserBtn', function () {
    $('#userForm')[0].reset();
    $('#userId').val('');
    $('#userFormTitle').text('Add User');
    $('#userPasswordGroup label').text('Password');
    $('#userPassword').attr('required', true);
    openModal('userModal');
});

$(document).on('click', '.editUser', function () {
    var id = $(this).data('id');
    ajaxGet('admin/getUser', { id: id }).done(function (res) {
        if (res.status !== 'success') { toast(res.message, 'error'); return; }
        var u = res.data;
        $('#userId').val(u.id);
        $('#userFullname').val(u.fullname);
        $('#userUsername').val(u.username);
        $('#userEmail').val(u.email);
        $('#userRole').val(u.role);
        $('#userStatus').val(u.status);
        $('#userPassword').val('').removeAttr('required');
        $('#userPasswordGroup label').text('Password (leave blank to keep)');
        $('#userFormTitle').text('Edit User');
        openModal('userModal');
    });
});

$(document).on('submit', '#userForm', function (e) {
    e.preventDefault();
    ajaxPost('admin/saveUser', $(this).serialize()).done(function (res) {
        toast(res.message, res.status);
        if (res.status === 'success') {
            closeModal('userModal');
            loadUsers();
        }
    });
});

$(document).on('click', '.deleteUser', function () {
    if (!confirm('Delete this user? This cannot be undone.')) return;
    var id = $(this).data('id');
    ajaxPost('admin/deleteUser', { id: id }).done(function (res) {
        toast(res.message, res.status);
        if (res.status === 'success') loadUsers();
    });
});

/* ===========================================================
   ADMIN — ATTENDANCE LIST + FILTERS
   =========================================================== */
function loadAttendance() {
    if (!$('#attendanceBody').length) return;
    var filters = $('#attendanceFilters').serialize();
    ajaxGet('admin/listAttendance', filters).done(function (res) {
        var rows = res.data || [];
        var html = '';
        if (!rows.length) {
            html = '<tr><td colspan="8" class="text-center text-muted">No attendance records</td></tr>';
        } else {
            rows.forEach(function (r) {
                html += '<tr>'
                    + '<td>#' + r.id + '</td>'
                    + '<td>' + escapeHtml(r.fullname) + '<br><small class="text-muted">@' + escapeHtml(r.username) + '</small></td>'
                    + '<td>' + r.date + '</td>'
                    + '<td>' + (r.time_in ? new Date(r.time_in.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + (r.time_out ? new Date(r.time_out.replace(' ', 'T')).toLocaleTimeString() : '—') + '</td>'
                    + '<td>' + r.duration + '</td>'
                    + '<td>' + renderStatusBadge(r.status) + '</td>'
                    + '<td><button class="btn btn-sm btn-danger deleteAtt" data-id="' + r.id + '">Delete</button></td>'
                    + '</tr>';
            });
        }
        $('#attendanceBody').html(html);
    });
}

$(document).on('submit', '#attendanceFilters', function (e) {
    e.preventDefault();
    loadAttendance();
});
$(document).on('click', '#clearFilters', function () {
    $('#attendanceFilters')[0].reset();
    loadAttendance();
});

$(document).on('click', '.deleteAtt', function () {
    if (!confirm('Delete this attendance record?')) return;
    var id = $(this).data('id');
    ajaxPost('admin/deleteAttendance', { id: id }).done(function (res) {
        toast(res.message, res.status);
        if (res.status === 'success') loadAttendance();
    });
});

/* ----------- helpers ----------- */
function escapeHtml(s) {
    if (s == null) return '';
    return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/* ===========================================================
   INIT
   =========================================================== */
$(function () {
    loadCompanyName();
    tickClock();
    refreshTodayLog();
    loadMyHistory();
    loadUsers();
    loadAttendance();
    loadAdminDashboard();
    loadAttendanceUserFilter();
    loadSettingsForm();
    loadProfileForm();
});
