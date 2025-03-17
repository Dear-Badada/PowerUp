document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const repairButtons = document.querySelectorAll(".repair-btn");
    const modal = document.getElementById("confirmDeleteModal");
    const confirmDeleteButton = document.getElementById("confirmDelete");
    const cancelDeleteButton = document.getElementById("cancelDelete");
    let powerBankId = null;

    // 监听删除按钮
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.getAttribute("data-id");
            modal.style.display = "block";
        });
    });

    // 确认删除
    confirmDeleteButton.addEventListener("click", function () {
        if (powerBankId) {
            window.location.href = `/manager/powerbanks/${powerBankId}/delete/`;
        }
    });

    // 取消删除
    cancelDeleteButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // 监听维修按钮
    repairButtons.forEach(button => {
        button.addEventListener("click", function () {
            let powerBankId = this.getAttribute("data-id");
            fetch(`/manager/powerbanks/${powerBankId}/repair/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();  // 修复后刷新页面
                } else {
                    alert("Failed to repair power bank.");
                }
            });
        });
    });

    // 获取 CSRF 令牌
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});