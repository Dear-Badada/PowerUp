document.addEventListener("DOMContentLoaded", function () {
    let feedbackForm = document.getElementById("feedbackForm");

    feedbackForm.addEventListener("submit", function (event) {
        let feedbackType = document.getElementById("feedback_type").value;
        let message = document.getElementById("message").value.trim();

        if (!feedbackType || !message) {
            event.preventDefault();
            alert("Please select a feedback type and enter a message.");
        }
    });
});
