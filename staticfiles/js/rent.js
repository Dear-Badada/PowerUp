document.addEventListener("DOMContentLoaded", function () {
    let rentButton = document.getElementById("rentButton");
    let powerbankSelect = document.getElementById("powerbankSelect");

    rentButton.addEventListener("click", function () {
        let selectedPowerbank = powerbankSelect.value;

        if (!selectedPowerbank) {
            alert("Please select a power bank before renting.");
        } else {
            window.location.href = `/rent/${selectedPowerbank}/`;
        }
    });
});
