document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const repairButtons = document.querySelectorAll(".repair-btn");
    const updateButtons = document.querySelectorAll(".update-btn");

    const modal = document.getElementById("confirmActionModal");
    const confirmActionButton = document.getElementById("confirmAction");
    const cancelActionButton = document.getElementById("cancelAction");
    let actionType = "";
    let powerBankId = null;

    // 监听修复按钮
    repairButtons.forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.getAttribute("data-id");
            actionType = "repair";
            showModal("Confirm Repair", "Are you sure you want to repair this power bank?");
        });
    });

    // 监听删除按钮
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.getAttribute("data-id");
            actionType = "delete";
            showModal("Confirm Delete", "Are you sure you want to delete this power bank?");
        });
    });

    // 监听更新状态按钮
    updateButtons.forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.getAttribute("data-id");
            window.location.href = `/manager/powerbanks/${powerBankId}/update-status/`;
        });
    });

    // 统一模态框按钮点击事件
    confirmActionButton.addEventListener("click", function () {
        if (powerBankId) {
            if (actionType === "delete") {
                fetch(`/manager/powerbanks/${powerBankId}/delete/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    }
                }).then(response => response.json())
                  .then(data => {
                      if (data.success) {
                          window.location.reload();
                      } else {
                          alert("Failed to delete power bank.");
                      }
                  });
            } else if (actionType === "repair") {
                fetch(`/manager/powerbanks/${powerBankId}/repair/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    }
                }).then(response => response.json())
                  .then(data => {
                      if (data.success) {
                          window.location.reload();
                      } else {
                          alert("Failed to repair power bank.");
                      }
                  });
            }
            modal.style.display = "none";
        }
    });

    cancelActionButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    function showModal(title, message) {
        document.getElementById("actionTitle").textContent = title;
        document.getElementById("actionMessage").textContent = message;
        modal.style.display = "block";
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
