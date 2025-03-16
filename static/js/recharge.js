function submitRecharge() {
    let amountInput = document.getElementById("amount");
    let amount = amountInput.value.trim();

    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
        alert("Please enter a valid number greater than 0.");
        return;
    }

    fetch(window.location.pathname, {  // 发送请求到当前 URL
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // 获取 CSRF 令牌
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Recharge successful! New balance: £${data.new_balance}`);

            // **自动跳转到 `redirect_url`，如果存在**
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                location.reload();  // 如果没有跳转 URL，则刷新页面
            }
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Recharge failed. Please try again.");
    });
}

// 获取 CSRF 令牌的函数（Django 需要）
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
