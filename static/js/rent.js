document.addEventListener("DOMContentLoaded", function () {
    let rentForm = document.getElementById("rentForm");
    let stationSelect = document.getElementById("rental_station");
    let selectedStationInput = document.getElementById("selected_station");

    rentForm.addEventListener("submit", function (event) {
        if (!stationSelect.value) {
            event.preventDefault();
            alert("Please select a rental station.");
        } else {
            selectedStationInput.value = stationSelect.value;
        }
    });
});
