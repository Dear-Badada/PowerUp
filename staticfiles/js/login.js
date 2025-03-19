document.addEventListener("DOMContentLoaded", function () {
    let loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function (event) {
        let username = document.getElementById("username").value.trim();
        let password = document.getElementById("password").value.trim();

        if (!username || !password) {
            event.preventDefault();
            alert("Please enter both username/email and password.");
        }
    });
});
