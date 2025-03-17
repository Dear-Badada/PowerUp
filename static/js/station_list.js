document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-station-btn");
    const modal = document.getElementById("confirmDeleteModal");
    const confirmDeleteButton = document.getElementById("confirmDelete");
    const cancelDeleteButton = document.getElementById("cancelDelete");
    let stationId = null;

    // 监听删除按钮
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            stationId = this.getAttribute("data-id");
            modal.style.display = "block";
        });
    });

    // 确认删除
    confirmDeleteButton.addEventListener("click", function () {
        if (stationId) {
            window.location.href = `/manager/stations/${stationId}/delete/`;
        }
    });

    // 取消删除
    cancelDeleteButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // 点击外部关闭弹窗
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
