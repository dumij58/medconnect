document.addEventListener("DOMContentLoaded", function() {

    const addMedicalHistoryBtn = document.getElementById("add-medical-history");
    const medicalHistoryMessage = document.getElementById("medical-history-message");
    
    const addMedicationBtn = document.getElementById("add-medication");
    const medicationMessage = document.getElementById("medication-message");

    const addSurgeryBtn = document.getElementById("add-surgery");
    const surgeryMessage = document.getElementById("surgery-message");

    const addVaccinationBtn = document.getElementById("add-vaccination");
    const vaccinationMessage = document.getElementById("vaccination-message");

    const addFamilyHistoryBtn = document.getElementById("add-family-history");
    const familyHistoryMessage = document.getElementById("family-history-message");

    addMedicalHistoryBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const medicalCondition = document.getElementById("medical_history-0-medical_condition");
        const diagnosisDate = document.getElementById("medical_history-0-diagnosis_date");
        const treatment = document.getElementById("medical_history-0-treatment");
        
        if (medicalCondition.value && diagnosisDate.value && treatment.value) {
            medicalHistoryMessage.textContent = "";
            // Create vaccination data object
            const medicalHistoryData = {
                medical_condition: medicalCondition.value,
                diagnosis_date: diagnosisDate.value,
                treatment: treatment.value
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(medicalHistoryData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#medical-history-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            medicalHistoryMessage.textContent = "*Please fill in all fields";
        }
        medicalCondition.value = "";
        diagnosisDate.value = "";
        treatment.value = "";
    });

    addMedicationBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const medicationName = document.getElementById("current_medications-0-medication_name");
        const dosage = document.getElementById("current_medications-0-dosage");
        const frequency = document.getElementById("current_medications-0-frequency");
        const startDate = document.getElementById("current_medications-0-start_date");

        // Check if all fields are filled
        if (medicationName.value && dosage.value && frequency.value && startDate.value) {
            medicationMessage.textContent = "";

            // Create medication data object
            const medicationData = {
                medication_name: medicationName.value,
                dosage: dosage.value,
                frequency: frequency.value,
                start_date: startDate.value
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(medicationData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#medication-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            medicationMessage.textContent = "*Please fill in all fields";
        }
        medicationName.value = "";
        dosage.value = "";
        frequency.value = "";
        startDate.value = "";

    });

    addSurgeryBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const surgeryName = document.getElementById("past_surgeries-0-surgery_name");
        const date = document.getElementById("past_surgeries-0-date");
        const notes = document.getElementById("past_surgeries-0-notes");
        
        if (surgeryName.value && date.value) {
            surgeryMessage.textContent = "";

            // Create surgery data object
            const surgeryData = {
                surgery_name: surgeryName.value,
                date: date.value,
                notes: notes.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(surgeryData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#surgery-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            surgeryMessage.textContent = "*Please fill in Surgery name & Date";
        }
        surgeryName.value = "";
        date.value = "";
        notes.value = "";
    });

    addVaccinationBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const vaccineName = document.getElementById("vaccinations-0-vaccine_name");
        const administrationDate = document.getElementById("vaccinations-0-administration_date");
        const notes = document.getElementById("vaccinations-0-notes");
        
        if (vaccineName.value && administrationDate.value) {
            vaccinationMessage.textContent = "";
            // Create vaccination data object
            const vaccinationData = {
                vaccine_name: vaccineName.value,
                administration_date: administrationDate.value,
                notes: notes.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(vaccinationData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#vaccination-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            vaccinationMessage.textContent = "*Please fill in Vaccine name & Administration date";
        }
        vaccineName.value = "";
        administrationDate.value = "";
        notes.value = "";
    });

    addFamilyHistoryBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const relationship = document.getElementById("family_medical_history-0-relationship");
        const medicalCondition = document.getElementById("family_medical_history-0-medical_condition");
        
        if (relationship.value && medicalCondition.value) {
            familyHistoryMessage.textContent = "";
            // Create vaccination data object
            const familyHistoryData = {
                relationship: relationship.value,
                medical_condition: medicalCondition.value
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(familyHistoryData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#family-history-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            familyHistoryMessage.textContent = "*Please fill in all fields";
        }
        relationship.value = "";
        medicalCondition.value = "";
    });

    // Add click event listener to all Remove buttons
    const removeButtons = document.querySelectorAll(".remove-button");
    removeButtons.forEach(button => {
        button.addEventListener("click", function() {
            const tableRow = button.closest("tr"); // Get the <tr> tag closest to the button
            const entryId = tableRow.getAttribute("data-id");
            const rowType = tableRow.getAttribute("data-row-type");
            const removeUrl = button.getAttribute("data-remove-url");

            // Create data object with id and type
            const data = {
                id: entryId,
                type: rowType
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
        });
    });

});