document.addEventListener("DOMContentLoaded", function() {
    // 获取充电宝状态 & 按钮
    const powerBankStatusElement = document.querySelector(".power-bank-status");
    const returnButton = document.querySelector(".return-btn");
    const stationButton = document.querySelector(".station-btn");

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

    // 监听 "Return" 按钮点击事件，让它立即消失
    if (returnButton) {
        returnButton.addEventListener("click", function(event) {
            event.preventDefault(); // 防止默认跳转
            let returnUrl = this.getAttribute("href"); // 获取归还 URL

            let userConfirmed = confirm("Are you sure you want to return the power bank?");
            if (userConfirmed) {
                window.location.href = returnUrl; // ✅ 确认后跳转到归还页面
            }
        });
    }
    showDjangoMessages();
});

function showDjangoMessages() {
    let messagesContainer = document.getElementById("django-messages");
    if (messagesContainer) {
        let messages = messagesContainer.getElementsByClassName("message");
        for (let message of messages) {
            let messageText = message.innerText;
            showMessage(messageText);
        }
    }
}

function showMessage(message) {
    let messageDiv = document.createElement("div");
    messageDiv.className = "alert alert-success";
    messageDiv.innerText = message;
    document.body.appendChild(messageDiv);

    // 3 秒后自动隐藏
    setTimeout(() => {
        messageDiv.style.display = "none";
    }, 3000);
}