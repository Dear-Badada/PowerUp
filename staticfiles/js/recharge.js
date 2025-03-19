document.addEventListener("DOMContentLoaded", function () {
    let rechargeForm = document.getElementById("rechargeForm");
    if (rechargeForm) {
        rechargeForm.addEventListener("submit", function (event) {
            event.preventDefault();
            showActionModal("Are you sure you want to recharge your wallet?", function () {
                rechargeForm.submit();
            });
        });
    }
});
