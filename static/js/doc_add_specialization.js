document.addEventListener("DOMContentLoaded", function() {

    const addSpecializationBtn = document.getElementById("add-specialization");
    const specializationMessage = document.getElementById("specialization-message");

    addSpecializationBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const specialization = document.getElementById("specialization");
        
        if (specialization.value) {
            specializationMessage.textContent = "";
            // Create vaccination data object
            const specializationData = {
                specialization: specialization.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(specializationData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#specialization-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            specializationMessage.textContent = "*Please fill in all fields";
        }
        specialization.value = "";
    });

    const everyTableBody = document.querySelectorAll(".details-table tbody");
    // Attach event listener to the table body to handle "X" button clicks
    everyTableBody.forEach(tableBody => {
        tableBody.addEventListener("click", function(event) {
            const clickedButton = event.target;
            if (clickedButton.classList.contains("remove-button")) {
                handleRemoveButton(clickedButton);
            }
        });
    });
    
    function handleRemoveButton(button) {
        tableRow = button.closest("tr"); // Get the <tr> tag closest to the button
        entryId = tableRow.getAttribute("data-id");
        removeUrl = button.getAttribute("data-remove-url");

        // Create data object with id
        const data = {
            id: entryId,
        };

        // Send data to Flask route using fetch API
        fetch(removeUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Remove the table row
            tableRow.remove();
        });
    }
});