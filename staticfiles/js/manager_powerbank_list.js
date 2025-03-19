document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("confirmActionModal");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    let actionType = "";
    let powerBankId = null;

    // 监听所有操作按钮
    document.querySelectorAll(".delete-btn, .repair-btn, .update-btn").forEach(button => {
        button.addEventListener("click", function () {
            powerBankId = this.dataset.id;
            actionType = this.classList.contains("delete-btn") ? "delete" :
                         this.classList.contains("repair-btn") ? "repair" : "update";

            const messages = {
                delete: ["⚠️ Delete Power Bank", "This action cannot be undone!", "Delete"],
                repair: ["🛠 Repair Power Bank", "This action will mark it as repaired.", "Confirm"],
                update: ["🔄 Update Power Bank", "This action will update the power bank status.", "Update"]
            };

            showModal(...messages[actionType]);
        });
    });

    // 处理确认操作
    confirmButton.addEventListener("click", async function () {
        if (!powerBankId) {
            console.error("No power bank ID found for action.");
            return;
        }

        let urlMap = {
            delete: `/manager/powerbanks/${powerBankId}/delete/`,
            repair: `/manager/powerbanks/${powerBankId}/repair/`,
            update: `/manager/powerbanks/${powerBankId}/update-status/`
        };

        if (actionType === "update") {
            window.location.href = urlMap.update;
            return;
        }

        try {
            let response = await fetch(urlMap[actionType], {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/json"
                }
            });
            let data = await response.json();

            if (data.success) {
                window.location.reload();
            } else {
                alert(`❌ Failed to ${actionType} power bank.`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("⚠️ An error occurred while processing the action.");
        }
        modal.style.display = "none";
    });

    // 取消操作
    cancelButton.addEventListener("click", () => (modal.style.display = "none"));

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