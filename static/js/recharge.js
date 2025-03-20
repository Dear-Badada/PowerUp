document.addEventListener("DOMContentLoaded", function() {
    const rechargeButton = document.getElementById("rechargeBtn");
    const globalModalElement = document.getElementById('globalModal');
    const globalModal = new bootstrap.Modal(globalModalElement);
    const confirmButton = document.getElementById("globalModalConfirm");
    const cancelButton = document.querySelector(".btn-cancel");

    if (rechargeButton) {
        rechargeButton.addEventListener("click", function(event) {
            event.preventDefault();

            const amountInput = document.getElementById("amount");
            const amountValue = amountInput.value;
            const minimumRecharge = parseFloat(amountInput.getAttribute("data-deposit"));

            // 判断金额是否符合最低充值要求
            if (!amountValue || parseFloat(amountValue) < minimumRecharge) {
                document.getElementById('globalModalBody').textContent =
                    `The minimum recharge amount is £${minimumRecharge}. Please enter a valid amount.`;
                confirmButton.style.display = "none";
                globalModal.show();
                return;
            }

            // 询问用户是否确定充值
            document.getElementById('globalModalBody').textContent =
                "Are you sure you want to proceed with the recharge?";
            confirmButton.style.display = "block";
            globalModal.show();

            confirmButton.onclick = function () {
                const csrftoken = getCookie('csrftoken');

                fetch('/recharge/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ amount: amountValue })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('globalModalBody').textContent = "Recharge successful!";
                        cancelButton.style.display = "none";
                        globalModal.show();
                        // 点击确认按钮后刷新页面
                        confirmButton.textContent = "OK";
                        confirmButton.onclick = function() {
                            location.reload(); // 刷新页面
                        };
                    } else {
                        // 充值失败，显示错误信息
                        document.getElementById('globalModalBody').textContent = `Error: ${data.error}`;
                        confirmButton.style.display = "none"; // 隐藏确认按钮
                        globalModal.show();

                        // 点击取消按钮关闭弹窗
                        cancelButton.textContent = "Close";
                        cancelButton.onclick = function() {
                            globalModal.hide();
                        };
                    }
                })
                .catch(error => {
                    // 捕获任何错误
                    document.getElementById('globalModalBody').textContent = `Error: ${error}`;
                    confirmButton.style.display = "none";
                    globalModal.show();

                    cancelButton.textContent = "Close";
                    cancelButton.onclick = function() {
                        globalModal.hide();
                    };
                });
            };
        });
    }
    // 点击取消按钮关闭弹窗
    if (cancelButton) {
        cancelButton.addEventListener("click", function() {
            globalModal.hide();
        });
    }
});

// 获取 CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}