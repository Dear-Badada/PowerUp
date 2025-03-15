// 低电量按钮弹窗逻辑
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