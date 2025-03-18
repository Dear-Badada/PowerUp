document.addEventListener("DOMContentLoaded", function () {
    const actionButtons = document.querySelectorAll(".delete-btn, .repair-btn, .update-btn");
    const modal = document.getElementById("confirmActionModal");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    let actionType = "";
    let powerBankId = null;

    // 监听按钮点击
    actionButtons.forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.getAttribute("data-id");

            if (this.classList.contains("delete-btn")) {
                actionType = "delete";
                showModal("⚠️ Are you sure delete this power bank?", "This action cannot be undone!", "Delete");
            } else if (this.classList.contains("repair-btn")) {
                actionType = "repair";
                showModal("⚠️ Are you sure repair this power bank?", "This action will mark it as repaired.", "Confirm");
            } else if (this.classList.contains("update-btn")) {
                actionType = "update";
                showModal("⚠️ Are you sure update this power bank?", "This action will update the status of the power bank.", "Update");
            }
        });
    });

    // 确认操作
    confirmButton.addEventListener("click", function () {
        if (!powerBankId) {
            console.error("No power bank ID found for action.");
            return;
        }

        let url = "";
        if (actionType === "delete") {
            url = `/manager/powerbanks/${powerBankId}/delete/`;
        } else if (actionType === "repair") {
            url = `/manager/powerbanks/${powerBankId}/repair/`;
        } else if (actionType === "update") {
            window.location.href = `/manager/powerbanks/${powerBankId}/update-status/`;
            return;
        }

        if (url) {
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert(`Failed to ${actionType} power bank.`);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while processing the action.");
            });
        }
        modal.style.display = "none";
    });

    cancelButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    function showModal(title, message, confirmText) {
        document.getElementById("actionTitle").textContent = title;
        document.getElementById("actionMessage").textContent = message;
        document.getElementById("confirmAction").textContent = confirmText;
        modal.style.display = "block";
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});