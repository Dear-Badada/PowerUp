document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".rent-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let rentUrl = this.getAttribute("data-url");
            if (!rentUrl) return;

            showActionModal(this.getAttribute("data-message"), function () {
                window.location.href = rentUrl;
            });
        });
    });

    // 统一 Low 按钮的弹窗
    document.querySelectorAll(".btn-low-battery").forEach(button => {
        button.addEventListener("click", function () {
            showActionModal("This power bank's battery is too low to rent. Please choose another one.");
        });
    });
});
