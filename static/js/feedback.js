document.addEventListener("DOMContentLoaded", function () {
    let feedbackForm = document.getElementById("feedbackForm");
    let feedbackType = document.getElementById("feedback_type");
    let refundWarning = document.getElementById("refund-warning");

    // 监听选择框变化
    feedbackType.addEventListener("change", function () {
        if (feedbackType.value === "abnormal") {
            refundWarning.style.display = "block"; // 显示警告信息
        } else {
            refundWarning.style.display = "none";  // 隐藏警告信息
        }
    });

    feedbackForm.addEventListener("submit", function (event) {
        let message = document.getElementById("message").value.trim();

        if (!feedbackType.value || !message) {
            event.preventDefault();
            alert("Please select a feedback type and enter a message.");
        }
    });
});
