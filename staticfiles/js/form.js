document.addEventListener("DOMContentLoaded", function () {
    let loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;

            if (username.length < 3) {
                document.getElementById("error-message").innerText = "Username must be at least 3 characters long.";
                event.preventDefault();
            } else if (password.length < 6) {
                document.getElementById("error-message").innerText = "Password must be at least 6 characters long.";
                event.preventDefault();
            }
        });
    }

    let registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;
            let confirmPassword = document.getElementById("confirm_password").value;

            if (username.length < 3) {
                alert("Username must be at least 3 characters long.");
                event.preventDefault();
            } else if (password.length < 6) {
                alert("Password must be at least 6 characters long.");
                event.preventDefault();
            } else if (password !== confirmPassword) {
                alert("Passwords do not match.");
                event.preventDefault();
            }
        });
    }
});
