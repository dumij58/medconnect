document.addEventListener("DOMContentLoaded", function() {
    const selectGender = document.getElementById("gender");
    const selectDOB = document.getElementById("dob");

    const addVitalSignsBtn = document.getElementById("add-vital-signs");
    const vitalSignsMessage = document.getElementById("vital-signs-message");

    const addExaminationNotesBtn = document.getElementById("add-examination-notes");
    const examinationNotesMessage = document.getElementById("examination-notes-message");

    const addOrderTestsBtn = document.getElementById("add-order-test");
    const orderTestsMessage = document.getElementById("order-test-message");

    const addTreatmentBtn = document.getElementById("add-treatment");
    const treatmentMessage = document.getElementById("treatment-message");

    const addMedicationBtn = document.getElementById("add-medications");
    const medicationMessage = document.getElementById("medications-message");

    const selectDoctor = document.getElementById("doctor");
    const extDoctorName = document.getElementById("external_doctor-0-doctor_name");
    const extDoctorSpecialization = document.getElementById("external_doctor-0-specialization");
    const extDoctorForm = document.getElementById("extDoctorForm");

    const chiefComplaint = document.getElementById("chief_complaint");
    const diagnosis = document.getElementById("diagnosis");

    const followUpCheck = document.getElementById("followUpCheck");
    const followUpDate = document.getElementById("follow_up_date");
    const followUpNotes = document.getElementById("follow_up_notes");
    const followUpMessage = document.getElementById("follow-up-message");

    const referralCheck = document.getElementById("referralCheck");
    const referralDate = document.getElementById("referral_date");
    const referralReason = document.getElementById("reason");
    const referralNotes = document.getElementById("referral_notes");
    // some variables related to referral form are assigned earlier
    const referralMessage = document.getElementById("referral-message");
    
    const endApmtBtn = document.getElementById("end-apmt");
    const endApmtMessage = document.getElementById("end-apmt-message");

    preSelectOption(selectGender);
    preSelectDate(selectDOB);

    addVitalSignsBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const sign = document.getElementById("vital_signs-0-sign");
        const value = document.getElementById("vital_signs-0-value");
        
        if (sign.value && value.value) {
            vitalSignsMessage.textContent = "";

            // Create vital signs data object
            const vitalSignsData = {
                sign: sign.value,
                value: value.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(vitalSignsData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#vital-signs-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            vitalSignsMessage.textContent = "*Please fill in all fields";
        }
        sign.value = "";
        value.value = "";
        
    });

    addExaminationNotesBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const title = document.getElementById("examination_notes-0-title");
        const notes = document.getElementById("examination_notes-0-notes");
        
        if (notes.value) {
            examinationNotesMessage.textContent = "";

            // Create examination notes data object
            const examinationNotesData = {
                title: title.value,
                notes: notes.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(examinationNotesData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#examination-notes-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            examinationNotesMessage.textContent = "*Examination notes field is required";
        }

        title.value = "";
        notes.value = "";
    });

    addOrderTestsBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const testName = document.getElementById("test_name");
        const additionalNotes = document.getElementById("additional_notes");
        
        if (testName.value) {
            orderTestsMessage.textContent = "";

            // Create examination notes data object
            const orderTestsData = {
                test_name: testName.value,
                additional_notes: additionalNotes.value
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(orderTestsData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#order-tests-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            orderTestsMessage.textContent = "*Test name field is required";
        }

        testName.value = "";
        additionalNotes.value = "";
    });

    addTreatmentBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const title = document.getElementById("treatments-0-title");
        const treatment_notes = document.getElementById("treatments-0-treatment_notes");
        
        if (treatment_notes.value) {
            treatmentMessage.textContent = "";

            // Create examination notes data object
            const treatmentData = {
                title: title.value,
                treatment_notes: treatment_notes.value,
            };

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(treatmentData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the displayed table with new data
                const tbody = document.querySelector("#treatments-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            treatmentMessage.textContent = "*Treatment notes field is required";
        }

        title.value = "";
        treatment_notes.value = "";
    });

    addMedicationBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-add-url");

        // Gather data from input fields
        const medicationName = document.getElementById("medications-0-medication_name");
        const dosage = document.getElementById("medications-0-dosage");
        const frequency = document.getElementById("medications-0-frequency");
        const pt_full_name = document.getElementById("full_name").getAttribute("placeholder");

        // Check if all fields are filled
        if (medicationName.value && dosage.value && frequency.value) {
            medicationMessage.textContent = "";

            // Create medication data object
            const medicationData = {
                medication_name: medicationName.value,
                dosage: dosage.value,
                frequency: frequency.value,
                pt_full_name: pt_full_name
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
                const tbody = document.querySelector("#medications-table tbody");
                tbody.insertAdjacentHTML("beforeend", data.row_html);
            });
        } else {
            medicationMessage.textContent = "*Please fill in all fields";
        }
        medicationName.value = "";
        dosage.value = "";
        frequency.value = "";
    });

    selectDoctor.addEventListener("change", function() {
        if (selectDoctor.value.trim() === "Other Doctor") {
            extDoctorName.disabled = false;
            extDoctorSpecialization.disabled = false;
            extDoctorForm.classList.add("show");
        } else {
            extDoctorName.disabled = true;
            extDoctorSpecialization.disabled = true;
            extDoctorForm.classList.remove("show");
        }
    })

    endApmtBtn.addEventListener("click", function() {
        // Get the URL from the data attribute
        const addUrl = this.getAttribute("data-submit-url");

        // Check if all fields are filled
        if (chiefComplaint.value && diagnosis.value) {
            endApmtMessage.textContent = "";

            // Create medication data object
            const apmtData = {
                chief_complaint: chiefComplaint.value,
                diagnosis: diagnosis.value
            };

            if (followUpCheck.checked) {
                if (followUpDate.value || followUpNotes.value) {
                    followUpMessage.textContent == "";
    
                    apmtData.follow_up_date = followUpDate.value;
                    apmtData.follow_up_notes = followUpNotes.value;
                } else {
                    followUpMessage.textContent == "*Either follow up date or follow up notes is required.";
                }
            }

            if (referralCheck.checked) {

                if (selectDoctor.value && referralDate.value && referralReason.value) {
                    referralMessage.textContent == "";

                    if (selectDoctor.value !== "Other Doctor") {
                        apmtData.doctor = selectDoctor.value;
                    } else {

                        if (extDoctorName.value && extDoctorSpecialization.value) {
                            apmtData.ext_doctor_name = extDoctorName.value;
                            apmtData.ext_doctor_specialization = extDoctorSpecialization.value;
                        } else {
                            referralMessage.textContent == "*Doctor's Name and Specialization fields are required.";
                        }

                    }

                    apmtData.referral_date = referralDate.value;
                    apmtData.referral_reason = referralReason.value;
                } else {
                    referralMessage.textContent == "*Doctor, referral date and referral reason fields are required.";
                }

            }

            // Send data to Flask route using fetch API
            fetch(addUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(apmtData)
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                if (data.status === 'success') {
                    // Redirect to another Flask route
                    window.location.href = data.redirect_url;
                }
            });
        } else {
            referralMessage.textContent = "*Chief complaint and diagnosis fields are required.";
        }
    });
});


function preSelectOption(selectField) {
    var selectedOptionValue = selectField.getAttribute("data-selected-option");

    for (var i = 0; i < selectField.options.length; i++) {
        if (selectField.options[i].value === selectedOptionValue) {
            selectField.options[i].selected = true;
            break;
        }
    }
}

function preSelectDate(dateField) {
    var selectedDateValue = dateField.getAttribute("data-selected-date");

    dateField.value = selectedDateValue;
}
