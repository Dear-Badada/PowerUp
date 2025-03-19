document.addEventListener("DOMContentLoaded", function () {
    let globalModal = new bootstrap.Modal(document.getElementById("globalModal"));
    let globalModalBody = document.getElementById("globalModalBody");
    let confirmActionButton = document.getElementById("globalModalConfirm");

    let actionCallback = null; // 存储当前的操作

    // 监听所有带 data-confirm 属性的按钮
    document.querySelectorAll("[data-confirm]").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let message = this.getAttribute("data-message") || "Are you sure you want to proceed?";
            let actionUrl = this.getAttribute("data-url");

            globalModalBody.textContent = message;
            globalModal.show();

            // 记录用户确认后的操作
            actionCallback = function () {
                if (actionUrl) {
                    window.location.href = actionUrl;
                }
            };
        });
    });

    // 用户点击确认按钮时执行操作
    confirmActionButton.addEventListener("click", function () {
        if (actionCallback) {
            actionCallback();
        }
        globalModal.hide();
    });
});

// 低电量弹窗
function alertLowBattery() {
    alert("Battery too low to rent. Please choose another.");
}

// 未登录用户点击 Rent 按钮的弹窗
function alertNotLoggedIn() {
    alert("You must log in to rent a power bank.");
    window.location.href = "/login";  // 重定向到登录页面
}

// 让全局可用
window.alertLowBattery = alertLowBattery;
window.alertNotLoggedIn = alertNotLoggedIn;