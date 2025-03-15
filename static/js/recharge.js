function submitRecharge() {
    let amountInput = document.getElementById("amount");
    let amount = amountInput.value.trim();

    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
        alert("Please enter a valid number greater than 0.");
        return;
    }

    fetch("/recharge/", {
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
            location.reload();  // 重新加载页面更新余额
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

// 获取 CSRF 令牌的函数（Django 需要）
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
