document.addEventListener('DOMContentLoaded', function () {
    const rechargeBtn = document.getElementById('rechargeBtn');
    const globalModal = new bootstrap.Modal(document.getElementById('globalModal'));
    const globalModalBody = document.getElementById('globalModalBody');
    const globalModalConfirm = document.getElementById('globalModalConfirm');

    if (!rechargeBtn) {
        console.error("Recharge button not found.");
        return;
    }
    if (!globalModal) {
        console.error("Global Modal not found.");
        return;
    }

    rechargeBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const amount = document.getElementById('amount').value;

        if (!amount || parseFloat(amount) < 15.00) {
            globalModalBody.textContent = "The amount entered is below the minimum recharge of £15.00.";
            globalModal.show();
            return;
        }

        globalModalBody.textContent = "Are you sure you want to recharge £" + amount + "?";
        globalModal.show();

        globalModalConfirm.onclick = function () {
            const form = document.getElementById('rechargeForm');
            form.submit(); // 提交表单
        }
    });
});