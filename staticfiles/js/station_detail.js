document.addEventListener("DOMContentLoaded", function () {
    const modal = new bootstrap.Modal(document.getElementById("globalModal"));
    const confirmButton = document.getElementById("globalModalConfirm");

    // 租借按钮的处理
    document.querySelectorAll(".btn-rent").forEach(button => {
        button.addEventListener("click", function () {
            const rentUrl = this.getAttribute("data-url");
            if (!rentUrl) return;

            showModal("⚠️ Rent Power Bank", this.getAttribute("data-message"), "Rent");

            confirmButton.onclick = function () {
                window.location.href = rentUrl;
            };

            modal.show();
        });
    });

    // 低电量按钮的处理
    document.querySelectorAll(".btn-low-battery").forEach(button => {
        button.addEventListener("click", function () {
            showModal("Low Battery Warning", "This power bank's battery is too low to rent. Please choose another one.", "OK");

            confirmButton.onclick = function () {
                modal.hide(); // 确认按钮被点击后关闭模态框
            };

            modal.show();
        });
    });

    function showModal(title, message, confirmText) {
        document.getElementById("globalModalLabel").textContent = title;
        document.getElementById("globalModalBody").textContent = message;
        confirmButton.textContent = confirmText;
    }
});
