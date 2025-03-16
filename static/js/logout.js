document.addEventListener("DOMContentLoaded", function () {
    let logoutLink = document.querySelector("a[href='#']");
    if (logoutLink) {
        logoutLink.addEventListener("click", function (event) {
            event.preventDefault();  // 阻止默认跳转
            document.getElementById("logout-form").submit();
        });
    }
});
