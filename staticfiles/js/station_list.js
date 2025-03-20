document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-station-btn");
    const modal = new bootstrap.Modal(document.getElementById("globalModal"));
    const confirmButton = document.getElementById("globalModalConfirm");
    let stationId = null;

    // 监听删除按钮
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            stationId = this.getAttribute("data-id");
            if (!stationId) {
                console.error("Station ID is missing.");
                return;
            }
            showModal("⚠️ Are you sure you want to delete this station?", "This action cannot be undone!", "Delete");
            modal.show();
        });
    });

    // 确认删除操作
    confirmButton.addEventListener("click", function () {
        if (!stationId) {
            console.error("No station ID found for deletion.");
            return;
        }

        fetch(`/manager/stations/${stationId}/delete/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to delete station.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert("Deletion failed: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting. Please try again.");
        });

        modal.hide();
    });

    function showModal(title, message, confirmText) {
        document.getElementById("globalModalLabel").textContent = title;
        document.getElementById("globalModalBody").textContent = message;
        confirmButton.textContent = confirmText;
    }

    function getCSRFToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});
