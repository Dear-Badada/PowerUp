document.addEventListener("DOMContentLoaded", function () {
    let returnForm = document.getElementById("returnForm");
    if (returnForm) {
        returnForm.addEventListener("submit", function (event) {
            event.preventDefault();
            showActionModal("Are you sure you want to return the power bank?", function () {
                returnForm.submit();
            });
        });
    }
});
