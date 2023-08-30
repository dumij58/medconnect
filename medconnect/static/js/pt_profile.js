const unameField = document.getElementById("username");
const chngUname = document.getElementById("edit-uname-button");
const submitUname = document.getElementById("submit-uname-button");
const unameMessage = document.getElementById("uname-message");
let isUnameEditable = false;

const selectGender = document.getElementById("gender");
const selectDOB = document.getElementById("dob");
const editButton = document.getElementById("edit-button");
const saveButton = document.getElementById("save-button");
const personalInfoInputs = document.querySelectorAll("#personal-info input");
const form = document.querySelector("form");
let isEditable = false;

document.addEventListener("DOMContentLoaded", function() {

    preSelectOption(selectGender);
    preSelectDate(selectDOB);

    chngUname.addEventListener("click", function() {
        isUnameEditable = !isUnameEditable;
        if (isUnameEditable) {
            editUname();
        } else {
            cancelEditingUname();
        }
    });

    editButton.addEventListener("click", function() {
        isEditable = !isEditable;
        if (isEditable) {
            editDetails();
        } else {
            cancelEditing();
        }
    });

    // Handle form submission when "Save Details" button is clicked
    const submitUrl = form.getAttribute("action");
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        saveDetails(submitUrl);
    });

    submitUname.addEventListener("click", function() {
        updateUname();
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

function editDetails() {
    selectGender.disabled = false;
    saveButton.hidden = false;
    editButton.textContent = "Cancel";
    editButton.classList.remove("btn-primary");
    editButton.classList.add("btn-danger");
    personalInfoInputs.forEach(input => {
        input.disabled = false;
        input.addEventListener("input", function() {
            saveButton.disabled = false;
        });
    });
}

function cancelEditing() {
    personalInfoInputs.forEach(input => {
        input.disabled = true;
        input.value = "";
    });
    selectGender.disabled = true;
    saveButton.hidden = true;
    saveButton.disabled = true;
    editButton.textContent = "Edit Details";
    editButton.classList.remove("btn-danger");
    editButton.classList.add("btn-primary");
    isEditable = false;
    preSelectOption(selectGender);
    preSelectDate(selectDOB);
}

function saveDetails(url) {
    const formData = new FormData(form);

    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Send data to the server using fetch API
    fetch(url, {
        method: "POST",
        headers: {
            // Set the correct Content-Type header here
            "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle success or display error message
        if (data.full_name != null) {
            document.getElementById("full_name").setAttribute("placeholder", data.full_name);
        }
        if (data.gender != null) {
            selectGender.setAttribute("data-selected-option", data.gender);
        }
        if (data.dob != null) {
            selectDOB.setAttribute("data-selected-date", data.dob);
        }
        if (data.email != null) {
            document.getElementById("email").setAttribute("placeholder", data.email);
        }
        if (data.contact != null) {
            document.getElementById("contact").setAttribute("placeholder", data.contact);
        }
        if (data.emergency_contact != null) {
            document.getElementById("emergency_contact").setAttribute("placeholder", data.emergency_contact);
        }
        if (data.address != null) {
            document.getElementById("address").setAttribute("placeholder", data.address);
        }
        cancelEditing();
    });
}


function editUname() {
    submitUname.hidden = false;
    chngUname.textContent = "Cancel";
    chngUname.classList.remove("btn-primary");
    chngUname.classList.add("btn-danger");
    unameField.disabled = false;
    unameField.addEventListener("input", function() {
        submitUname.disabled = false;
    });
}

function cancelEditingUname() {
    unameField.disabled = true;
    unameField.value = "";
    submitUname.hidden = true;
    submitUname.disabled = true;
    chngUname.textContent = "Change Username";
    chngUname.classList.remove("btn-danger");
    chngUname.classList.add("btn-primary");
    unameMessage.textContent = "";
    isUnameEditable = false;
}

function updateUname() {
    const data = {};
    data["username"] = unameField.value;

    url = submitUname.getAttribute("data-url");

    // Send data to the server using fetch API
    fetch(url, {
        method: "POST",
        headers: {
            // Set the correct Content-Type header here
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Handle success or display error message
        if (data.message == 'username taken') {
            unameMessage.textContent = "*Username is already taken. Try a different one.";
        } else if (data.message != 'username taken') {
            document.getElementById("username").setAttribute("placeholder", data.username);
            document.getElementById("nav-username").innerText = data.username;
            cancelEditingUname();
        } else {
            unameMessage.textContent = "*ERROR: Please contact support.";
        }
    });
}
