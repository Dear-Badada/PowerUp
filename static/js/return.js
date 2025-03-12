document.addEventListener("DOMContentLoaded", function () {
    let returnForm = document.getElementById("returnForm");

    if (returnForm) {
        returnForm.addEventListener("submit", function (event) {
            event.preventDefault();

            let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            fetch('/api/return_powerbank/', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Power bank returned successfully! Redirecting to payment page...");
                    window.location.href = "/payment/";
                } else {
                    alert("Error returning power bank: " + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
