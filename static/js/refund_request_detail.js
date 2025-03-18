document.addEventListener("DOMContentLoaded", function () {
    const approveBtn = document.querySelector(".btn-approve");
    const rejectBtn = document.querySelector(".btn-reject");

    if (approveBtn) {
        approveBtn.addEventListener("click", function (event) {
            let confirmAction = confirm("Are you sure you want to APPROVE this refund?");
            if (!confirmAction) {
                event.preventDefault(); // 取消提交
            }
        });
    }

    if (rejectBtn) {
        rejectBtn.addEventListener("click", function (event) {
            let confirmAction = confirm("Are you sure you want to REJECT this refund?");
            if (!confirmAction) {
                event.preventDefault(); // 取消提交
            }
        });
    }
});
