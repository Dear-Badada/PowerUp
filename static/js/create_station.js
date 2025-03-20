document.addEventListener("DOMContentLoaded", function () {
    const openModalBtn = document.getElementById("openConfirmModal");
    const form = document.getElementById("createStationForm");
    const modal = new bootstrap.Modal(document.getElementById("globalModal"));
    const confirmButton = document.getElementById("globalModalConfirm");

    // 打开模态框
    openModalBtn.addEventListener("click", function () {
        showModal("⚠️ Are you sure you want to create this station?", "This action will create a new station.", "Create");
        modal.show();
    });

    // 确认创建操作
    confirmButton.addEventListener("click", function () {
        form.submit(); // 提交表单
    });

    function showModal(title, message, confirmText) {
        document.getElementById("globalModalLabel").textContent = title;
        document.getElementById("globalModalBody").textContent = message;
        confirmButton.textContent = confirmText;
    }
});
