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
    const logoutBtn = document.querySelector(".logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (event) {
            event.preventDefault(); // 防止默认提交行为
            fetch("/logout/", { method: "POST", credentials: "same-origin", headers: { "X-CSRFToken": getCSRFToken() } })
                .then(response => {
                    if (response.ok) {
                        window.location.href = "/"; // 跳转到 home 页
                    } else {
                        console.error("Logout failed");
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    }

    // 获取 CSRF Token（Django 需要）
    function getCSRFToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});
