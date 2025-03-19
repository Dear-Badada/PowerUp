document.addEventListener("DOMContentLoaded", function () {
    // 颜色调整逻辑（保持原样）
    const statuses = document.querySelectorAll(".status-text");
    statuses.forEach(status => {
        if (status.innerText.toLowerCase() === "available") {
            status.classList.add("text-success");
        } else if (status.innerText.toLowerCase() === "rented") {
            status.classList.add("text-warning");
        } else {
            status.classList.add("text-danger");
        }
    });

    // 监听 Logout 按钮
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            fetch("/logout/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = "/login/"; // 退出后跳转到登录页
                } else {
                    alert("⚠️ Logout failed. Please try again.");
                }
            })
            .catch(error => {
                console.error("Logout error:", error);
                alert("⚠️ An error occurred while logging out.");
            });
        });
    }

    // 获取 CSRF Token（Django 需要）
    function getCSRFToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});