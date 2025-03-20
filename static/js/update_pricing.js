document.addEventListener('DOMContentLoaded', function () {
    const showModalBtn = document.getElementById('showModalBtn');
    const globalModalConfirm = document.getElementById('globalModalConfirm');

    if (showModalBtn && globalModalConfirm) {
        showModalBtn.addEventListener('click', function () {

            // 设置模态框的内容
            document.getElementById('globalModalLabel').innerText = "Confirm Price Update";
            document.getElementById('globalModalBody').innerText = "Are you sure you want to update the pricing information?";

            // 显示模态框
            var globalModal = new bootstrap.Modal(document.getElementById('globalModal'), {
                backdrop: 'static',
                keyboard: false
            });
            globalModal.show();
        });

        // 当用户点击确认按钮时，提交表单
        globalModalConfirm.addEventListener('click', function () {
            document.getElementById('pricingForm').submit();
        });
    }
});
