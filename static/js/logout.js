function logout() {
    fetch('/logout/', { method: 'POST', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("You have been logged out!");
                window.location.href = "/";
            }
        })
        .catch(error => console.error("Logout Error:", error));
}

function logoutAdmin() {
    fetch('/admin_logout/', { method: 'POST', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Admin has been logged out!");
                window.location.href = "/admin-login/";
            }
        })
        .catch(error => console.error("Admin Logout Error:", error));
}
