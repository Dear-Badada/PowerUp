document.addEventListener("DOMContentLoaded", function () {
    // 监听 Rent 按钮
    document.querySelectorAll(".rent-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // 防止默认跳转

            let rentUrl = this.getAttribute("data-rent-url"); // 获取租借 URL
            if (!rentUrl) return;

            let userConfirmed = confirm("Do you want to rent this power bank? Your deposit will be charged.");
            if (userConfirmed) {
                window.location.href = rentUrl; // 只有用户确认后才跳转
            }
        });
    });

    // 监听低电量按钮
    document.querySelectorAll(".low-battery-btn").forEach(button => {
        button.addEventListener("click", function () {
            alert("This power bank has low battery. Please choose another one.");
        });
    });

    // 监听未登录用户点击 Rent 按钮
    document.querySelectorAll(".not-logged-in").forEach(button => {
        button.addEventListener("click", function () {
            alert("You must be logged in to rent a power bank.");
        });
    });
});
