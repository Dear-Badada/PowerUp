document.addEventListener("DOMContentLoaded", function () {
    const openModalBtn = document.getElementById("openConfirmModal");
    const confirmModal = document.getElementById("confirmActionModal");
    const confirmBtn = document.getElementById("confirmAction");
    const cancelBtn = document.getElementById("cancelAction");
    const form = document.getElementById("createStationForm");

    // 显示弹窗
    openModalBtn.addEventListener("click", function () {
        confirmModal.style.display = "block";
    });

    // 确认创建
    confirmBtn.addEventListener("click", function () {
        form.submit(); // 提交表单
    });

    // 监听表单提交，成功后跳转并刷新
    form.addEventListener("submit", function (event) {
        setTimeout(function () {
            window.location.href = "/manager/stations/";
        }, 1000);
    });

    // 取消操作
    cancelBtn.addEventListener("click", function () {
        confirmModal.style.display = "none";
    });

    // 点击窗口外部关闭弹窗
    window.addEventListener("click", function (event) {
        if (event.target === confirmModal) {
            confirmModal.style.display = "none";
        }
    });
});
