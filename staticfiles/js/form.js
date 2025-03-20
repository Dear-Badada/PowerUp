document.addEventListener("DOMContentLoaded", function () {
    const registerBtn = document.getElementById("registerBtn");
    const registerForm = document.getElementById("registerForm");

    if (registerBtn && registerForm) {
        registerBtn.addEventListener("click", function () {
            const username = document.getElementById("id_username").value;
            const password = document.getElementById("id_password").value;
            const confirmPassword = document.getElementById("confirm_password").value;

            if (username.length < 3) {
                alert("Username must be at least 3 characters long.");
                return;
            }

            if (password.length < 6) {
                alert("Password must be at least 6 characters long.");
                return;
            }

            if (password !== confirmPassword) {
                alert("Passwords do not match.");
                return;
            }

            // 确认注册弹窗
            const confirmAction = confirm("Are you sure you want to register with the provided information?");
            if (confirmAction) {
                registerForm.submit();
            }
        });
    }
});