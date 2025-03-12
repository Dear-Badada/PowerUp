document.addEventListener("DOMContentLoaded", function () {
    let adminLoginForm = document.getElementById("adminLoginForm");

    adminLoginForm.addEventListener("submit", function (event) {
        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("password").value.trim();

        if (!username || !password) {
            event.preventDefault();
            alert("Please enter both username and password.");
        }
    });
});
