document.addEventListener("DOMContentLoaded", function() {
    // 获取充电宝状态 & 按钮
    const powerBankStatusElement = document.querySelector(".power-bank-status");
    const returnButton = document.querySelector(".return-btn");
    const stationButton = document.querySelector(".station-btn");
    const modal = new bootstrap.Modal(document.getElementById("globalModal"));
    const confirmButton = document.getElementById("globalModalConfirm");

    if (powerBankStatusElement) {
        let powerBankStatus = powerBankStatusElement.innerText.trim().toLowerCase();

        console.log("Power Bank Status:", powerBankStatus);

        if (powerBankStatus === "available") {
            if (returnButton) returnButton.style.display = "none"; // 归还后隐藏 "Return"
            if (stationButton) {
                stationButton.style.display = "block";
                stationButton.style.visibility = "visible";
            }

            showMessage("Power Bank returned successfully!");
        }
    }

    // 监听 "Return" 按钮点击事件
    if (returnButton) {
        returnButton.addEventListener("click", function(event) {
            event.preventDefault(); // 阻止默认跳转行为
            let returnUrl = this.getAttribute("href");

            showModal(
                "Confirm Return",
                "Are you sure you want to return the power bank?",
                "Return"
            );

            confirmButton.onclick = function() {
                // 点击确认后隐藏按钮，并跳转
                if (returnButton) returnButton.style.display = "none";
                window.location.href = returnUrl;
            };

            modal.show();
        });
    }
});

function showModal(title, message, confirmText) {
    document.getElementById("globalModalLabel").textContent = title;
    document.getElementById("globalModalBody").textContent = message;
    document.getElementById("globalModalConfirm").textContent = confirmText;
}
